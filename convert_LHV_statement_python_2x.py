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
    for row in transactions:
        outListItem = {} # each item in the list is a dict
        if row['Currency'] == currency:
            outListItem['Date'] = row['Date']
            outListItem['Amount'] = row['Amount']
            outListItem['Description'] = row['Description']
            outListCurrency.append(outListItem)
    return outListCurrency
 

tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
directory = askdirectory(title = "Choose a directory") # shows a "choose directory" dialog box

outList = [] # initialize the list where to store the output
currencies = [] # a list of non-EUR currencies encountered

with open (filename) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        outListItem = {} # each item in the list is a dict
        formattedDate = row['Date'][8:] + row['Date'][4:8] + row['Date'][:4]
        outListItem['Date'] = formattedDate
        amount = str(row['Amount'])
        outListItem['Amount'] = amount
        formattedDescription = row['Description'] + ' Sender/receiver: ' + row['Sender/receiver name'] + ' ' + row['Sender/receiver account']
        outListItem['Description'] = formattedDescription
        outListItem['Currency'] = row['Currency']
        outList.append(outListItem)
        curr = row['Currency']
        if curr not in currencies:
            currencies.append(curr)
        
for currency in currencies:
    outFilename = directory + '/transactions_in_' + currency + '.csv'
    rows_to_file = generate_report(currency, outList)
    with open (outFilename, 'w') as outFile:
        for item in rows_to_file:
            oneRow = str(item ['Date']) + ', ' + item['Amount'] + ', ' + item ['Description'].replace(',', '') + '\n'
            outFile.write(oneRow)
            
    

        


