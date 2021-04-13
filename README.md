# assign-reviewers

Very simple script to randomly assign reviewers and create scoring sheets.

## Installation

````bash
pip install assign-reviewers
````

## How to use

1. Start from an Excel or Google sheet. Each row corresponds to a submission. Columns are organized as per [this example
CSV file](./testing/form.csv).

2. Export the sheet into a CSV file.

3. Run (replace with your exported form):

````bash
assign-reviewers -c form.csv
````
