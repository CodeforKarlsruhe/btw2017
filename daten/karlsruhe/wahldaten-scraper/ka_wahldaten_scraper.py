#!/usr/bin/env python
# encoding: utf-8

'''
Scraper for election results for the Bundestag election for Karlsruhe.

The results are published online as an HTML-export from PC-Wahl. This
scraper uses the per-district results from that export for both the
first and second votes and combines them into a single dataset.
'''

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import re


BOROUGHS = {
    1: 'Innenstadt-Ost',
    2: 'Innenstadt-West',
    3: 'Südstadt',
    4: 'Südweststadt',
    5: 'Weststadt',
    6: 'Nordweststadt',
    7: 'Oststadt',
    8: 'Mühlburg',
    9: 'Daxlanden',
    10: 'Knielingen',
    11: 'Grünwinkel',
    12: 'Oberreut',
    13: 'Beiertheim-Bulach',
    14: 'Weiherfeld-Dammerstock',
    15: 'Rüppurr',
    16: 'Waldstadt',
    17: 'Rintheim',
    18: 'Hagsfeld',
    19: 'Durlach',
    20: 'Grötzingen',
    21: 'Stupferich',
    22: 'Hohenwettersbach',
    23: 'Wolfartsweier',
    24: 'Grünwettersbach',
    25: 'Palmbach',
    26: 'Neureut',
    27: 'Nordstadt',
}


def district_to_borough(district_num):
    '''
    Return the borough number for a district.
    '''
    parts = district_num.split('-')
    return int(parts[0])


def extract_table(table):
    '''
    Extract data from a BeautifulSoup table.

    Returns the table's data as a nested list of strings.
    '''
    rows = []
    for tr in table.find_all('tr'):
        rows.append([td.get_text(separator='\n').strip() for td in tr.find_all(['td', 'th'])])
    return rows


def fix_district_number(s):
    '''
    Fix the number of a voting district to match our other data.
    '''
    parts = s.split('.')
    return parts[0].rjust(3, '0') + '-' + parts[1].rjust(2, '0')


def parse_german_number(s):
    '''
    Parse a number string that uses German separators.

    Returns ``None`` if the string could not be parsed.
    '''
    s = s.replace('.', '')
    try:
        if ',' in s:
            return float(s.replace(',', '.'))
        else:
            return int(s)
    except ValueError:
        return None


def collapse_whitespace(s):
    '''
    Collapse all adjacent whitespace to a single space and strip the string.
    '''
    return re.sub(r'\s+', ' ', s).strip()


if __name__ == '__main__':

    import sys
    if sys.version_info.major == 3:
        from urllib.request import urlopen
        import csv
    else:
        from urllib import urlopen
        from backports import csv
    import io
    import json

    from bs4 import BeautifulSoup

    if len(sys.argv) != 3:
        sys.exit('Usage: {} INPUT_FILE OUTPUT_FILE'.format(sys.argv[0]))
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    # fv = first vote, sv = second vote

    FV_URL = 'http://web3.karlsruhe.de/Stadtentwicklung/afsta/Wahlen/Wahlabend-Netmodul/2013-btw/erst/bundestag-2013-erst-wbz.php'
    SV_URL = 'http://web3.karlsruhe.de/Stadtentwicklung/afsta/Wahlen/Wahlabend-Netmodul/2013-btw/zweit/bundestag-2013-zwei-wbz.php'

    def get_data_from_url(url):
        '''
        Get tabular vote data from an URL.
        '''
        html = urlopen(url).read()
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table')
        assert len(tables) == 2
        return extract_table(tables[1])

    fv_data = get_data_from_url(FV_URL)
    sv_data = get_data_from_url(SV_URL)
    assert len(fv_data) == len(sv_data)

    fv_header = fv_data[0]
    sv_header = sv_data[0]
    candidates = [collapse_whitespace(s) for s in fv_header[5:]]
    parties = [collapse_whitespace(s) for s in sv_header[5:]]

    def parse_votes(row, names):
        '''
        Parse the first/second votes of a single voting district.
        '''
        votes = []
        for cell, name in zip(row[5:], names):
            parts = cell.split()
            num_votes = parse_german_number(parts[0])
            if '(' in name:
                parts = name.split('(')
                party = parts[1].rstrip(')').strip()
                parts = parts[0].split(',')
                if parts[0].startswith('Dr. '):
                    name = 'Dr.' + parts[1] + parts[0][4:]
                else:
                    name = parts[1] + parts[0]
                name = name.replace('- ', '-')
                name = re.sub(r'-([a-z])', r'\1', name)
                votes.append({
                    'name': name,
                    'partei': party,
                    'stimmen': num_votes,
                })
            else:
                votes.append({
                    'partei': name,
                    'stimmen': num_votes,
                })
        return votes

    # Parse data for each district
    districts = {}
    for fv_row, sv_row in zip(fv_data[1:], sv_data[1:]):
        for i in range(5):
            assert fv_row[i] == sv_row[i]
        district_num = fix_district_number(fv_row[0])
        borough_num = district_to_borough(district_num)
        btw2017 = {
            'wahlberechtigte': parse_german_number(fv_row[2]),
            'waehler/-innen': parse_german_number(fv_row[3]),
            'erststimme': parse_votes(fv_row, candidates),
            'zweitstimme': parse_votes(sv_row, parties),
            'wahlbeteiligung': parse_german_number(fv_row[4].rstrip('%')),
        }
        district = {
            'stadtteilnummer': borough_num,
            'stadtteilname': BOROUGHS.get(borough_num),
            'wahlbezirksnummer': district_num,
            'wahlbezirksname': fv_row[1],
            'btw2017': btw2017,
        }
        districts[district_num] = district

    # Remove postal votes
    for district_num in list(districts.keys()):
        if districts[district_num]['wahlbezirksname'] == 'Briefwahl':
            districts.pop(district_num)

    # Export to GeoJSON
    with open(input_filename, 'r', encoding='utf-8') as f:
        geojson = json.load(f)
    for f in geojson['features']:
        p = f['properties']
        district = districts[p['wahlbezirksnummer']]
        if district['wahlbezirksname'] != p['wahlbezirksname']:
            print((district['wahlbezirksname'], p['wahlbezirksname']))
        p.update(district)
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(geojson, f)

