"""
Quickly call every function available in the Pathway Tools API functions [1]
(which is referenced from the BioCyc web services page [2]). Saves all results.
so that you can search locally for what you want from a call, then know which 
API function to call. 

Helps out with the limited documentation.


[1] http://bioinformatics.ai.sri.com/ptools/ptools-fns.html 
[2] http://biocyc.org/web-services.shtml
"""
import requests
import time

URL_TEMPLATE = "http://websvc.biocyc.org/apixml?fn={}&id=ECOLI:EG10943&detail=full"

functions = """all-products-of-gene
binding-site-transcription-factors
chromosome-of-gene
compounds-of-pathway
containers-of
containing-tus
direct-activators
direct-inhibitors
enzymes-of-gene
enzymes-of-pathway
enzymes-of-reaction
genes-of-pathway
genes-of-protein
genes-of-reaction
genes-regulated-by-gene
genes-regulating-gene
modified-containers
modified-forms
monomers-of-protein
pathways-of-compound
pathways-of-gene
reactions-of-compound
reactions-of-enzyme
reactions-of-gene
regulator-proteins-of-transcription-unit
regulon-of-protein
substrates-of-reaction
top-containers
transcription-unit-activators
transcription-unit-binding-sites
transcription-unit-genes
transcription-unit-inhibitors
transcription-unit-mrna-binding-sites
transcription-unit-promoter
transcription-unit-terminators
transcription-unit-transcription-factors
transcription-units-of-gene
transcription-units-of-protein""".split()

def call_and_save(fn_name):
    print "[*] Retrieving {}...".format(fn_name)
    r = requests.get(URL_TEMPLATE.format(fn_name))
    with open("{}.xml".format(fn_name), "w") as outfile:
        outfile.write(r.text)

for f in functions:
    call_and_save(f)
    time.sleep(1) # be a good citizen and wait between requests