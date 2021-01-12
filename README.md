# The Exoplanet Catalog (ExoCat)


![alt text](https://github.com/spacetelescope/exocat/blob/master/exocat/exocat-logo-2.png)

## What is ExoCat?
This repository hosts the back-end of HST/WFC3's Exoplanet Catalog, ExoCat, which tabulates the status of completed and planned observations of transiting exoplanets by the WFC3 IR instrument. This catalog serves the astronomical community by helping to reduce target duplication and redundant effort in proposal preparation.

Users can search for a target using the target name to see what observation programs already exist for it. Users can also check the status of their program(s) by searching for the proposal ID. 

ExoCat is currently hosted by STScI and can be found here: https://www.stsci.edu/~WFC3/exocat/exocat/exocat.html

## ExoCat Layout

The Exoplanet Catalog provides the information found in the Phase 1/2 file of the designated proposal/program. All information provided by ExoCat is non-proprietary and available on the STScI website. The following are the 10 columns available in the catalog, and their descriptions:
1. `Target`	= The target name as shown in the APT proposal
2. `Program ID`	= The proposal number, or program ID, as shown in the APT proposal/Phase 2
3. `Status`	= The current status the proposal
4. `SpElement` =
5. `Phase Start`	= The start time of the orbital phase
6. `Phase End`	= The end time of the orbital phase
7. `Norbits`	= The number of orbits observed
8. `Scan Direction`	= The scan direction, if observation mode is set to spatial scan
9. `Scan Rate`	= The scanning rate, in pixels per second, if observation mode is set to spatial scan
10. `Alt. Name` = Alternative name for the target if given. Otherwise, this column is the same as the first

## Contact
If you have any questions/comments/suggestions on ExoCat, please click the `Issue` tab above to submit a ticket or contact us through the <a href="https://www.stsci.edu/contents/news/wfc3-stans/wfc3-stan-issue-34-january">HST Help Desk</a>, and we will respond as soon as possible. 
