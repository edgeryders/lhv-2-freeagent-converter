## Converts a LHV bank account statement CSV into a format that FreeAgent can process
## FreeAgent CSV format is described here: https://www.freeagent.com/support/kb/banking/file-format-for-bank-upload-csv/

from sys import version_info
from sys import exit
if version_info.major == 2:
    # We are using Python 2.x
    sys.exit ("Please refer to the cersion of the script for Python 2: https://github.com/edgeryders/lhv-2-freeagent-converter")
# We are using Python 3.
import tkinter
import csv
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
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


tkinter.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
directory = askdirectory(title = "Choose a directory") # shows a "choose directory" dialog box
outFilename = directory + '/Transactions_from_LHV.csv'

outList = [] # initialize the dictionary where to store the output
nonEURrows = [] # a list of raw non-EUR payments
nonEURcurrencies = [] # a list of non-EUR currencies encountered

with open (filename) as csvfile: # this part generates the list for the main EUR CSV file
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Currency'] == 'EUR':
            outListItem = {} # each item in the list is a dict
            formattedDate = row['Date'][8:] + row['Date'][4:8] + row['Date'][:4]
            outListItem['Date'] = formattedDate
            amount = str(row['Amount'])
            outListItem['Amount'] = amount
            formattedDescription = row['Description'] + ' Sender/receiver: ' + row['Sender/receiver name'] + ' ' + row['Sender/receiver account']
            outListItem['Description'] = formattedDescription
            outList.append(outListItem)
        else: # this part provides for the non-EUR transaction files
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


# save outList (the main list with only EUR transactions) as a CSV file. I cannot use dictWriter because FreeAgent wants a specific order for columns.with open (outFilename, 'w') as outFile:
    for item in outList:
##        oneRow = str(item ['Date']) + ', ' + str(Decimal(item ['Amount']).quantize(Decimal('.01'))) + ', ' + item ['Description'] + '\n'
        oneRow = str(item ['Date']) + ', ' + item['Amount'] + ', ' + item ['Description'].replace(',', '') + '\n'
        outFile.write(oneRow)
    
    

        


