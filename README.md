# Rate Deck Parsing
There are several strategies for how to approach this depending on the number of accounts and frequency you have to handle. 

WHAT: Automate parsing of supplier rate decks, i.e. find the data you need in the files and convert it to a format that your system accepts. The assumptions is that the cost lists from suppliers are sent as email attachements in either CSV or any kind of spreadsheet format like xlsx. 

WHY: This process is highly manual today, taking a lot of manual work labor efforts with high risk of mistakes that can lead to margin loss because of error in cost or price list management. Changes the needs attention can also happen outside of office hours or other times when staff is not available for manual handling. 

HOW: 
There are a number of approcahes: 

1. Create for each supplier a code snippet that takes the new cost file as input, parse it and write a new cost file for upload in the format that your system requires. Fast, easy but not scalable...works when you have fe suppliers. 

2. Create an in data processor that parse's the file into an internal calaculation/storage JSON format (for example), and then via an out data processor converts it to the specified routing system format. 

3. Out sources the whole shabang to a 3rd party like IX Links. This will cost you approxematly a CAPEX and then OPEX of about 100 USD per account and month. Then the 3rd party will take over all your communication with the 3rd party and ensure that they dleivery the costlist in the correct format and at the right time, ie ensure that everything techncial and legally agreed is being honored. 
