import os
from arcgis.gis import GIS
from utils import clean_data

print("Connecting to source Portal...")
source = GIS("https://mormont.esri.es/portal", os.environ["MORMONT_USER"], os.environ["MORMONT_PWD"])

print("Getting group from source...")
dev_group = source.groups.search("Source group - DevSummit 2021")[0]
print(dev_group)
print("Building epk file...")

epk_job = dev_group.migration.create(future=True) # Async call
epk_file = epk_job.result()

print("Downloading export package...")
fp = epk_file.download()
print("Export operation finished:")
print(fp)

print("Connecting to target Portal...")
target = GIS("https://formacionutility.esri.es/portal", os.environ["UTILITY_USER"], os.environ["UTILITY_PWD"])

print("Cleaning data from previous executions")
clean_data(target)

print("Adding export package to Target Portal...")
pitem = target.content.add({'title': "DEVtoTEST Migration Package", "tags": ['Migration', 'TEST', 'Cloning'], 'type': 'Export Package'}, data=fp)
print(pitem)

print("Creating target group...")
new_group = target.groups.create(title="Target group - DevSummit 2021", tags="Migration,Cloning")

print("Sharing Export Package (.epk) to the target group...")
pitem.share(groups = [new_group])

print("Inspecting the epk...")
m = new_group.migration
resp = m.inspect(pitem)
from pprint import pprint
pprint(resp)

print("Executing import operation...")
res = m.load(pitem)
print("Import operation finished")
print(res)