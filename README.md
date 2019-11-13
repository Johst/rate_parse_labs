# Rate Deck Parsing
There are several strategies for how to approach this depending on the number of accounts and frequency you have to handle. 

**WHAT:** Automate parsing of supplier rate decks, i.e. find the data you need in the files and convert it to a format that your system accepts to upload. The assumptions is that the cost lists from suppliers are sent as email attachments in either CSV or any kind of spreadsheet format like xlsx. 

**WHY:** This process is highly manual today, taking a lot of manual work labor efforts with high risk of mistakes that can lead to margin loss due to error in cost or price list management. Changes that needs attention can also happen outside of office hours or other times when staff is not available for manual handling of update. 

**HOW:**
There are a number of approcahes: 

1. For each supplier, create a code snippet that takes the new cost file as input, parse it and write a new cost file for upload in the format that your system requires. Fast, easy but not scalable...works when you have few suppliers. For example you can create an input dict from the new file and one dict for the old file. Then use the new dicts to just update the old dict and write back to cost file. 

2. Create an in data processor that parse's the file into an internal calaculation/storage JSON format (for example), and then via an out data processor convert it to the specified routing system format. This solution can also include GUI for file logistics (user to set input and output file etc). 

3. Outsource the whole shabang to a 3rd party like IX Links. This will cost you approxematly a CAPEX and then OPEX of about 100 USD per account and month. Then the 3rd party will take over all your communication with the 3rd party and ensure that they dleivery the costlist in the correct format and at the right time, ie ensure that everything techncial and legally agreed is being honored. 


# Verify Script #

Open file `costlist_update_from_csv_via_dict.py`. use files `ebss_costlist_old.csv` and `supplier_costlis_new2.csv` as input and the result will end up as file `costlist_simple_result.csv` The file paths has to be set in the code as you wish them to be. 

# Design & TODO For Option 2 # 

1. Read new costs from `new_cost_file ` CSV/XLSX into a ` new_dict ` with MCCMNC and COST. 
2. Then download and read the `current_file ` supplier costlist CSV/XLSX from routing system and put data into a ` current_dict ` with MCCMNC and COST. 
3. Create a function to compare dicts for stats display in html format. Number of networks updated, old new price diff, added reach. 
4. If added reach is discovered, it needs to be flagged to operator so the new newtwork(s) can be added to current supplier cost list in system and a new system `current_file ` then needs to be re downloaded when this is done. 
4. Loop through the `current_file `and replace each cost with matching MCCMNC from the ` new_dict `
