# DigikeyOrderPrice

## Usage

Call the python script like this:

```
python3 DigikeyPricing.py [CSVFile] [QuantitytoOrder]
```
For example:

```
python3 DigikeyPricing.py BillOfMaterialsPowerPortMax-v5.csv 10
```

## Code Breakdown

### getProductDetails(stockCode)

This function attempt to get the product details of a part's stock code, this is retrieved using the CSV file attached.
If the details are succesfully fetched, they are returned.

If an error occurs, the error is appended to a list of errors and printed at the end of the process, this is because many errors may occur due to mismatched or unavailable part stock codes.

### getPrice(part, quantity, orderQuantity)

This function calculates the price of the components to be bought, it multiplies the unitprice (Taken from the Digikey API), quanitity passed when the file is run, and the quanity inside the CSV file.

### CalculateTotalPrice(CSVFile, quantity)

This function reads a CSV file containing parts information. 
For each part, it tries to retrieve its details and calculate the price based on the provided quantity. 
If successful, it adds the price to the total. If not, it keeps track of unmatched parts. 
Finally, it returns the total price and a list of unmatched parts.
