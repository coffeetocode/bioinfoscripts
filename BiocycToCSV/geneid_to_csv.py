"""
Fetches specific data from the biocyc.org web services and saves as CSV.

See column names in make_csv or EXAMPLE-genedata.csv
Examples of the XML produced by biocyc and consumed by this are in the EXAMPLE*.xml files
"""

import xml.etree.ElementTree as ET
import csv
import requests
import time

GENEIDS_FILENAME = "GENEIDS.txt"
#eg: http://websvc.biocyc.org/apixml?fn=all-products-of-gene&id=ECOLI:EG10943&detail=full 
URL_TEMPLATE = "http://websvc.biocyc.org/apixml?fn=all-products-of-gene&id=ECOLI:{}&detail=full"
#eg: http://websvc.biocyc.org/getxml?ECOLI:GO:0016260
GO_URL_TEMPLATE = "http://websvc.biocyc.org/getxml?ECOLI:{}"
geneids = open(GENEIDS_FILENAME).read().split()


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
    

def fetch_and_extract(geneid):
    """Call apixml?fn=all-products-of-gene on the given gene, and get most of the required info"""
    print "[*] Retrieving {}...".format(geneid)
    r = requests.get(URL_TEMPLATE.format(geneid))
    # Use for debugging to keep a copy of each requested file
    #with open("{}.xml".format(geneid), "w") as outfile:
    #    outfile.write(r.text)
    with open("tmp.xml".format(geneid), "w") as tmpfile:
        tmpfile.write(r.text)
    
    tree = ET.parse("tmp.xml") # 
    root = tree.getroot()
    column_values = {}

    column_values["gene_name"] = root.find("./Protein/common-name").text
    column_values["molecular_weight_by_seq"] =  root.find("./Protein/molecular-weight-seq").text.strip()  
    exp_weight = root.find("./Protein/molecular-weight-exp")
    column_values["molecular_weight_by_exp"] =  exp_weight.text.strip() if exp_weight is not None else "NaN"
    # TODO: Actually dereference these to get the terms instead of term IDs
    gene_ontology_object_ids = [x.attrib["frameid"] for x in root.findall("./Protein/has-go-term/GO-Term")]
    column_values["ontology_frameids"] = ";".join(gene_ontology_object_ids)
    column_values["ontology_text"] = ";".join([fetch_and_extract_gene_ontology(id) for id in gene_ontology_object_ids])
    column_values["left_end_protein_feature"] = root.find("./Protein/has-feature/Feature/left-end-position").text
    column_values["right_end_protein_feature"] = root.find("./Protein/has-feature/Feature/right-end-position").text
    column_values["assay"] = root.find("./Protein/has-go-term/evidence/Evidence-Code/common-name").text
    
    return column_values

def make_csv():
    column_names = ["gene_name", "molecular_weight_by_seq", "molecular_weight_by_exp", "ontology_frameids", "ontology_text", "left_end_protein_feature", "right_end_protein_feature", "assay"]
    
    row_data = [fetch_and_extract(geneid) for geneid in geneids]
    
    with open('genedata.csv', 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)
        writer.writeheader()
        writer.writerows(row_data)

make_csv()
