## Converts a LHV bank account statement CSV into a format that FreeAgent can process
## FreeAgent CSV format is described here: https://www.freeagent.com/support/kb/banking/file-format-for-bank-upload-csv/

import sys
if sys.version_info.major == 2:
    # We are using Python 2.x
    sys.exit ("Please refer to the version of the script for Python 2: https://github.com/edgeryders/lhv-2-freeagent-converter")
# We are using Python 3.
import tkinter
import csv
from datetime import datetime
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from decimal import *

def generate_report(currency, transactions):
    '''
    THIS ONE I AM NOT GOING TO NEED IN THE CASE OF OPERATIONS IN A SINGLE CURRENCY
    (str, list of dicts) => list of dict
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


root = tkinter.Tk() # as per https://stackoverflow.com/questions/32217114/tkinter-askopenfilename-wont-close
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
directory = askdirectory(title = "Choose a directory") # shows a "choose directory" dialog box
root.update()

# print(sys.version)

outList = [] # initialize the list where to store the output

with open (filename, 'r', encoding="utf-8-sig") as csvfile: # encoding is necessary to avoid Unicode error in python 3
    # see: https://stackoverflow.com/questions/5004687/python-csv-dictreader-with-utf-8-data
    fieldnames = ['date', 'myaccount', 'amount', 'otheraccount', 'bank', 'name', 'address', 'code', 'info', 'balance']
    reader = csv.DictReader(csvfile, fieldnames = fieldnames)
    for row in reader:
        outListItem = {} # each item in the list is a dict
        formattedDate = row['date'].replace('-','/')
        outListItem['Date'] = formattedDate
        amount = str(row['amount']).replace('.','') # Triodos uses ',' for decimals, '.' for thousands. FreeAgent wants '.' for decimals and no thousands.
        amount = amount.replace(',', '.')
        outListItem['Amount'] = amount
        formattedDescription = row['info'] + ' Sender/receiver: ' + row['name']
        outListItem['Description'] = formattedDescription
        outListItem['Currency'] = 'EUR' # this account is Euro only
        outList.append(outListItem)

outFilename = directory + '/transactions as of ' + str(datetime.today().strftime('%Y-%m-%d')) + '.csv'
print(outFilename)
with open (outFilename, 'w', encoding='UTF-8') as outFile:
    for item in outList:
        oneRow = str(item ['Date']) + ', ' + item['Amount'] + ', ' + item ['Description'].replace(',', '') + '\n'
        outFile.write(oneRow)
