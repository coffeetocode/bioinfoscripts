"""
Fetches specific data from the biocyc.org web services and saves as CSV.
Equivalent human-readable form is at http://biocyc.org/gene?orgid=ECOLI&id=EG10943#tab=showAll

Current usage is for acetylation work, but easily modified for other stuff.

See column names in make_csv or EXAMPLE-genedata.csv
Examples of the XML produced by biocyc and consumed by this are in the EXAMPLE*.xml files
"""

import xml.etree.ElementTree as ET
import csv
import requests
import time
from collections import namedtuple

GENEIDS_FILENAME = "GENEIDS.csv"
Gene = namedtuple('Gene', ["accession_id", "acetylation_site"])
# eg: http://websvc.biocyc.org/apixml?fn=all-products-of-gene&id=ECOLI:EG10943&detail=full 
URL_TEMPLATE = "http://websvc.biocyc.org/apixml?fn=all-products-of-gene&id=ECOLI:{}&detail=full"
# eg: http://websvc.biocyc.org/getxml?ECOLI:GO:0016260
GO_URL_TEMPLATE = "http://websvc.biocyc.org/getxml?ECOLI:{}"

def read_geneids(filename):
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        genes = [Gene(row["ecocyc_accession_id"], row["acetylation_site"]) for row in reader]
    return genes

def fetch_and_extract_gene_ontology(go_id):
    r = requests.get(GO_URL_TEMPLATE.format(go_id))
    # Use for debugging to keep a copy of each requested file
    #with open("{}.xml".format(go_id), "w") as outfile:
    #    outfile.write(r.text)
    with open("tmp_go.xml".format(go_id), "w") as tmpfile:
        tmpfile.write(r.text)
    
    tree = ET.parse("tmp_go.xml") # 
    root = tree.getroot()
    
    go_text = root.find("./GO-Term/common-name").text.strip()
    time.sleep(1) # respect biocyc request to throttle to less than 1 request/sec
    return go_text

def extract_assays(column_values, root):
    #Direct assay, Purified assay, Mutant assay
    assays = [assay_type.text for assay_type in root.findall("./Protein/has-go-term/evidence/Evidence-Code/common-name")]
    # TODO: I'm worried the string matching is too loose for a poorly structured data fields. 
    # See issue #2 for discussion
    column_values["direct_assay"] = any("direct" in a for a in assays)
    column_values["mutant_assay"] = any("mutant" in a for a in assays)
    column_values["purified_assay"] = any("mutant" in a for a in assays)
    # Not actually an assay. Suck it.
    column_values["computational_assay"] = any("computational" in a for a in assays)

def fetch_and_extract(gene):
    """Call apixml?fn=all-products-of-gene on the given gene, and get most of the required info"""
    print "[*] Retrieving {}...".format(gene.accession_id),
    r = requests.get(URL_TEMPLATE.format(gene.accession_id))
    # Use for debugging to keep a copy of each requested file
    #with open("{}.xml".format(gene.accession_id), "w") as outfile:
    #    outfile.write(r.text)
    with open("tmp.xml".format(gene.accession_id), "w") as tmpfile:
        tmpfile.write(r.text)
    
    tree = ET.parse("tmp.xml") # 
    root = tree.getroot()
    column_values = {}

    # TODO: Refactor to use a function per column
    column_values["gene_name"] = root.find("./Protein/common-name").text
    column_values["molecular_weight_by_seq"] =  root.find("./Protein/molecular-weight-seq").text.strip()  
    exp_weight = root.find("./Protein/molecular-weight-exp")
    column_values["molecular_weight_by_exp"] =  exp_weight.text.strip() if exp_weight is not None else "NaN"
    gene_ontology_object_ids = [x.attrib["frameid"] for x in root.findall("./Protein/has-go-term/GO-Term")]
    column_values["ontology_frameids"] = ";".join(gene_ontology_object_ids)
    print "({} ontologies)...".format(len(gene_ontology_object_ids))
    column_values["ontology_text"] = ";".join([fetch_and_extract_gene_ontology(id) for id in gene_ontology_object_ids])
    column_values["left_end_protein_feature"] = root.find("./Protein/has-feature/Feature/left-end-position").text
    column_values["right_end_protein_feature"] = root.find("./Protein/has-feature/Feature/right-end-position").text
    
    extract_assays(column_values, root)
    
    return column_values

def make_csv():
    column_names = ["gene_name", 
                    "molecular_weight_by_seq", 
                    "molecular_weight_by_exp", 
                    "ontology_frameids", 
                    "ontology_text", 
                    "left_end_protein_feature", 
                    "right_end_protein_feature", 
                    
                    # from extract_assays
                    "direct_assay",
                    "mutant_assay",
                    "purified_assay",
                    "computational_assay",
                    ]
    
    row_data = [fetch_and_extract(gene) for gene in read_geneids(GENEIDS_FILENAME)]
    
    with open('genedata.csv', 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(row_data)

make_csv()
