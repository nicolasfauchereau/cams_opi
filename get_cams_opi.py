#!/Users/nicolasf/anaconda/bin/python

import os, sys
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

dpath = os.path.join(os.environ['HOME'], 'data/cams_opi')

today = datetime.utcnow()

date = today - relativedelta(months=1)

ym = date.strftime("%Y%m")
cmd = "curl --silent ftp://ftp.cpc.ncep.noaa.gov/precip/data-req/cams_opi_v0208/cams_opi_merged.{0} -o {1}/cams_opi_merged.{0}".format(ym, dpath)
os.system(cmd)
