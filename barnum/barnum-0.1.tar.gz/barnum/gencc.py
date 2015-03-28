"""
gencc: A simple program to generate credit card numbers that pass the MOD 10 check
(Luhn formula).
Usefull for testing e-commerce sites during development.

Copyright 2003 Graham King

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""
from __future__ import print_function
import random
import sys
import copy

visaPrefixList = [ 	['4', '5', '3', '9'], 
                    ['4', '5', '5', '6'], 
                    ['4', '9', '1', '6'],
                    ['4', '5', '3', '2'], 
                    ['4', '9', '2', '9'],
                    ['4', '0', '2', '4', '0', '0', '7', '1'],
                    ['4', '4', '8', '6'],
                    ['4', '7', '1', '6'],
                    ['4'] ]
mastercardPrefixList = [    ['5', '1'],
                            ['5', '2'],
                            ['5', '3'],
                            ['5', '4'],
                            ['5', '5'] ]
amexPrefixList = [  ['3', '4'],
                    ['3', '7'] ]
discoverPrefixList = [ ['6', '0', '1', '1'] ]
dinersPrefixList = [    ['3', '0', '0'],
                        ['3', '0', '1'],
                        ['3', '0', '2'],
                        ['3', '0', '3'],
                        ['3', '6'],
                        ['3', '8'] ]
enRoutePrefixList = [   ['2', '0', '1', '4'],
                        ['2', '1', '4', '9'] ]
jcbPrefixList16 = [   ['3', '0', '8', '8'],
                    ['3', '0', '9', '6'],
                    ['3', '1', '1', '2'],
                    ['3', '1', '5', '8'],
                    ['3', '3', '3', '7'],
                    ['3', '5', '2', '8'] ]
jcbPrefixList15 = [ ['2', '1', '0', '0'],
                    ['1', '8', '0', '0'] ]
voyagerPrefixList = [ ['8', '6', '9', '9'] ]                    


def completed_number(prefix, length):
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically 13 or 16
    """
    ccnumber = prefix
    # generate digits
    while len(ccnumber) < (length - 1):
        digit = random.choice(['0',  '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        ccnumber.append(digit)
    # Calculate sum 
    sum = 0
    pos = 0
    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()
    while pos < length - 1:
        odd = int( reversedCCnumber[pos] ) * 2
        if odd > 9:
            odd -= 9
        sum += odd
        if pos != (length - 2):
            sum += int( reversedCCnumber[pos+1] )
        pos += 2
    # Calculate check digit
    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10
    ccnumber.append( str(int(checkdigit)) )
    return ''.join(ccnumber)

def credit_card_number(prefixList, length, howMany):
    result = []
    for i in range(howMany):
        ccnumber = copy.copy( random.choice(prefixList) )
        result.append( completed_number(ccnumber, length) )
    return result

def output(title, numbers):
    result = []
    result.append(title)
    result.append( '-' * len(title) )
    result.append( '\n'.join(numbers) )
    result.append( '' )
    return '\n'.join(result)

if __name__ == "__main__":
    mastercard = credit_card_number(mastercardPrefixList, 16, 10)
    print(output("Mastercard", mastercard))
    visa16 = credit_card_number(visaPrefixList, 16, 10)
    print(output("VISA 16 digit", visa16))
    visa13 = credit_card_number(visaPrefixList, 13, 5)
    print(output("VISA 13 digit", visa13))
    amex = credit_card_number(amexPrefixList, 15, 5)
    print(output("American Express", amex))
    # Minor cards
    discover = credit_card_number(discoverPrefixList, 16, 3)
    print(output("Discover", discover))
    diners = credit_card_number(dinersPrefixList, 14, 3)
    print(output("Diners Club / Carte Blanche", diners))
    enRoute = credit_card_number(enRoutePrefixList, 15, 3)
    print(output("enRoute", enRoute))
    jcb15 = credit_card_number(jcbPrefixList15, 15, 3)
    print(output("JCB 15 digit", jcb15))
    jcb16 = credit_card_number(jcbPrefixList16, 16, 3)
    print(output("JCB 16 digit", jcb16))
    voyager = credit_card_number(voyagerPrefixList, 15, 3)
    print(output("Voyager", voyager))

