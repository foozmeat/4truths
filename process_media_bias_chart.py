import csv
import statistics
import json
from urllib.parse import urlparse

input_csv = 'Interactive Media Bias Chart - Ad Fontes Media.csv'
sites = {}

line = 0
with open(input_csv) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:

        if line > 0:
            site, url, bias, quality = row

            if not sites.get(site):
                parsed_uri = urlparse(url)

                sites[site] = {
                    'url':  f"{parsed_uri.scheme}://{parsed_uri.netloc}",
                    'b': [float(bias)],
                    'q': [float(quality)]
                }
            else:
                sites[site]['b'].append(float(bias))
                sites[site]['q'].append(float(quality))
        line += 1

with open('sites.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Site', 'B', 'Q'])

    for site, data in sites.items():
        sites[site]['b_med'] = statistics.median(data['b'])

        sites[site]['q_med'] = statistics.median(data['q'])

        if sites[site]['q_med'] >= 32.0:
            csv_writer.writerow([site, sites[site]['url'], sites[site]['b_med'], sites[site]['q_med']])


