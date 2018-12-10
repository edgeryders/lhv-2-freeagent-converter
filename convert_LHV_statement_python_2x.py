## Converts a LHV bank account statement CSV into a format that FreeAgent can process
## FreeAgent CSV format is described here: https://www.freeagent.com/support/kb/banking/file-format-for-bank-upload-csv/

from sys import version_info
if version_info.major == 2: # we are using Python 2.x
    import tkinter as tk
else: 
    sys.exit ("Please refer to the version of the script for Python 3: https://github.com/edgeryders/lhv-2-freeagent-converter")

import csv
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from decimal import *

def generate_report(currency, transactions):
    '''
    (str) => list of dict
    For each non-EUR currency present in the transactions statement, generate a separate 
    list of transaction. Later to be saved into a CSV file
    '''
    ## iterate on nonEURrows to find the transaction in that currency
    outListCurrency = []
    for transaction in transactions:
        if transaction['Currency'] == currency:
            outListItem = {} # each item in the list is a dict
            formattedDate = row['Date'][8:] + row['Date'][4:8] + row['Date'][:4]
            outListItem['Date'] = formattedDate
            amount = str(row['Amount'])
            outListItem['Amount'] = amount
            formattedDescription = row['Description'] + ' Sender/receiver: ' + row['Sender/receiver name'] + ' ' + row['Sender/receiver account']
            outListItem['Description'] = formattedDescription
            outListCurrency.append(outListItem)
    return outListCurrency
            
    
    
  

tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
directory = askdirectory(title = "Choose a directory") # shows a "choose directory" dialog box
outFilename = directory + '/Transactions_from_LHV.csv'

outList = [] # initialize the list where to store the output
nonEURrows = [] # a list of raw non-EUR payments
nonEURcurrencies = [] # a list of non-EUR currencies encountered

with open (filename) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Currency'] == 'EUR':
            outListItem = {} # each item in the list is a dict
            formattedDate = row['Date'][8:] + row['Date'][4:8] + row['Date'][:4]
            outListItem['Date'] = formattedDate
            amount = str(row['Amount'])
            outListItem['Amount'] = amount
##        if row['Debit/Credit (D/C)'] == "C":
##            formattedAmount = round(float(row['Amount']), 2)
##        else:
##            formattedAmount = -1 * (round(float(row['Amount']), 2))
##        outListItem['Amount'] = formattedAmount
            formattedDescription = row['Description'] + ' Sender/receiver: ' + row['Sender/receiver name'] + ' ' + row['Sender/receiver account']
            outListItem['Description'] = formattedDescription
            outList.append(outListItem)
        else:
            nonEURrows.append(row)
            nonEURcurrencies.append(row['Currency'])

    if len(nonEURcurrencies) > 0: # we have encountered at least one non-EUR currency
        for currency in nonEURcurrencies:
            outFilenameCurrency = directory + '/transactions_in_' + currency + '.csv'
            rows_to_file = generate_report(currency, nonEURrows)
            with open (outFilenameCurrency, 'w') as outFile:
                for item in rows_to_file:
            ##        oneRow = str(item ['Date']) + ', ' + str(Decimal(item ['Amount']).quantize(Decimal('.01'))) + ', ' + item ['Description'] + '\n'
                    oneRow = str(item ['Date']) + ', ' + item['Amount'] + ', ' + item ['Description'].replace(',', '') + '\n'
                    outFile.write(oneRow)
            


# save outList (the main list with only EUR transactions) as a CSV file. I cannot use dictWriter because FreeAgent wants a specific order for columns.

with open (outFilename, 'w') as outFile:
    for item in outList:
##        oneRow = str(item ['Date']) + ', ' + str(Decimal(item ['Amount']).quantize(Decimal('.01'))) + ', ' + item ['Description'] + '\n'
        oneRow = str(item ['Date']) + ', ' + item['Amount'] + ', ' + item ['Description'].replace(',', '') + '\n'
        outFile.write(oneRow)
    
    

        


