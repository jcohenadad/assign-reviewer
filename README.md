[![test status](https://github.com/jcohenadad/assign-reviewers/workflows/test/badge.svg)](https://github.com/jcohenadad/assign-reviewers/actions/workflows/test.yml)
[![publish pypi](https://github.com/jcohenadad/assign-reviewers/workflows/publish/badge.svg)](https://github.com/jcohenadad/assign-reviewers/actions/workflows/publish.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.md)

# assign-reviewers

Very simple script to randomly assign reviewers and create scoring sheets.

## Installation

````bash
pip install assign-reviewers
````

## How to use

1. Start from an Excel or Google sheet. Each row corresponds to a submission. Columns are organized as per [this example
CSV file](./testing/form.csv).

2. Export the sheet into a CSV file. For this example, let's use [this example CSV file](./testing/form.csv).

3. Run:

````bash
assign-reviewers -c form.csv -r Anna -r Elsa -r Christophe -r Sven -n 2
````

This will generate four CSV files, each containing an additional column with the name of the reviewer. 

4. Send individual CSV file to the corresponding reviewer.

5. Each reviewer uploads the CSV on Google Sheet: **File > Import**, then click "Upload", drag & drop the CSV file, 
   and click "Import data". The listed submissions can then be graded/ranked as shown below:
   
   ![Alt text](documentation/fig_tutorial_1.png?raw=true "Title")

6. Each reviewer shares their Google Sheet with you, and you can simply copy the reviewer column and append it to the
   main Google Sheet document. Then, a row-wise summation can easily be done.
   

## More complex usage

The software can also ignore reviewers if their affiliation match that of a submitter. Below is an example:

````bash
assign-reviewers -c form.csv -r Anna -a "Chiang Mai" -r Elsa -a UBC "British Columbia"
````

In this example, the reviewer **Elsa** has the affiliations {'UBC', 'British Columbia'}, and if these are found in the 
affiliation of the submitter, then this reviewer will not be assigned.


## Got any problem?

Please [open an issue](https://github.com/jcohenadad/assign-reviewers/issues)
