#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Paul Sladen, 2016-03-08, Hereby placed in the Public Domain
#
# http://www.otif.org/otif/_epdf/dir_tech_adm_2006/07_2006_A_94-03_4.2006_e.pdf
# Union internationale des chemins de fer (UIC)
# Regolamento Internazionale Veicoli (RIV)
# Regolamento Internazionale Carrozze (RIC)
# European Vehicle Numbers (ENV)
# Validated against Richard Suchenwirth's 1999 Tcl solution in http://wiki.tcl.tk/607
import sys

# Doubling a digit and taking the digit sum adjusts as follows:
# 0 0   0
# 1 2  +1
# 2 4  +2
# 3 6  +3
# 4 8  +4
# 5 1  -4
# 6 3  -3
# 7 5  -2
# 8 7  -1
# 9 9   0
# Pragmatically this lookup table is: range(5)+range(-4,1)

uic_testcases = (
    '182 002-6', # DB loco
    '220 071-5',
    '21 80 155 9 084-5', # Suchenwirth example
    '21-81-2471217-3', # https://en.wikipedia.org/wiki/UIC_wagon_numbers
    '31 RIV 81 ÖBB 665 0 286-0',
    '33 RIV 70 BR 7899 047-6', # Tank wagon
    '37 TEN RIV 84 N̲L̲-GERS 4667 019-2 Sfhimmns',
    '37.84.4667.019-2', # http://www.ltsv.com/w_ref_codes_uic.php
    '51-80-0843001-0',
    '01 RIV\n83 FS\n575 0 421-8', # http://www.blainestrains.org/pdfs/RIV.pdf
    '60 80 99 26 187-7', # Wiesloch Feldbahn Wohnschlafwagen
    '82 70 GB-DBSUK 6723 675-8 Fabnooss',
    '91 53 0472 001-3', # Romanian Class 92 ex-pat: https://www.flickr.com/photos/62982979@N05/13289168904
    '93 70 3740 021–8 GB-EIL', # Eurostar e320 from Wikipedia, including endash
    'CH-FPC 62 85 78-90049-8 WLABmz', # Paris Moscow express
    # 'KT-FI Sm6 94 10 3890001-0', # breaks the rules by having 'Sm6' in middle
    'KT-FI 94 10 3890001-0', # Finnish/Russian Pendolino
    )

# Indian railways.  Related but incompatible 11-digit system.
indian_testcases = (
    # http://www.indianrailways.gov.in/railwayboard/uploads/directorate/mec_engg/downloads/freight/New_Wagon_Numb_Sys.pdf
    'BOXNHS 12 03 03 4567-9',
    'BCNAHS 31101695215',
    )

russian_testcases = (
    '2ЭВ120-002', # http://www.railwaygazette.com/news/traction-rolling-stock/single-view/view/russian-traxx-unveiled-at-engels-locomotive-plant-inauguration.html
    '3П20 012', # http://static.progressivemediagroup.com/uploads/imagelibrary/EP.jpg
    )
    

def main(identity):
    print identity.replace('\n', ' ')
    validate_uic_longform(identity)
    validate_uic_checksum(identity)

def validate_uic_checksum(uic):
    """
    Checksum UIC rolling stock number.  Short Pythonic code
    """
    d = map(int,filter(str.isdigit, uic))
    c = -sum(d[:-1] + [(range(5) + range(-4,1))[i] for i in d[-2::-2]]) % 10
    assert len(d) in (7,8,12) and c == d[-1]
    return c

def validate_uic_longform(uic):
    """
    Checksum UIC rolling stock number.  Original code
    """
    digits = [int(c) for c in uic if c.isdigit()]
    assert len(digits) in (7,8,12)
    main_digits = digits[:-1]
    multipliers = (2,1) * 6
    multipled = [a*b for a,b in zip(multipliers,reversed(main_digits))]
    big_digits = map(int,''.join(map(str,multipled)))
    big_total = sum(big_digits)
    check_digit = (-big_total) % 10
    assert check_digit == digits[-1]
    return check_digit

if __name__=='__main__':
    if not map(main, sys.argv[1:]):
        map(main, sorted(uic_testcases, key=len))
