#!/usr/bin/env python
 # -*- coding: ascii -*-

####################
# Code description #
####################
'''

Run with python 3

- put python file in a folder
- run code from that folder "python get_ozone_pv.py"
- can use a command line argument "python get_ozone_pv.py all" will download ALL the PV maps since 2015 instead of just the last 30 maps

It creates a "PV" and "ozone" folder if they don't already exist. In ozone\ a folder named YYYY-MM-DD is created based on the current date.

In PV\ it downloads the images from http://www.pa.op.dlr.de/arctic/ecmwf.php

In ozone\YYYY-MM-DD it downloads all the total ozone and deviation maps from http://exp-studies.tor.ec.gc.ca/e/ozone/Curr_allmap.htm

the naming convention I use is:

NH-tot-O3-YYMMDD.png for northern hemisphere total ozone map of the specified date
SH-dev-O3-YYMMDD.png for the southern hemisphere deviation map of the specified date
GL-.... for global maps
'''

####################
# Import libraries #
####################

import urllib.request

import os

import time
from datetime import datetime, timedelta

import sys

#########
# Setup #
#########

argu = sys.argv

# get working directory
working_dir = os.getcwd()

# path to the folder where potential vorticity maps are saved
PV_path = os.path.join(working_dir,'PV')

# path to the folder where ozone maps are saved
ozone_path = os.path.join(working_dir,'ozone') 

# if those folders don't exist already, make them
for path in [PV_path,ozone_path]:
	if not os.path.isdir(path):
		os.mkdir(path)

# Toronto time
today_toronto = datetime.utcnow()-timedelta(hours=5)
yesterday_toronto = today_toronto - timedelta(days=1)

# format a new folder name as YYYY-MM-DD based on today_toronto time
new_folder = today_toronto.strftime('%Y-%m-%d')

# create a new folder with that name in the ozone folder
new_ozone_path = os.path.join(ozone_path,new_folder)
if not os.path.isdir(new_ozone_path):
	os.mkdir(new_ozone_path)

# ozone urls
fmt = today_toronto.strftime('%Y%m%d') # YYMMDD
fmt_1 = yesterday_toronto.strftime('%Y%m%d') # YYMM(DD-1)
ozone_urls = {	'NH-tot-O3-'+fmt+'.png':'http://exp-studies.tor.ec.gc.ca/ozone/images/graphs/o3_hrmaps/current.gif',
				'NH-tot-O3-'+fmt_1+'.png':'http://exp-studies.tor.ec.gc.ca/ozone/images/graphs/o3_hrmaps/current_1.gif',
				'NH-dev-O3-'+fmt+'.png':'http://exp-studies.tor.ec.gc.ca/ozone/images/graphs/o3_hrmaps_dev/current.gif',
				'NH-dev-O3-'+fmt_1+'.png':'http://exp-studies.tor.ec.gc.ca/ozone/images/graphs/o3_hrmaps_dev/current_1.gif',
				'SH-tot-O3-'+fmt+'.png':'http://exp-studies.tor.ec.gc.ca/ozone/images/graphs/sh/current.gif',
				'SH-tot-O3-'+fmt_1+'.png':'http://exp-studies.tor.ec.gc.ca/ozone/images/graphs/sh/current_1.gif',
				'SH-dev-O3-'+fmt+'.png':'http://exp-studies.tor.ec.gc.ca/ozone/images/graphs/sh_dev/current.gif',
				'SH-dev-O3-'+fmt_1+'.png':'http://exp-studies.tor.ec.gc.ca/ozone/images/graphs/sh_dev/current_1.gif',
				'GL-tot-O3-'+fmt+'.png':'http://exp-studies.tor.ec.gc.ca/ozone/images/graphs/gl/current.gif',
				'GL-tot-O3-'+fmt_1+'.png':'http://exp-studies.tor.ec.gc.ca/ozone/images/graphs/gl/current_1.gif',
				'GL-dev-O3-'+fmt+'.png':'http://exp-studies.tor.ec.gc.ca/ozone/images/graphs/gl_dev/current.gif',
				'GL-dev-O3-'+fmt_1+'.png':'http://exp-studies.tor.ec.gc.ca/ozone/images/graphs/gl_dev/current_1.gif',					
				}

# PV website index
PV_url = 'http://www.pa.op.dlr.de/arctic/tropoth/'
with urllib.request.urlopen(PV_url) as response:

	if 'all' in argu:
		PV_html = str(response.read()).split('\\n')[39:-3] # all the past maps
	else:
		PV_html = str(response.read()).split('\\n')[-33:-3] # only the last 30 maps

#############
# Execution #
#############

#PV
print('\nNow doing PV maps:\n')

for line in PV_html:
	gif_name = line.split()[-4].split('"')[1]

	img_path = os.path.join(PV_path,gif_name)

	if not os.path.exists(img_path):
		print('Now requesting '+PV_url+gif_name)
		urllib.request.urlretrieve(PV_url+gif_name,img_path)
	else:
		print('Already downloaded '+PV_url+gif_name)

# ozone
print('\nNow doing ozone maps:\n')
# download each ozone image
failcheck = True
while failcheck:
	failcount = 0
	for key in ozone_urls.keys():
		img_path = os.path.join(new_ozone_path,key)
		if not os.path.exists(img_path):
			print('Now requesting '+ozone_urls[key])
			try:
				urllib.request.urlretrieve(ozone_urls[key], img_path)
			except (urllib.error.URLError,TimeoutError) as e:
				failcount +=1
				continue
		else:
			print('Already downloaded '+ozone_urls[key])
	if failcount==0:
		failcheck = False

print('\nDONE')