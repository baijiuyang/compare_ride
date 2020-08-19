# compare_ride
Play multiple gpx files together to compare different bike ride on the same route!

Gpx files can be acquired from tracking devices or exported from Strava.

To avoid ambiguity on start and end location, try to use one-way ride instead round trip or laps. You can extract one-way segment from gpx files using GPX Splitter: http://iamdanfox.github.io/gpxsplitter/#

You can play with two example gpx files (1.gpx, 2.gpx) in the repo.

Enjoy!

# Required packages:
Python >= 3.6

numpy

matplotlib

gpxpy


# Command line arguments:
--filename: the name(s) of gpx file(s)

--startloc, --endloc: the latitude and longitude or the start and end location for animation (can be acquired on google map, do not need to be on the gpx path) 

--speed: the play back speed

--save: toggle to save animation to a mp4 file (might take a couple minutes)

# Command line example:
python ride_compare.py --filename 1.gpx 2.gpx --startloc 41.787215 -71.456121 --endloc 41.690784 -71.699043 --save
