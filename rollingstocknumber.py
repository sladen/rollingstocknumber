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

uic_testcases = (
    '000-000-0', # Pathological cases
    #'111-111-1', '222-222-2', '333-333-3', '444-444-4',
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
    'KT-FI Sm6 94 10 3890001-0', # Finnish/Russian Pendolino 'Sm6' prefix requires truncation
    )

# Indian railways.  Related but incompatible 11-digit system.
indian_testcases = (
    # http://www.indianrailways.gov.in/railwayboard/uploads/directorate/mec_engg/downloads/freight/New_Wagon_Numb_Sys.pdf
    'BOXNHS 12 03 03 4567-9',
    'BCNAHS 31101695215',
    )

# Russian/former CIS numbering examples
russian_testcases = (
    '2ЭВ120-002', # http://www.railwaygazette.com/news/traction-rolling-stock/single-view/view/russian-traxx-unveiled-at-engels-locomotive-plant-inauguration.html
    '3П20 012', # http://static.progressivemediagroup.com/uploads/imagelibrary/EP.jpg
    )

# Australian numbering examples
australian_testcases = (
    'AMOX18S', # http://www.rissb.com.au/wp-content/uploads/2014/08/Sect-23-CLASSIFICATION-AND-NUMBERING1.pdf
    )

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

def validate_uic_checksum(uic, validate_length=True, validate_checksum=True):
    """Validate and return checksum digit from a UIC/RIV/RIC/ENV rolling stock number.

    Args:
        uic (str): rolling stuck number as string, can include UIC letters/punctuation
    Kwargs:
        validate_length (bool): validate digit count (default: True)
        validate_checksum (bool): validate checksum (default: True)
    Returns:
        checksum digit `c` as integer between 0 and 9
    Raises:
        IndexError: incorrect number of digits supplied (if validate_length)
        ValueError: mismatching checksum detected (if validate_checksum)

    Can be used to calculate a checksum from scratch by passing an additional digit
    and explicitly turning off the normal validation step:

    >>> validate_uic_checksum('123-456' + '0', validate_checksum=False)
    6

    Because zero is a validate checksum digit, avoid comparing for success:
    >>> if validate_uic_checksum('000-000-0'): # Incorrect 10% of the time

    Implementation:
    Digits `d` are maximum of twelve numbers, extracted from righthand side.
    Check sum `c` of digits with alterate numbers multipled by two,
        subtracted from next multiple of ten.
    """
    assert isinstance(uic, str)

    d = map(int, filter(str.isdigit, uic))[-12:]
    c = -sum(d[:-1] + [(range(5) + range(-4,1))[i] for i in d[-2::-2]]) % 10

    if validate_length and not len(d) in (7,8,12):
        raise IndexError('Invalid number of digits in "%s", found "%s" (%d digits)' % (uic, ''.join(map(str,d)), len(d)))
    if validate_checksum and not c is d[-1]:
        raise ValueError('Invalid checksum "%s", found digits %s, calculated checksum %d?' % (uic, ''.join(map(str,d)), c))
    return c

def validate_uic_longform(uic):
    """
    Checksum UIC rolling stock number.  Original code
    """
    assert isinstance(uic, str)
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

def main(identity):
    """Run each test, printing checksum and input UIC number if succesful"""
    try:
        checksum = validate_uic_checksum(identity)
    except: raise
    else: print checksum, ':', identity.replace('\n', ' ')

if __name__=='__main__':
    if not map(main, sys.argv[1:]):
        map(main, sorted(uic_testcases, key=len))
