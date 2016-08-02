

Script state:
 - [x] Script short description
 - [x] Script full description
 - [ ] Accepts command line params
 - [x] Sample inputs
 - [x] Sample outputs
 - [ ] Commented

# Load Data from BioCyc XML into CSV
 
Fetches specific data from the biocyc.org web services and saves as CSV. Reads in BioCyc gene IDs (such as "EG10020")

Output data includes: 
* gene_name
* molecular_weight_by_seq
* molecular_weight_by_exp
* ontology_frameids
* ontology_text
* features_at_acetylation_site
* direct_assay
* mutant_assay
* purified_assay
* computational_assay

Examples of the XML produced by biocyc/ecocyc and consumed by this are in the EXAMPLE*.xml files.

Gene IDs loaded from GENEIDS.txt

Example output in genedata.csv

# Requirements

Python 2.7 and [requests](http://docs.python-requests.org/en/master/) library

# Usage

```
C:\src\bioinfoscripts\BiocycToCSV>python geneid_to_csv.py
[*] Retrieving (cached) EG10943... (12 ontologies)...
[*] Retrieving EG10020... (12 ontologies)...
[*] Retrieving EG11647... (20 ontologies)...
[*] Retrieving EG10217... (26 ontologies)...
[*] Retrieving (cached) EG11528... (15 ontologies)...
```

