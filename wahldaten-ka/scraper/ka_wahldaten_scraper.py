#!/usr/bin/env python
# encoding: utf-8

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


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


if __name__ == '__main__':

    try:
        # Python 2
        from urllib import urlopen
    except ImportError:
        # Python 3
        from urllib.request import urlopen

    from bs4 import BeautifulSoup

    URL = 'http://web3.karlsruhe.de/Stadtentwicklung/afsta/Wahlen/Wahlabend-Netmodul/2013-btw/erst/bundestag-2013-erst-wbz.php'

    html = urlopen(URL).read()
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    assert len(tables) == 2
    data = extract_table(tables[1])

    header = data[0]
    direct_candidates = header[5:]
    districts = {}
    for row in data[1:]:
        district_num = fix_district_number(row[0])
        district = {
            #'Wahlkreisnummer': 271,
            #'Wahlkreisname': 'Karlsruhe-Stadt',
            #'Stadtteilnummer': 'FIXME',
            #'Stadtteilname:': 'FIXME',
            'Wahlbezirksnummer': district_num,
            'Wahlbezirksname': row[1],
            'Wahlberechtigte insgesamt': parse_german_number(row[2]),
            'Wähler/-innen': parse_german_number(row[3]),
            'Wahlbeteiligung': parse_german_number(row[4].rstrip('%')),
        }
        # Extract votes for each candidate
        valid_votes = 0
        for cell, candidate in zip(row[5:], direct_candidates):
            parts = cell.split()
            votes = parse_german_number(parts[0])
            district[candidate] = votes
            valid_votes += votes
        district['Gültige Erststimmen'] = valid_votes

        districts[district_num] = district

    from pprint import pprint
    pprint(districts)

