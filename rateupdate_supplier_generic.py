## WHAT: Generic Supplier Rate Deck Update. See repo https://github.com/Johst/RateParse.git
## INPUT: A supplier "new_file" xlsx file with new rates, a "current_file" supplier rate file downloaded from system
## OUTPUT: a new re-named "current_file" for re-upload to system
## Target supplier for development = Deutsche Telekom

## File logistics ##
# Files folder: C:\Users\johastje\Desktop\PythonPlay\Costlists\generic_supplier
# Code module: C:\Users\johastje\Desktop\PythonPlay\Costlists\generic_supplier\rateupdate_supplier_generic.py
# Code execution: C:/Users/johastje/AppData/Local/Programs/Python/Python36/python.exe C:\Users\johastje\Desktop\PythonPlay\Costlists\generic_supplier\rateupdate_supplier_generic.py

## Cooding priority ##
# Frequent update senders: Deutsche Telekom (2-3 times per week), CLX (daily) 
# Most complex format senders: Telenor (monthly)

## Functions ##
# (Done) create_dict_from_new(new_cost_file) - creates dict with new rates from supplier file
# (Done) create_dict_from_system(system_current) - creates dict with current rates from system file
# (Not Done) update_system_file(new_rates_dict) - Create new system file for upload with new rates
# (Not Done) compare_new_current_dict(new_dict, current_dict) - compares current and new rate decks

import openpyxl, pprint, csv
from openpyxl import load_workbook

def create_dict_from_new(new_cost_file):
    """ Create a dict with new prices derived from the new cost list from [xxx] supplier with its unique format.
    WHAT: Convert supplier Excel file to a dictinary with mccmnc-rate value pairs
    ARGS: Supplier new costlist file
    RETURN: new MCCMNC:rate dict
    """
    ## Dev status: 
    # 2019-11-14 Done and tested!

    ## Data positions in file:
    supplier_name_pos = 'Deutsche Telekom AG' # Manual if not file pos [col, row] can be set
    account_product = '' # # Manual if not file pos [col, row] can be set
    validity_date_col = 4 #Column for "valid date" value 
    #validity_date_pos = [x, y] # Read from a specific file position if not on every network row
    currency_pos = 'EUR' # Manual if not file pos [col, row] can be set
    data_start_row = 19 # First row of network data
    mccmnc_col = 3 # Column for concatenated mccmnc value 
    rate_col = 5 # Column for concatenated rate value 
    change_status_col = 6 # Column "Increase", "Decrease", "Unchanged" value
    fx_conversion = 100 # Conversion multiplication value for FX is "1", "100" 
                        # or "0.01". I.e if supplier rate is in EUR it has to be 
                        # mulitplied by 100 to become EURO cent as in system.
    rate_decimal_type = ',' # If ',' (comma), replace to '.' (dot) as system file 
                            # requires it. IGNORE coding it for now, seems Python takes care of it.                    

    # Define dict that will hold all new MCCMNC-RATE value pairs
    new_rates = {} 
   
    # Open supplier excel file and add key-value pairs to dict
    try:
        wb = openpyxl.load_workbook(new_cost_file, data_only=True)
        sheet = wb['Price List']
        print('Sheet max rows: %s and file path %s' % (sheet.max_row, new_cost_file))
        cnt = 0
        for rowNum in range(data_start_row, sheet.max_row +1): # skip headers, data starts on row 6
            mccmnc = sheet.cell(row=rowNum, column=mccmnc_col).value # Set column for mccmnc
            current_rate = sheet.cell(row=rowNum, column=rate_col).value # Set column for current_rate
            validity_date = sheet.cell(row=rowNum, column=validity_date_col).value # Assuming its the same and given (not blank cell) for all networks
            change_status = sheet.cell(row=rowNum, column=change_status_col).value # Unique per network
            new_rates[mccmnc] = current_rate * fx_conversion
            #new_rates[mccmnc] = str(int(current_rate) * fx_conversion) # Convert to Euro cent (requires dot instead of comma for rate)
            cnt += 1
        wb.close()
        
        #pprint.pprint(new_rates)
        print('Supplier:', supplier_name_pos)
        print ('Max rows in file: ', sheet.max_row)
        print('Count of rows iterated:', cnt)
        print('Network list lenght:', str(len(new_rates)))
        print('Currency in file:', currency_pos)
        print('Validity date:', validity_date)
       
        return new_rates
     
    except Exception as e: print('An error occured in function create_dict_from_new(): ' + str(e)) 

def create_dict_from_system(system_current):
    """ Create a dict with current rates derived from the downloaded system ratedeck of supplier in CSV format.
    ARGS: system current ratedeck in CSV format
    RETURN: dict with MCCMNC-RATE value pairs of new pricing
    """
    ## Dev status: 
    # 2019-11-14 Done and tested!

    # Open and read current system CSV file
    try:
        rates_current_dict={} # dict that will hold all current MCCMNC prices for supplier
        print('Loading cost file...')
        with open(system_current) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            ratelist = list(reader)
            print('Creating cost dictionary...')
            cnt = 0
            for i in range(1, len(ratelist)): # skip header row
                mccmnc = ratelist[i][6] + ratelist[i][7] 
                (key, val) = mccmnc, ratelist[i][8] 
                rates_current_dict[str(key)] = val
                cnt +=1
        #pprint.pprint(rates_current_dict)
        print('Number of networks processed: ', cnt)
        print ('Number of networks in list: ', str(len(rates_current_dict)))
        print ('Number of networks with MCC = 0 and MNC = na and default rate = 2.0 EURC: ', str(cnt-len(rates_current_dict)))
        return rates_current_dict

    except Exception as e: print('An error occured in function create_dict_from_system(): ' + str(e))   

def create_new_system_file(system_current, supplier_new, outputfile):
    """
    Takes an EBSS supplier rate deck CSV file and updates all new rates (only) based on MCCMNC identifier from new_rates dict
    created by function create_dict_from_new()
    PARAM: a downloaded suppliler rate deck from system, supplier_new file (dict creatation will be made by funcation call inside)
    RETURN: a system uploadble rate deck with new_rates added (only new rates will be updated and only for existing MCCMNC)
    """
    ## Dev status: 
    # 2019-11-14 Tested and works. But how to handle added reach in new_file that doesn't exist in current_file?
    # For example 41288 is added in new rate deck but doesn't exist in current_file (or system as network id).
    # Answer. Ignore networks not in the current_file. Write the added network to log for later implementaion 
    # in system. 
    
    # Open current_file for read and create a new_file for write
    try:
        # open input file and add each data row to a list
        print('Reading old cost file...')
        with open(system_current) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            ratelist = list(reader)

        # Call function to get new_rates dict 
        new_rates =  create_dict_from_new(supplier_new)               
          
        # Create result file for read
        resultFile = open(outputfile, 'w')
        print('Updating costs...')
        # Loop through and write new rates to file
        for i in range(0, len(ratelist) ):
            mccmnc = ratelist[i][6] + ratelist[i][7]  # join mcc and mnc for dict lookup
            if mccmnc in new_rates:
                ratelist[i][8] = new_rates[mccmnc]
            
            # Write data to new file, make it semi colon separated
            resultFile.write(
                ratelist[i][0] + ';' + # region
                ratelist[i][1] + ';' + # country
                str(ratelist[i][2]) + ';' + # op id
                ratelist[i][3] + ';' + # operator
                ratelist[i][4] + ';' + # network
                ratelist[i][5] + ';' + # unique name
                str(ratelist[i][6]) + ';' + # MCC
                str(ratelist[i][7]) + ';' + # MNC
                str(ratelist[i][8]) + '\n') # rate  
           
        print('Writing to the new file...')
        print('Networks processed:', i)
        print('Rates updated: ', str(len(new_rates)))
        print('Path to new file for upload to EBSS:', outputfile)
        resultFile.close()         
    except Exception as e: print('An error occured in function create_new_system_file(): ' + str(e))                      

## MAIN ##

# File logistics:

## Downloaded from system to drive folder
system_current = "C:\\Users\\johastje\\Desktop\\PythonPlay\\Costlists\\generic_supplier\\EBSS\\2019-11-18 price_list_DEUT.csv"
## New file received from supplier
supplier_new = "C:\\Users\\johastje\\Desktop\\PythonPlay\\Costlists\\\\generic_supplier\\Deutsche Telekom AG\\2019-11-12 priceList [dtagtele2554][A-Z].xlsx"

# Path to result file for upload back to system
outputfile = "C:\\Users\\johastje\\Desktop\\PythonPlay\\Costlists\\generic_supplier\\Results\\new_system_file.csv"

## Create new rate dict
#create_dict_from_new(supplier_new)
## Create current rate dict
#create_dict_from_system(system_current)

## Create new system file
create_new_system_file(system_current, supplier_new, outputfile)
