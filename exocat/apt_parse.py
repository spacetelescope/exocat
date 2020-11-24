"""Downloads Phase II APT files to parse for data needed to fill 
out the ExoCat table. 


Authors
-------
    - Catherine Martlin, 2020
Use
---
    This module is intended to be called by ``parse_apt.py``
    as part of the ExoCat pipeline.
Notes
-----
    We currently have a list of proposals hardcoded - may need to 
    update in the future. 
"""
import numpy as np 
import pandas as pd
import urllib.request 
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET

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

    webpage = ('http://www.stsci.edu/hst/phase2-public/{}.apt'.format(proposal_number)) 
    try:
        response = urllib.request.urlopen(webpage)
        html = response.read()
    except urllib.error.HTTPError:
        #logging.info('Error: Could not retrieve %s' % file)
        return False
    
    filename = proposal_number + '.apt'
    
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
	"""
	apt_file = proposal_number + '.apt'

	#We are using XML to read in the file
	tree = ET.parse(apt_file)
	entire_file = tree.getroot()

	# To find the values we gather data from several 
	# places that I will list in different sections and then 
	# we will combine them into a single table.
	targets_info = entire_file.findall('Targets/FixedTarget')
	observations_info = entire_file.findall('Observations/Observation')
	visits_info = entire_file.findall('Visits/Visit')
	exposures_info = entire_file.findall('Visits/Visit/ExposureGroup/Exposure')
	spatial_scan_info = entire_file.findall('Visits/Visit/ExposureGroup/Exposure/SpatialScan')
	phase_info = entire_file.findall('Visits/Visit/ExposureGroup/Exposure/Phase')

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

	target_name_exposure = []
	spectral_element = []
	label = []
	for element in exposures_info:
	    target_name_exposure.append(element.get('TargetName'))
	    spectral_element.append(element.get('SpElement'))
	    label.append(element.get('Label'))

	status = []
	number = []
	for element in visits_info:
	    status.append(element.get('Status'))
	    number.append(element.get('Number'))

	target_name_obs=[]
	NumberOfOrbits = []
	for element in observations_info:
	    target_name_obs.append(element.get('TargetName'))
	    NumberOfOrbits.append(element.get('NumberOfOrbits'))

	target_name=[]
	for element in targets_info:
	    target_name.append(element.get('Name'))

	# Create dataframes from the different sections: 
	target_name_exposure = np.array(target_name_exposure)
	spectral_element = np.array(spectral_element)
	exposures = zip(target_name_exposure, spectral_element)
	exposure_df = pd.DataFrame((exposures), columns=['target_name_exposure','spectral_element'])

	# Remove aquisition exposures:
	indexNames = exposure_df[exposure_df['spectral_element'].str.contains('F')].index
	exposure_df.drop(indexNames , inplace=True)

	target_name_obs = np.array(target_name_obs)
	NumberOfOrbits = np.array(NumberOfOrbits)
	obs = zip(target_name_obs,NumberOfOrbits)
	observations_df = pd.DataFrame((obs), columns=['target_name_obs', 'number_orbits'])

	rate = np.array(rate)
	direction = np.array(direction)
	sp_scan = zip(rate, direction)
	sp_scan_df = pd.DataFrame((sp_scan),columns=['rate','direction'])

	phase_start = np.array(phase_start)
	phase_end = np.array(phase_end)
	phases = zip(phase_start, phase_end)
	phase_df = pd.DataFrame((phases), columns=['phase_start', 'phase_end'])

	target_name = np.array(target_name)
	target_df = pd.DataFrame((target_name), columns = ['target_name'])

# Still need to gather alternate name from Targets/FixedTarget/AlternateNames
# and Date from Visits/Visit/ToolData/ToolDataItem


