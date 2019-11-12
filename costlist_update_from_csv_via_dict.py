import csv, time
# C:/Users/johastje/AppData/Local/Programs/Python/Python36/python.exe C:\Users\johastje\Desktop\PythonPlay\Costlists\costlist_update.py

### DESCRIPTION ###
# One way of updating a supplier costlist specifically for EBSS is to just go off of the network id
# (EBSS has a newworkId as identifier instead of the MCCMNC) and update with the new prices 
# stored from a pre stored dictionary.


# General steps:
# 1. Download the current supplier costlist from EBSS to ensure correct format for re upload.
# 2. Create a copy of it. We will later update the prices and re upload to EBSS.
# 3. Go through the new costlist (this may reqiure pre-parse) and build a dictinonary holding MCCMNC 
# and price like {'24001':0.25,'23402':0.46}.
# 4. Loop through the new copy, created in pt2, of the costfile and update/overwrite prices identified by the MCCMNC value.
# 5. Upload the newly created file to EBSS.

# Pre-parsing: 
# Some cost lists will require pre parsing before a dictionary can be created from it. Typically 
# the pre parsing needed is to seprate grouped MNC's to one row for each mnc,  merge MCC and MNC 
# to one column and to replance cost decimal with a dot instead of a comma. 

# Another way, long term better maybe, is to define a universal costlist format in json (see file universal_costlist_format.json) 
# and then parse all supplier files into this format before any calculation of analysis is made to it. 
# Finally it would be parsed into the format that EBSS accepts by "dowload-edit-upload" to EBSS as main change procedure. 


### Supplier Costlist Parsing ###
# These functions handles suppplier cost list updates both dealing with files coming
# from suppliers and the EBSS format for cost. EBSS only accept the ecact format of its
# own cost list so the procedure is to download the current costlist supplier file and 
# update it with the data from the new supplier file sent to us. Finally we uploead
# the updated EBSS file back to the system. 
# For additional parse code the file_analysis class file

def csvcostupdateDict(newcostfile):
    
    """ Loads dict with updated prices from a csv price file or manual
    PARAM: Supplier cost file with new costs per destination
    RETURN: dict with {MCCMNC:COST} 
    USAGE: The is used to update the downloaded current supplier EBSS file for re upload back. 
    
    """

    # inputfile = "C:\\Users\\johastje\\Desktop\\PythonPlay\\Costlists\\costlist_simple.csv"
    # Region;Country;Op Id;Operator Name;Network Name;Unique Name;MCC;MNC;Price(EUR cent)
    # Asia Pacific;Afghanistan;1626;Afghan Telecom;Salaam;Salaam-AF;412;80;2.00
    
    # Create a dict with MCCMNC rates to be updated
    # cost_updates = {'27601':'13.07','41280':'41.19','60302':'51.27'}

    #TODO: create the dictionary from file input. 
    # 1. read input file 
    # 2. grab and add data pairs to dict from MCCMNC and rate/cost column
    # Assumptions:
    # Separator ; 
    # MCC in col 6 and MNC in col 7
    # Rates in col 8

    costDict = {}
    print('Loading cost file...')
    with open(newcostfile) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        ratelist = list(reader)
        print('Creating cost dictionary...')
        for i in range(1,len(ratelist)): # skip header row
            mccmnc = ratelist[i][0] + ratelist[i][1] 
            (key, val) = mccmnc, ratelist[i][2] 
            costDict[str(key)] = val
    print('Passing dictionary to function requesting it...')
    print('Printing cost dict below'+ '\n')
    print(costDict)
    return costDict                

def updateCostlist():
    """
    Takes an EBSS supplier costlist MS Excel download and updates all costs based on MCCMNC identifier
    PARAM: a EBSS CSV  Costlist downloaded from EBSS
    RETURN: a EBSS CSV Costlist for upload to EBSS
    """
    
    # TODO.TXT
    # 1. dwnld current file from EBSS
    # 2 prepare the new supplier file (Region;Country;Op Id;Operator Name;Network Name;Unique Name;MCC;MNC;Price(EUR cent))
    # 3. run script
    # 4 upload the new file

    oldcostfile = "C:\\Users\\johastje\\Desktop\\PythonPlay\\Costlists\\ebss_costlist_old.csv" # dwnld from EBBS
    newcostfile = "C:\\Users\\johastje\\Desktop\\PythonPlay\\Costlists\\supplier_costlis_new2.csv" # Provided by Supplier
    outputfile = "C:\\Users\\johastje\\Desktop\\PythonPlay\\Costlists\\costlist_simple_result.csv" # result for upload to EBSS
    try:
        # open input file and add each data row to a list
        print('Reading old cost file...')
        with open(oldcostfile) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            ratelist = list(reader)

        # Call function with cost updates and add to dictionary
        COST_UPDATES =  csvcostupdateDict(newcostfile)               
        
        # TODO: Loop through the rows and update the prices.
        # Skip header
        # Read value in mccmnc column, or join if mcc and mnc are seprarated
        # If
        
        resultFile = open(outputfile, 'w')
        print('Updating costs...')
        for i in range(0,len(ratelist)):
            mccmnc = ratelist[i][6] + ratelist[i][7]  # join mcc and mnc for dict lookup
            if mccmnc in COST_UPDATES:
                ratelist[i][8] = COST_UPDATES[mccmnc]
            resultFile.write(
                ratelist[i][0] + ',' +
                ratelist[i][1] + ',' +
                ratelist[i][2] + ',' +
                ratelist[i][3] + ',' +
                ratelist[i][4] + ',' +
                ratelist[i][5] + ',' +
                ratelist[i][6] + ',' +
                ratelist[i][7] + ',' +
                ratelist[i][8] + '\n')   
           
        print('Writing to the new file...')
        print('Networks processed:', i)
        print('Rates updated:', len(COST_UPDATES))
        print('Path to new file for upload to EBSS:', outputfile)
        logg('Costs updated at' + str(outputfile))
        resultFile.close()         
    except Exception as e: 
        print('An error occured: ' + str(e))
        logg(str(e))   

def logg(msg):
    """Loggs data str to file """
    filePath = "C:\\Users\\johastje\\Desktop\\PythonPlay\\logg.txt" 
    ts = time.gmtime()
    try:
        f = open(filePath, "a")
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", ts) + ',' + msg + '\n')
        f.close()
    except Exception as e: print('An error occured: ' + str(e))    
    print('Operation logged with message length:', len(msg))     

# main
print('Staring operation...')
updateCostlist()
print('Operation complete.')
