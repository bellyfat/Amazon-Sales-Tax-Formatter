#Python 3
import sys
import csv
import logging
from decimal import *
from Logging import Logger, LoggerCallback

class Order(object):
    orderID = None
    shipZip = ""
    state = ""
    stateTaxable = 0
    stateWithheld = 0
    city = ""
    cityTaxable = 0
    cityWithheld = 0
    county = ""
    countyTaxable = 0
    countyWithheld = 0
    district = ""
    districtTaxable = 0
    districtWithheld = 0
    
    def __init__(self, orderID):
        self.orderID = orderID
 
def getOrders(reader):
    order = None
    for row in reader:
        break; #skip headers
    
    for row in reader:
        newOrderID = row[0]
        if newOrderID != "" and (order == None or newOrderID != order.orderID):
            if order != None:
                yield order
                order = None
            order = Order(newOrderID)
        
        shipZip = row[34]
        if shipZip != "":
            order.shipZip = shipZip
        jurisdictionLevel= row[38].lower().strip()
        jurisdictionName=row[39] #Jurisdiction_Name
        taxableAmountString= row[58].strip() #Taxable_Amount
        taxWithheldString= row[52].strip() #Tax_Amount
        taxableAmount = Decimal(taxableAmountString) if taxableAmountString != '' else 0
        taxWithheld = Decimal(taxWithheldString) if taxWithheldString != '' else 0 
        
        if jurisdictionLevel == "state":
            order.state = jurisdictionName
            order.stateTaxable = order.stateTaxable + taxableAmount
            order.stateWithheld = order.stateWithheld + taxWithheld
        elif jurisdictionLevel == "city":
            order.city = jurisdictionName
            order.cityTaxable = order.cityTaxable + taxableAmount
            order.cityWithheld = order.cityWithheld + taxWithheld
        elif jurisdictionLevel == "county":
            order.county = jurisdictionName
            order.countyTaxable = order.countyTaxable + taxableAmount
            order.countyWithheld = order.countyWithheld + taxWithheld
        elif jurisdictionLevel == "district":
            order.district = jurisdictionName
            order.districtTaxable = order.districtTaxable + taxableAmount
            order.districtWithheld = order.districtWithheld + taxWithheld

    if order is not None:
        yield order

def processOrder(writer, order):
    if order.county != "" or order.city != "" or order.district != "" or order.state != "":
        writer.writerow([order.orderID, order.shipZip, order.state, str(order.stateTaxable), str(order.stateWithheld), order.county, str(order.countyTaxable), str(order.countyWithheld), order.city, str(order.cityTaxable), str(order.cityWithheld), order.district, str(order.districtTaxable), str(order.districtWithheld), str(order.stateWithheld + order.countyWithheld + order.cityWithheld + order.districtWithheld)])
    
file = "amazon.csv"
if len(sys.argv) > 1:
    file = sys.argv[1]
    
try:
    with open(file, 'rt') as csvfile, open("output.csv", 'wt') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Order ID", "Ship-To Zip", "State", "State Taxable", "State Tax W/Held", "County", "County Taxable", "County Tax W/Held", "City", "City Taxable", "City Tax W/Held", "District", "District Taxable", "District Tax W/Held", "Total W/Held"])
        reader = csv.reader(csvfile)
        for order in getOrders(reader):
            Logger.log("Processing Order " + order.orderID + ". ")
            processOrder(writer, order)
            pass;
except Exception as e:
    logging.error(e, exc_info=True)