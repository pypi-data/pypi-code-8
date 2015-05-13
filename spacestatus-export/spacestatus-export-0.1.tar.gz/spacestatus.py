import datetime

import requests, vlermv

DIR = '~/.spacestatus-export'

@vlermv.cache(DIR, 'directory')
def get_directory(date):
    url = 'http://spacestatus.bastinat0r.de/spaces/_design/all/_view/json'
    return requests.get(url)

@vlermv.cache(DIR, 'hackerspace')
def get_hackerspace(date, name):
    dt = datetime.datetime.fromordinal(date.toordinal()).timestamp()
    url = 'http://spacestatus.bastinat0r.de/%s/_design/space/_view/all?endkey=%f'
    return requests.get(url % (name, dt))

def main():
    import sys, csv
    today = datetime.date.today()

    writer = csv.writer(sys.stdout)
    writer.writerow(('hackerspace', 'timestamp', 'open'))

    directory_response = get_directory(today)
    if not directory_response.ok:
        sys.stderr.write('Error downloading directory\n')
        sys.exit(1)

    for hackerspace in directory_response.json().get('rows', []):
        hackerspace_name = hackerspace['value']['name']
        hackerspace_response = get_hackerspace(today, hackerspace_name)
        if not directory_response.ok:
            sys.stderr.write('Error downloading hackerspace\n')
            sys.exit(2)

        for reading in hackerspace_response.json().get('rows', []):
            row = (
                hackerspace_name,
                reading['value']['lastchange'],
                str(reading['value']['open']).upper(),
            )
            writer.writerow(row)

if __name__ == '__main__':
    main()
