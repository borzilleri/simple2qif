## simple2qif

Converts Simple.com CSV export to QIF files.

### Usage

    python simple2qif.py <export.csv>

### Output

The resulting file will be:

    simple-YYYY-MM-DD.qif

The date depends on the input file name, by default, Simple's exported files
have a name like:

    2014-01-01-exported_transactions.csv

If the input file starts with a date in that format (`yyyy-mm-dd`), the output
file will be named using that date, otherwise it will use the current date.

### Conversion Description

* D: Tranasction Date, from the 'Date' field
* T: Transaction Amount, from the 'Amount' field
* P: Payee, from the 'Description' field
* A: Address, from the Street, City, State, Zip, as availble.
* L: Category:Subcategory, from the 'Category folder' and 'Category' fields,
	respectively
