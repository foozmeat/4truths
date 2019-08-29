import csv
import statistics
import json
from urllib.parse import urlparse

input_csv = 'Interactive Media Bias Chart - Ad Fontes Media.csv'
sites = {}

"""
Collect the data
"""
line = 0
with open(input_csv) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:

        if line > 0:
            site, url, bias, quality = row

            if not sites.get(site):
                parsed_uri = urlparse(url)

                sites[site] = {
                    'url': f"{parsed_uri.scheme}://{parsed_uri.netloc}",
                    'b':   [float(bias)],
                    'q':   [float(quality)]
                }
            else:
                sites[site]['b'].append(float(bias))
                sites[site]['q'].append(float(quality))
        line += 1

l_biases = []
r_biases = []

sites_to_save = []
sites_to_remove = [
    'The Skimm',
    'Jacobin',
    'Vanity Fair',
    'OZY',
    'Weather.com',
]

"""
Clean out sites we don't want and figure out where to split the buckets
"""
for site, data in sites.items():
    q_med = statistics.median(data['q'])

    if q_med >= 32.0 and site not in sites_to_remove:
        b_med = statistics.median(data['b'])

        if b_med >= 0:
            r_biases.append(b_med)
        else:
            l_biases.append(b_med)

        data = (site, sites[site]['url'], b_med, q_med)
        sites_to_save.append(data)

l_median = statistics.median(l_biases)
r_median = statistics.median(r_biases)

"""
Split into buckets
"""
print("Left/Right Median", l_median, r_median)

l2_sites = []
l1_sites = []
r1_sites = []
r2_sites = []

for site in sites_to_save:

    if site[2] < l_median:
        l2_sites.append(site)
    elif site[2] < 0:
        l1_sites.append(site)
    elif site[2] < r_median:
        r1_sites.append(site)
    else:
        r2_sites.append(site)

print("Bucket Sizes", len(l2_sites), len(l1_sites), len(r1_sites), len(r2_sites), )

with open('sites.csv', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Site', 'URL', 'B', 'Q'])

    for site in sites_to_save:
        csv_writer.writerow(site)

with open('sites.json', 'w') as fp:
    json.dump([l2_sites, l1_sites, r1_sites, r2_sites], fp, indent=4)
