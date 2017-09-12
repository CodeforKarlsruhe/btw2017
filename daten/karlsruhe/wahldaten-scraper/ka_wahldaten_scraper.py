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
        votes = {}
        for cell, name in zip(row[5:], names):
            parts = cell.split()
            num_votes = parse_german_number(parts[0])
            votes[name] = num_votes
        return votes

    # Parse data for each district
    districts = {}
    for fv_row, sv_row in zip(fv_data[1:], sv_data[1:]):
        for i in range(5):
            assert fv_row[i] == sv_row[i]
        district_num = fix_district_number(fv_row[0])
        borough_num = district_to_borough(district_num)
        district = {
            'Wahlkreisnummer': 271,
            'Wahlkreisname': 'Karlsruhe-Stadt',
            'Stadtteilnummer': borough_num,
            'Stadtteilname': BOROUGHS.get(borough_num),
            'Wahlbezirksnummer': district_num,
            'Wahlbezirksname': fv_row[1],
            'Wahlberechtigte insgesamt': parse_german_number(fv_row[2]),
            'Wähler/-innen': parse_german_number(fv_row[3]),
            'Wahlbeteiligung': parse_german_number(fv_row[4].rstrip('%')),
        }
        # Extract votes for each candidate
        district['Erststimmen'] = parse_votes(fv_row, candidates)
        district['Gültige Erststimmen'] = sum(district['Erststimmen'].values())
        district['Zweitstimmen'] = parse_votes(sv_row, parties)
        district['Gültige Zweitstimmen'] = sum(district['Zweitstimmen'].values())
        districts[district_num] = district

    # Combine postal votes into a single row
    postal_votes = {
        'Wahlkreisnummer': 271,
        'Wahlkreisname': 'Karlsruhe-Stadt',
        'Stadtteilname': 'Briefwahl',
        'Stadtteilnummer': None,
        'Wahlbezirksnummer': None,
        'Wahlbezirksname': None,
        'Wahlbeteiligung': None,
        'Wahlberechtigte insgesamt': None,
        'Wähler/-innen': 0,
        'Erststimmen': {},
        'Zweitstimmen': {},
    }
    for district_num in districts.keys():
        if districts[district_num]['Wahlbezirksname'] == 'Briefwahl':
            district = districts.pop(district_num)
            postal_votes['Wähler/-innen'] += district['Wähler/-innen']
            for vote_type in 'Erststimmen', 'Zweitstimmen':
                for key, value in district[vote_type].iteritems():
                    postal_votes[vote_type][key] = postal_votes[vote_type].get(key, 0) + value
                postal_votes['Gültige ' + vote_type] = sum(postal_votes[vote_type].values())
    districts['Briefwahl'] = postal_votes

    # Export to CSV
    CSV_COLUMNS = (['Wahlkreisnummer', 'Wahlkreisname', 'Stadtteilnummer',
                   'Stadtteilname', 'Wahlbezirksnummer', 'Wahlbezirksname',
                   'Wahlberechtigte insgesamt', 'Wähler/-innen',
                   'Gültige Erststimmen'] + candidates + ['Gültige Zweitstimmen']
                   + parties)
    with io.open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)
        for district_num in sorted(districts):
            d = districts[district_num]
            row = [d['Wahlkreisnummer'], d['Wahlkreisname'], d['Stadtteilnummer'],
                   d['Stadtteilname'], d['Wahlbezirksnummer'], d['Wahlbezirksname'],
                   d['Wahlberechtigte insgesamt'], d['Wähler/-innen'],
                   d['Gültige Erststimmen']]
            row.extend(d['Erststimmen'][c] for c in candidates)
            row.append(d['Gültige Zweitstimmen'])
            row.extend(d['Zweitstimmen'][p] for p in parties)
            writer.writerow(row)

    # Export to JSON
    with open('results.json', 'w') as f:
        json.dump(districts, f)

