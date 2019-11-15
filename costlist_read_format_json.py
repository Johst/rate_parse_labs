## read a costlist json file, edit and save changes back

# C:/Users/johastje/AppData/Local/Programs/Python/Python36/python.exe C:\Users\johastje\Desktop\PythonPlay\Costlists\costlist_format_dev\read_costlist_format.py

import json

# Retrieve data from json file
jsonfilename = "C:\\Users\\johastje\\Desktop\\PythonPlay\\Costlists\\costlist_format_dev\\universal_costlist_format3.json"
try:
    with open (jsonfilename) as fo:
        costlist = json.load(fo)
        
        #Do somthing with the list
        print( costlist['telenor'] ) # print all "telenor" data
        print( costlist['telenor']['networks'][0] ) # print first network in "telenor" list

        # print telenor number of networks
        print('Number of networks for Telenor: ', len( costlist['telenor']['networks']) )

        # Print all key and values in telenor first network
        for key, value in costlist['telenor']['networks'][0].items():
            print (key, ':', value )
        #print(costlist['networks'][])

except Exception as e: print('An error occured: ' + str(e))     

