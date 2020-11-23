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

import urllib.request 
import urllib.error
import urllib.parse

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