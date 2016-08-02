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
import os
from collections import namedtuple

GENEIDS_FILENAME = "GENEIDS.csv"
Gene = namedtuple('Gene', ["accession_id", "acetylation_site"])
# eg: http://websvc.biocyc.org/apixml?fn=all-products-of-gene&id=ECOLI:EG10943&detail=full 
URL_TEMPLATE = "http://websvc.biocyc.org/apixml?fn=all-products-of-gene&id=ECOLI:{}&detail=full"
# eg: http://websvc.biocyc.org/getxml?ECOLI:GO:0016260
GO_URL_TEMPLATE = "http://websvc.biocyc.org/getxml?ECOLI:{}"

# Dir to keep downloaded files to prevent re-hitting online service on every run
# Delete the dir to get fresh data
XML_CACHE_DIR = "xml_cache"
if not os.path.isdir(XML_CACHE_DIR):
    os.makedirs(XML_CACHE_DIR)

def read_geneids(filename):
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        genes = [Gene(row["ecocyc_accession_id"], int(row["acetylation_site"])) for row in reader]
    return genes

def extract_molecular_weights(column_values, root):
    column_values["molecular_weight_by_seq"] =  root.find("./Protein/molecular-weight-seq").text.strip()  
    exp_weight = root.find("./Protein/molecular-weight-exp")
    column_values["molecular_weight_by_exp"] =  exp_weight.text.strip() if exp_weight is not None else "NaN"

def fetch_and_extract_gene_ontology(go_id):
    fname = os.path.join(XML_CACHE_DIR, "{}.xml".format(go_id.replace(":","_")))
    if not os.path.isfile(fname):
        time.sleep(1) # respect biocyc request to throttle to less than 1 request/sec
        r = requests.get(GO_URL_TEMPLATE.format(go_id))
        with open(fname, "w") as outfile:
            outfile.write(r.text)
    
    tree = ET.parse(fname) 
    root = tree.getroot()
    
    go_text = root.find("./GO-Term/common-name").text.strip()
    return go_text

def extract_gene_ontologies(column_values, root):
    gene_ontology_object_ids = [x.attrib["frameid"] for x in root.findall("./Protein/has-go-term/GO-Term")]
    column_values["ontology_frameids"] = "\n".join(gene_ontology_object_ids)
    print "({} ontologies)...".format(len(gene_ontology_object_ids))
    column_values["ontology_text"] = "\n".join([fetch_and_extract_gene_ontology(id) for id in gene_ontology_object_ids])

def extract_protein_features(column_values, root, gene):
    features = root.findall("./Protein/has-feature/Feature")
    
    features_at_acetylation_site = []
    for num,feature in enumerate(features):
        leftf = feature.find("./left-end-position")
        left = int(leftf.text) if leftf is not None else -1
        rightf = feature.find("./right-end-position")
        right = int(rightf.text) if rightf is not None else -1
        if left <= gene.acetylation_site <= right:
            commentf = feature.find("./comment")
            comment = commentf.text if commentf is not None else "no comment"
            features_at_acetylation_site.append("{}-{}/{}".format(left, right, comment))
    
    column_values["left_end_protein_feature"] = "DEPRECATED"
    column_values["right_end_protein_feature"] = "DEPRECATED"
    column_values["features_at_acetylation_site"] = "\n".join(features_at_acetylation_site)

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
    fname = os.path.join(XML_CACHE_DIR, "{}.xml".format(gene.accession_id))
    if not os.path.isfile(fname):
        print "[*] Retrieving {}...".format(gene.accession_id),
        r = requests.get(URL_TEMPLATE.format(gene.accession_id))
        with open(fname, "w") as outfile:
            outfile.write(r.text)
    else:
        print "[*] Retrieving (cached) {}...".format(gene.accession_id),
    
    tree = ET.parse(fname) # 
    root = tree.getroot()
    column_values = {}

    column_values["accession_id"] = gene.accession_id
    column_values["acetylation_site"] = gene.acetylation_site
    name_node = root.find("./Protein/common-name")
    column_values["gene_name"] = name_node.text if name_node is not None else "(no gene common name)"
    extract_molecular_weights(column_values, root)
    extract_gene_ontologies(column_values, root)
    extract_protein_features(column_values, root, gene)
    extract_assays(column_values, root)
    
    return column_values

def make_csv():
    column_names = [
                    "accession_id", 
                    "acetylation_site", 
                    "gene_name", 
    
                    # from extract_molecular_weights
                    "molecular_weight_by_seq", 
                    "molecular_weight_by_exp", 
                    
                    # from extract_gene_ontologies
                    "ontology_frameids", 
                    "ontology_text", 
                    
                    # from extract_protein_features
                    "features_at_acetylation_site",
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
