#!/usr/bin/env python3

'''
Small script to merge the data from the CSV into the GeoJSON.
'''

if __name__ == '__main__':
    import csv
    import json
    from pprint import pprint
    import sys

    if len(sys.argv) != 4:
        sys.exit('Usage: {} CSV_FILE GEOJSON_FILE OUTPUT_FILE'.format(
                 sys.argv[0]))
    csv_filename = sys.argv[1]
    geojson_filename = sys.argv[2]
    output_filename = sys.argv[3]

    with open(csv_filename, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC))
    rows = {row['Wahlbezirksnummer']: row for row in rows}

    with open(geojson_filename, 'r', encoding='utf-8') as f:
        districts = json.load(f)

    for feature in districts['features']:
        props = feature['properties']
        row = rows[props['Wahlbezirksnummer']]
        props.update(row)

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(districts, f)

