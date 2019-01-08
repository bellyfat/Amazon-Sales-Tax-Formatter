# Amazon Sales Tax Formatter

This tool is designed to take Amazon Seller Central's sales tax report and output relevant columns into a format that's more easy to be managed by a spreadsheet application like Excel.

## Getting Started

Copy your sales tax report to the folder location as "amazon.csv" and then simply run:
python collatesalestax.py
The script will output your results to output.csv.  Note that this will combine all "district" jurisdiction taxes into the same thing.  This was programmed for Wisconsin Sales & Use tax, which doesn't have overlapping "district" taxes.  If your state has this (not sure if that's ever the case), these values will be inaccurate and the script will have to be modified to identify these.  This will will not re-sort the document but you now can easily do it through a spreadsheet application since al values will be present.

You'll find counties with "NOT APPLICABLE" and unfortunately you'll have to go by the shipping zip to find those counties manually.  These are for counties that do not have their own sales tax.
### Prereqs

You should only need python 3.X and standard python libraries for this application.

### Author

Scott Degen

## License

This project is licensed under the MIT License.  See https://opensource.org/licenses/MIT for details.

The author is not a tax expert or accountant and makes no claims of accuracy.  Consult your tax accountant for accurate sales tax numbers.