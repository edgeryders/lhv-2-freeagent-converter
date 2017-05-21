## Converts a LHV bank account statement CSV into a format that FreeAgent can process
## FreeAgent CSV format is described here: https://www.freeagent.com/support/kb/banking/file-format-for-bank-upload-csv/

import csv
from Tkinter import Tk
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from decimal import *

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

outList = [] # initialize the dictionary where to store the output

with open (filename) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        outListItem = {} # each item in the list is a dict
        formattedDate = row['Date'][8:] + row['Date'][4:8] + row['Date'][:4]
        outListItem['Date'] = formattedDate
        if row['Debit/Credit (D/C)'] == "C":
            formattedAmount = round(float(row['Amount']), 2)
        else:
            formattedAmount = -1 * (round(float(row['Amount']), 2))
        outListItem['Amount'] = formattedAmount
        formattedDescription = row['Description'] + ' Sender/receiver: ' + row['Sender/receiver name'] + ' ' + row['Sender/receiver account']
        outListItem['Description'] = formattedDescription
        outList.append(outListItem)

# save outDict as a CSV file. I cannot use dictWriter because FreeAgent wants a specific order for columns.

directory = askdirectory(message = "Choose a directory")
outFilename = directory + '/Transactions_from_LHV.csv'

with open (outFilename, 'w') as outFile:
    for item in outList:
        oneRow = str(item ['Date']) + ', ' + str(Decimal(item ['Amount']).quantize(Decimal('.01'))) + ', ' + item ['Description']
        outFile.write(oneRow)
    
    

        


