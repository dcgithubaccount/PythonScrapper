from sys import argv

import os,time

script, country = argv

filename = "Archive" + "_" + country + ".csv"

path = "/Volumes/MyData/SharesProject/FTCompanyData/Output"
apath = "/Volumes/MyData/SharesProject/FTCompanyData/archive/Output"

countrypath = os.path.join(path,country)

now = time.time()

for f in os.listdir(countrypath):
	if os.stat(
		os.path.join(countrypath, f)
	).st_mtime < now - 15 * 86400 and os.path.isfile(
		os.path.join(countrypath, f)
	):
		with open(os.path.join(apath,filename),'a') as f1:
			for line in open(os.path.join(countrypath,f)):
				f1.write(line)
		os.remove(os.path.join(countrypath,f))


			 
