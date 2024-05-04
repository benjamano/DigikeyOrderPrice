import webbrowser 
import os 
import sys
import csv
import digikey
import json
from digikey.v3.productinformation import KeywordSearchRequest
from digikey.v3.batchproductdetails import BatchProductDetailsRequest

errors = []

os.environ['DIGIKEY_CLIENT_ID'] = 'voYufhN1Yd3buAQsb1zbYMtdkXtb06hi'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'b4RXB7h3Yn8zY5EU'
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = '/home/ben/.virtualenvs/python3devwork'

def getProductDetails(stockCode):
    try:
        part = digikey.product_details(stockCode)
        return part
    
    except Exception as bugger:
        errors.append(f"Error while retrieving part details\n Stock Code: {stockCode}\nException: {bugger}")
        return None
    
def getPrice(part, quantity, orderQuantity):
    
    if part:
        unitPrice = part.unit_price * quantity * orderQuantity
        
        return unitPrice
        
    return None
    

def CalculateTotalPrice(CSVFile, quantity):
    noFit = 0
    unmatchedParts = []
    totalPrice = 0.0
    partsSearched = 0
    
    file = open(CSVFile)
    csvreader = csv.DictReader(file)
    
    #For debugging if needed
    header=[]
    header=next(csvreader)
    
    for row in csvreader:
        stockCode = row.get("Stock Code")
        orderQuantity = int(row.get("Quantity"))
        if stockCode == 'NO FIT':
            #If there is no stock code listed in the file
            noFit +=1
            unmatchedParts.append(stockCode)
            break
            
        else:
            part = getProductDetails(stockCode)
            
            if part:
                
                price = getPrice(part, quantity, orderQuantity)
                
                partsSearched += 1
                print(f"\nParts Searched: {partsSearched}")
                
                if price:
                    totalPrice += price
                
                else:
                    unmatchedParts.append(stockCode)
            else:
                unmatchedParts.append(stockCode)
    
    return totalPrice, unmatchedParts
                
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 DigikeyPricing.py <CSVfile> <Quantity>")
        #Default, fall-back value for debugging
        # CSVFile = 'BillOfMaterialsPowerPortMax-v5.csv'
        # Quantity = 50
    
    else:
        CSVFile = sys.argv[1]
        Quantity = int(sys.argv[2])
        
    print(f"\n\nOpening file '{CSVFile}', ordering {Quantity} sets.\n Working...")
    
    totalPrice, unmatchedParts = CalculateTotalPrice(CSVFile, Quantity)
    
    print('---------------------------FINISHED---------------------------------\n')
    
    print(f"Total price for {Quantity} sets of parts: £{totalPrice.__round__(2)}")
    
    print('\n--------------------------------------------------------------------\n')
    
    if unmatchedParts:
        print("Unmatched parts:\n")
        for part in unmatchedParts:
            print(part)
    
    print('\n--------------------------------------------------------------------\n')
    
    if errors:
        print("Errors:")
        for error in errors:
            print(f"Error #1: {error}")
        
        print('\n\n--------------------------------------------------------------------\n\n')
