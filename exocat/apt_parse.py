"""Downloads Phase II APT files to parse for data needed to fill
out the ExoCat table.


Authors
-------
    - Catherine Martlin, 2020
    - Jennifer Medina, 2020
Use
---
    This module is intended to be called by ``parse_apt.py``
    as part of the ExoCat pipeline.
Notes
-----
    We currently have a list of proposals hardcoded - may need to
    update in the future.
"""
from datetime import datetime
import astroquery.mast as mast
import logging
import numpy as np
import pandas as pd
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET

def make_proposal_list():
    """ Generates a list of proposals dedicated to WFC3 IR exoplanet
    observations whose files will be downloaded using `fetch_apt`.
    """

    proposal_list = mast.Observations.query_criteria(project='HST',
                                                     instrument_name='WFC3/IR')['proposal_id']
    proposal_list = np.unique(proposal_list)

    return list(proposal_list)


def fetch_apt(proposal_number = '15469'):
    """Downloads and saves the APT version of a proposal.

    Parameters
    ----------
    proposal_number : string
        The proposal number

    Returns
    -------
    True or False : binary
    True if the html request succeeds
    False if the html request fails
    """
    keywords = ['exoplanet', 'extra solar', 'mini neptune']

    webpage = ('http://www.stsci.edu/hst/phase2-public/{}.apt'.format(proposal_number))
    try:
        response = urllib.request.urlopen(webpage)
        html_bytes = response.read()
    except urllib.error.HTTPError:
        #logging.info('Error: Could not retrieve %s' % file)
        return False

    # Verify exoplanet
    html = html_bytes.decode('latin-1')

    abstract_start, abstract_end = html.find('<Abstract>'), html.find('</Abstract>')
    obsdesc_start, obsdesc_end = html.find('<ObservingDescription>'), html.find('</ObservingDescription>')

    abstract = html[abstract_start:abstract_end]
    #observing_description = html[obsdesc_start:obsdesc_end]
    for keyword in keywords:
        if (keyword in abstract.lower()):

            filename = proposal_number + '.apt'
            print(proposal_number)
            f = open(filename, "wb")
            f.write(html_bytes)
            f.close()

            return True

        else:
            return False

def fetch_visit_status(proposal_number='15469'):
    proposal_number = str(proposal_number)
    
    webpage = ('https://www.stsci.edu/cgi-bin/get-visit-status?id={}&markupFormat=xml&observatory=HST'.format(proposal_number)) 
    try:
        response = urllib.request.urlopen(webpage)
        html = response.read()
    except urllib.error.HTTPError:
        #logging.info('Error: Could not retrieve %s' % file)
        return False
    
    filename = proposal_number + '_visit_status.xml'
    
    f = open(filename, "wb")
    f.write(html)
    f.close()
    
    return True

def read_apt(proposal_number = '15469'):
    """Uses the APT file to read in values we want for the
    ExoCat table.

    Parameters
    ----------
    proposal_number : string
        The proposal number

    Returns
    -------
    save_path : string
    Path the final exocat table is saved at as a csv file.
    """

    apt_file = proposal_number + '.apt'

    #We are using XML to read in the file
    tree = ET.parse(apt_file)
    entire_file = tree.getroot()

    # To find the values we gather data from several
    # places that I will list in different sections and then
    # we will combine them into a single table.
    targets_info = entire_file.findall('Targets/FixedTarget')
    RA_info = entire_file.findall('Targets/FixedTarget/EquatorialPosition/RA')
    DEC_info = entire_file.findall('Targets/FixedTarget/EquatorialPosition/DEC')
    observations_info = entire_file.findall('Observations/Observation')
    visits_info = entire_file.findall('Visits/Visit')
    exposures_info = entire_file.findall('Visits/Visit/ExposureGroup/Exposure')
    spatial_scan_info = entire_file.findall('Visits/Visit/ExposureGroup/Exposure/SpatialScan')
    phase_info = entire_file.findall('Visits/Visit/ExposureGroup/Exposure/Phase')

    if not spatial_scan_info:
        warning = apt_file + " has no spatial scan info."
        logging.info(warning)

    if not phase_info:
        warning = apt_file + " has no phase info."
        logging.info(warning)

    RA = []
    for element in RA_info:
        hrs = (element.get('Hrs'))
        mins = (element.get('Mins'))
        secs = (element.get('Secs'))
        ra = str(hrs) + " " + str(mins) + " " + str(secs) 
        RA.append(ra)

    DEC = []
    for element in DEC_info:
        deg = (element.get('Degrees'))
        arcmin = (element.get('Arcmin'))
        arcsec = (element.get('Arcsec'))
        dec = str(deg) + " " + str(arcmin) + " " + str(arcsec) 
        DEC.append(dec)

    rate = []
    direction = []
    for element in spatial_scan_info:
        rate.append(element.get('Rate'))
        direction.append(element.get('Direction'))

    phase_start = []
    phase_end = []
    for element in phase_info:
        phase_start.append(element.get('Start'))
        phase_end.append(element.get('End'))

    exp_num = []
    target_name_exposure = []
    spectral_element = []
    label = []
    for element in exposures_info:
        exp_num.append(element.get('Number'))
        target_name_exposure.append(element.get('TargetName'))
        spectral_element.append(element.get('SpElement'))
        label.append(element.get('Label'))

    status = []
    number = []
    label = []
    for element in visits_info:
        status.append(element.get('Status'))
        number.append(element.get('Number'))
        label.append(element.get('Label'))

    target_name_obs=[]
    NumberOfOrbits = []
    for element in observations_info:
        target_name_obs.append(element.get('TargetName'))
        NumberOfOrbits.append(element.get('NumberOfOrbits'))

    target_name=[]
    for element in targets_info:
        target_name.append(element.get('Name'))

    # create dataframes from the different sections:
    target_name_exposure = np.array(target_name_exposure)
    spectral_element = np.array(spectral_element)
    exp_num = np.array(exp_num)
    exposure_df = pd.DataFrame(list(zip(exp_num, target_name_exposure, spectral_element)), columns=['exposure_number','target_name_exposure','spectral_element'])

    # Remove aquisition/other instrument exposures:
    exposure_df = exposure_df[exposure_df['spectral_element'].str.contains('G141|G102')]
    exposure_df = exposure_df.reset_index()
    exposure_df = exposure_df.drop(['index'], axis=1)

    target_name_obs = np.array(target_name_obs)
    NumberOfOrbits = np.array(NumberOfOrbits)
    observations_df = pd.DataFrame(list(zip(target_name_obs,NumberOfOrbits)), columns=['target_name_obs', 'number_orbits'])

    rate = np.array(rate)
    direction = np.array(direction)
    sp_scan_df = pd.DataFrame(list(zip(rate, direction)),columns=['rate','direction'])

    phase_start = np.array(phase_start)
    phase_end = np.array(phase_end)
    phase_df = pd.DataFrame(list(zip(phase_start, phase_end)), columns=['phase_start', 'phase_end'])

    target_name = np.array(target_name)
    target_df = pd.DataFrame((target_name), columns = ['target_name'])

    status = np.array(status)
    number = np.array(number)
    label = np.array(label)
    visits_info_df = pd.DataFrame(list(zip(status, number, label)), columns = ['status', 'visit_number','label'])
    
    RA = np.array(RA)
    DEC = np.array(DEC)
    coord_info_df = pd.DataFrame(list(zip(RA, DEC)), columns = ['RA', 'Dec'])

    # Add phase and label to visit info: 
    visits_info_df_label = visits_info_df.drop_duplicates(subset = ["label"])
    visits_info_df_label = visits_info_df_label.reset_index()
    phase_df['label'] = visits_info_df_label['label']
    
    visits_info_df['phase_start'] = 0
    visits_info_df['phase_end'] = 0

    for x in range(len(visits_info_df['label'])):
        for y in range(len(phase_df['label'])):
            if visits_info_df['label'][x] == phase_df['label'][y]:
                visits_info_df['phase_start'][x] = phase_df['phase_start'][y]
                visits_info_df['phase_end'][x] = phase_df['phase_end'][y]

    #fix table with orbit numbers:
    if len(visits_info_df.index) != len(observations_df.index):
        visits_no_fail = visits_info_df.copy()
        failed_visits = visits_info_df[visits_info_df['status'].str.contains('failed')].index
        visits_no_fail.drop(failed_visits, inplace=True)
        visits_no_fail = visits_no_fail.reset_index()
        obs_and_visits_df = pd.concat([observations_df, visits_no_fail], axis=1)
        obs_and_visits_df = obs_and_visits_df.drop(['index'], axis=1)
        obs_and_visits_df = obs_and_visits_df.drop(['target_name_obs'], axis=1)
        obs_and_visits_df = obs_and_visits_df.drop(['status'], axis=1)
    else:
        obs_and_visits_df = pd.concat([observations_df, visits_info_df], axis=1)
        obs_and_visits_df = obs_and_visits_df.drop(['target_name_obs'], axis=1)
        obs_and_visits_df = obs_and_visits_df.drop(['status'], axis=1)

    # Add RA/Dec to exposure table: 
    # Add RA/Dec to exposure table: 
    target_df['RA'] = coord_info_df['RA']
    target_df['Dec'] = coord_info_df['Dec']
    exposure_df = pd.merge(target_df, exposure_df, left_on='target_name', right_on='target_name_exposure')
    
    #combine tables:
    combine1 = pd.concat([exposure_df,sp_scan_df], axis=1)
    reduce1 = combine1[combine1["exposure_number"] == '2']
    reduce1 = reduce1.reset_index()
    reduce1 = reduce1.drop(['index'], axis=1)
    combine2 = pd.concat([reduce1, visits_info_df], axis=1)
    combine2 = combine2.drop(['exposure_number'], axis=1)
    combine2 = combine2[combine2['spectral_element'].notna()]


    #If there are missing target_name we use the visit_label to name it: 
    if combine2['target_name_exposure'].isnull().values.any() == True: 
        for x in range(len(combine2['target_name_exposure'])):
            if pd.isna(combine2['target_name_exposure'][x]):
                visit_num = combine2['visit_number'][x]
                index = visits_info_df[visits_info_df['visit_number']==visit_num].index.values
                combine2['target_name_exposure'][x] = visits_info_df['label'][index[0]]

    #add column with proposal number:
    total_entries = len(combine2.index)
    proposal_list = []
    for x in range(total_entries):
        proposal_list.append(proposal_number)
    prop_list = np.array(proposal_list)
    prop_df = pd.DataFrame((prop_list), columns=['proposal_number'])

    #final dataframe
    add_orbits = pd.merge(combine2, obs_and_visits_df, on='visit_number')
    final_table = pd.concat([combine2, prop_df], axis=1)

    #save final_table
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    save_path = proposal_number + '_exocat_' + dt_string + '.csv'
    final_table.to_csv(save_path)

    return save_path

def read_visit_status(proposal_number = '15469'):
    """Uses the visit status file to read in the visit date/time

    Parameters
    ----------
    proposal_number : string
        The proposal number

    Returns
    -------

    """
    proposal_number = str(proposal_number)
    filename = proposal_number + '_visit_status.xml'

    #We are using XML to read in the file
    tree = ET.parse(filename)
    entire_file = tree.getroot()
    print(entire_file)
    
    visits = entire_file.findall('visit')
    statuses = entire_file.findall('visit/status')
    targets = entire_file.findall('visit/target')
    startTimes = entire_file.findall('visit/startTime')
    endTimes = entire_file.findall('visit/endTime')
    
    visit_list = []
    for visit in visits: 
        visit_list.append(visit.get('id'))

    status_list = []
    for elem in statuses: 
        status_list.append(elem.text)

    targets_list = []
    for elem in targets: 
        targets_list.append(elem.text)

    startTimes_list = []
    for elem in startTimes: 
        startTimes_list.append(elem.text)

    endTimes_list = []
    for elem in endTimes: 
        endTimes_list.append(elem.text)
        
    all_info = list(zip(visit_list, status_list, targets_list, startTimes_list, endTimes_list))


def main():
    """The main function that will run a list of proposals. Also sets
    up and logs timing and information of each run.


    Parameters
    ----------
    proposal_list : list
        The proposal numbers

    Returns
    -------
    """
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    logging_name = 'apt_parsing_log_' + dt_string +'.txt'
    logging.basicConfig(filename=logging_name, format='%(asctime)s - %(message)s', level=logging.INFO)

    proposal_list = make_proposal_list()
    print(proposal_list)
    for prop in proposal_list:
        prop = str(prop)
        logging.info(prop)

        # Fetch the APT file and log the execution time
        start_time = datetime.now()
        output_bool = fetch_apt(proposal_number=prop)

        if output_bool == True:
            time_elapsed = datetime.now() - start_time
            time_info = 'Time elapsed for download {}'.format(time_elapsed)
            logging.info(time_info)

            # Parse the APT file and save the table and log the execution time
            start_time2 = datetime.now()
            try:
                read_apt(proposal_number=prop)
            except ValueError:
                continue
            time_elapsed2 = datetime.now() - start_time2
            time_info2 = 'Time elapsed for parsing {}'.format(time_elapsed2)
            logging.info(time_info2)
        else:
            continue

if __name__ == '__main__':

    print('Executing APT parser')
    main()
