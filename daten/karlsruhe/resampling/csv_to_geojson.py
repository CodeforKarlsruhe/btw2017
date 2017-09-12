#!/usr/bin/env python3

'''
Takes data from a CSV file (in the format used by the Transparenzportal)
and adds it to a GeoJSON file containing the suburbs of Karlsruhe.

Usage::

    csv_to_geojson.py CSV_FILE GEOJSON_FILE COLUMN YEAR PROPERTY OUTPUT_FILE

``CSV_FILE`` is the filename of a CSV file downloaded from the
Transparenzportal.

``GEOJSON_FILE`` is a GeoJSON file that contains a GeoJSON feature for
each suburb of Karlsruhe. The features must have a property
``Stadtteilname`` containing the name of the suburb.

``COLUMN`` is the column from the CSV file which should be exported.
This must match one of the column names in the CSV header line.

``YEAR`` is the year for which data should be exported.

``PROPERTY`` is the name of the property under which the data is stored
in the GeoJSON features. An existing property of the same name is
overwritten.

``OUTPUT_FILE`` is the filename to which the updated GeoJSON is written.
This can be the same as ``GEOJSON_FILE``. An existing file of the same
name is overwritten.
'''

import csv
import json
import os


if __name__ == '__main__':
    from pprint import pprint
    import sys

    if len(sys.argv) != 7:
        sys.exit(('Usage: {} CSV_FILE GEOJSON_FILE COLUMN YEAR PROPERTY ' +
                  'OUTPUT_FILE').format(sys.argv[0]))
    csv_filename = sys.argv[1]
    geojson_filename = sys.argv[2]
    column = sys.argv[3]
    year = sys.argv[4]
    prop = sys.argv[5]
    output_filename = sys.argv[6]

    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC)
        rows = list(reader)

    with open(geojson_filename, 'r', encoding='utf-8') as f:
        suburbs = json.load(f)

    def find_suburb(name):
        for feature in suburbs['features']:
            if feature['properties'].get('Stadtteilname') == name:
                return feature
        raise KeyError('No such suburb "{}"'.format(name))

    for row in rows[1:]:
        if row['Jahr'] != year:
            continue
        feature = find_suburb(row['Stadtteil'])
        feature['properties'][prop] = row[column]
        print('{}: {}'.format(row['Stadtteil'], row[column]))

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(suburbs, f)

