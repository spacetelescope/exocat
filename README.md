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
3. `Right Ascension` = Right Ascension in hh:mm:ss
4. `Declination` = Declination in dd:mm:ss
5. `Dispersive Element` = Dispersive element that delivers the spectra (e.g. G102, G141, G280)
6. `Phase Start`	= Starting planet orbital phase for visit window start (range: 0 to 1)
7. `Phase End`	= End planet orbital phase for visit window start (range: 0 to 1)
8. `Observing Mode` = Observing mode (e.g., Stare, Forward/Reverse/Roundtrip Spatial Scan)
9. `Scan Rate`	= The scanning rate, in arcsec per second, if observation mode is set to spatial scan
10. `Visit Number` = Visit number
11. `Date/Time Start` = The start date and time of the visit
12. `Date/Time End` = The end date and time of the visit
13. `Num of Orbits`	= The number of orbits observed
14. `Status` = Status of data (e.g., Archived, Failed, Scheduling, Implementation)
15. `PI Family Name` = PI family name
16. `Proprietary Period` = Proprietary period in months

## Contact
If you have any questions/comments/suggestions on ExoCat, please click the `Issues` tab at the top of this page to submit a ticket or contact us through the <a href="https://www.stsci.edu/contents/news/wfc3-stans/wfc3-stan-issue-34-january">HST Help Desk</a>, and we will respond as soon as possible.
