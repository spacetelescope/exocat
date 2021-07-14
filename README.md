# The Exoplanet Catalog (ExoCat)


![alt text](https://github.com/spacetelescope/exocat/blob/master/exocat/exocat-logo-2.png)

## What is ExoCat?
This repository hosts the back-end of HST/WFC3's Exoplanet Catalog, ExoCat, which tabulates the status of completed and planned observations of transiting exoplanets by the WFC3 IR instrument. This catalog serves the astronomical community by helping to reduce target duplication and redundant effort in proposal preparation.

Users can search for a target using the target name to see what observation programs already exist for it. Users can also check the status of their program(s) by searching for the proposal ID.

ExoCat is currently hosted by STScI and can be found here: https://www.stsci.edu/~WFC3/exocat/exocat/exocat.html

## ExoCat Layout

The Exoplanet Catalog provides the information found in the Phase 1/2 file of the designated proposal/program. All information provided by ExoCat is non-proprietary and can be found publicly on the STScI website. The following are the 10 columns shown in the catalog, and their descriptions:
1. `Program ID`	= The proposal number, or program ID, as shown in the APT proposal/Phase 2, linking to the GO proposal information
2. `Target`	= The target name as shown in the APT proposal, including any possible alternative name, linking to its corresponding ExoMAST page
3. `R.A.` = Right ascension coordinate
4. `Dec` = Declination coordinate
5. `Status`	= The current status the proposal
6. `SpElement` = Dispersive element that delivers the spectra
7. `Phase Start`	= The start time of the orbital phase
8. `Phase End`	= The end time of the orbital phase
9. `Visit Number` = The number of visits to this target observed
10. `Scan Direction`	= The scan direction, if observation mode is set to spatial scan
11. `Scan Rate`	= The scanning rate, in pixels per second, if observation mode is set to spatial scan
12. `Date Start` = The start date of the observation
13. `Date End` = The end date of the observation
14. `Norbits`	= The number of orbits observed

## Contact
If you have any questions/comments/suggestions on ExoCat, please click the `Issues` tab at the top of this page to submit a ticket or contact us through the <a href="https://www.stsci.edu/contents/news/wfc3-stans/wfc3-stan-issue-34-january">HST Help Desk</a>, and we will respond as soon as possible.
