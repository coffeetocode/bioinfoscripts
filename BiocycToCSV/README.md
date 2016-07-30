

Script state:
 - [x] Script short description
 - [ ] Script full description
 - [ ] Accepts command line params
 - [x] Sample inputs
 - [x] Sample outputs
 - [ ] Commented

# Load Data from BioCyc XML into CSV
 
Fetches specific data from the biocyc.org web services and saves as CSV. Reads in BioCyc gene IDs (such as EG10020)

Data includes: "gene_name", "molecular_weight_by_seq", "molecular_weight_by_exp", "ontology_frameids", "ontology_text", "left_end_protein_feature", "right_end_protein_feature", "assay"

Examples of the XML produced by biocyc and consumed by this are in the EXAMPLE*.xml files.
Gene IDs loaded from GENEIDS.txt
Example output in genedata.csv

# Requirements

Python 2.7 and [requests](http://docs.python-requests.org/en/master/) library

# Usage

```
C:\src\bioinfoscripts\BiocycToCSV>python geneid_to_csv.py
[*] Retrieving EG10020...
[*] Retrieving EG11647...
[*] Retrieving EG10217...
[*] Retrieving EG11528...
```

