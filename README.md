# README #

## get_ozone_pv.py ##

Run with python 3

- run code with "python get_ozone_pv.py"

- can use a command line argument "python get_ozone_pv.py all" will download ALL the PV maps since 2015 instead of just the last 30 maps

It creates a "PV" and "ozone" folder if they don't already exist. In ozone\ a folder named YYYY-MM-DD is created based on the current date.

In PV\ it downloads the images from http://www.pa.op.dlr.de/arctic/ecmwf.php

In ozone\YYYY-MM-DD it downloads all the total ozone and deviation maps from http://exp-studies.tor.ec.gc.ca/e/ozone/Curr_allmap.htm

the naming convention I use is:

NH-tot-O3-YYMMDD.png for northern hemisphere total ozone map of the specified date

SH-dev-O3-YYMMDD.png for the southern hemisphere deviation map of the specified date

GL-.... for global maps

The ozone maps are updated daly after 14 UTC