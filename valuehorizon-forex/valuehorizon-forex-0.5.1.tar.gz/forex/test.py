from lxml import objectify
import pandas as pd

path = 'table_a1.xml'
xml = objectify.parse(open(path))

field_names = ['CountryName', 'CurrencyName', 'CurrencySymbol', 'CurrencyNumber', 'CurrencyUnits']

df = pd.DataFrame(columns=('CountryName', 'CurrencyName', 'CurrencySymbol', 'CurrencyNumber', 'CurrencyUnits'))

for currency_row in root.getchildren()[0].getchildren():
    obj = currency_row.getchildren()
    if len(obj) == len(field_names):
	    row = dict(zip(field_names, [item.text for item in obj]))
	    row_s = pd.Series(row)
	    row_s.name = i
	    df = df.append(row_s)

