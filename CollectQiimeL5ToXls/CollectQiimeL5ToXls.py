"""
CollectQiimeL5ToXls.py

Consumes a directory of files containing Qiime L5 Taxa identifications 
and produces a single CSV file that contains rows for all observed taxa
and columns of the match percentages for all observed samples.

Sample input file "ABC_R237_L5.txt":
--------
Taxon	ABCR237
k__Bacteria;Other;Other;Other;Other	0.00871188550093
k__Bacteria;p__Actinobacteria;c__Actinobacteria;o__Actinomycetales;f__Actinomycetaceae	0.000555604942662
k__Bacteria;p__Actinobacteria;c__Actinobacteria;o__Actinomycetales;f__Corynebacteriaceae	0.00340030224909
--------

Sample input file "ABC_R241_L5.txt"
--------
Taxon	ABCR241
Unclassified;Other;Other;Other;Other	0.00354843240606
k__Bacteria;p__Actinobacteria;c__Actinobacteria;o__Actinomycetales;f__Actinomycetaceae	0.000532264860909
k__Bacteria;p__Firmicutes;c__Bacilli;o__Lactobacillales;f__Enterococcaceae	0.00363714321621
--------

Sample output file "CollectedL5Data.csv"
--------
Taxa,SampleId
k__Bacteria;Other;Other;Other;Other,0.00871188550093,0.00354843240606
k__Bacteria;p__Actinobacteria;c__Actinobacteria;o__Actinomycetales;f__Actinomycetaceae,0.000555604942662,0.000532264860909
k__Bacteria;p__Actinobacteria;c__Actinobacteria;o__Actinomycetales;f__Corynebacteriaceae,0.00340030224909,,
k__Bacteria;p__Firmicutes;c__Bacilli;o__Lactobacillales;f__Enterococcaceae,,0.00363714321621
--------

Note: These sample inputs and outputs have been made smaller. Real inputs have many more taxa, and match percentages will add up to 1.0.

"""

import os
import re
from collections import defaultdict
import csv

# A regex that will match the filename of all samples; Must have a single capture group that captures the sample ID
SAMPLE_FILENAME_REGEX = re.compile("(ABC_.[0-9]+).*")
INPUT_DIRECTORY = "."
OUTPUT_DIRECTORY = "."
OUTPUT_FILENAME = "CollectedL5Data.csv"

# This lines gets us all the sample filenames out of the INPUT_DIRECTORY
# The square bracket notation used here is called a "list comprehension"; it's a quick way to make a list
sample_filenames = [filename for filename in os.listdir(INPUT_DIRECTORY) if SAMPLE_FILENAME_REGEX.match(filename)]

#see http://docs.python.org/2/library/collections.html#collections.defaultdict
master_taxa_matchvals = defaultdict(dict)
sample_ids = set() #used for setting up the CSV columns

#Takes a filename, returns a dictionary of taxa to matchval
def parse_L5_file(filename):
    lines = open(filename).readlines()
    lines = lines[1:] #ignore the first line which just contains the sample id
    taxa_matchvals = {} #create a new dictionary where we'll keep all data for this sample
    for line in lines:
        taxa, matchval = line.split("\t")
        taxa_matchvals[taxa] = matchval
    return taxa_matchvals
    

for sample_filename in sample_filenames:
    sample_id = SAMPLE_FILENAME_REGEX.match(sample_filename).group(1)
    sample_ids.add(sample_id)
    sample_taxa_matchvals = parse_L5_file(sample_filename)
    
    #merge this new information into the taxa_to_samples dictionary we're building
    for taxa in sample_taxa_matchvals:
        samples_with_this_taxa = master_taxa_matchvals[taxa]
        samples_with_this_taxa[sample_id] = sample_taxa_matchvals[taxa]
        master_taxa_matchvals[taxa] = samples_with_this_taxa

        
with open(os.path.join(OUTPUT_DIRECTORY, OUTPUT_FILENAME), "wb") as outfile:
    csv_columns = ["Taxa"]
    csv_columns.extend(sorted(sample_ids))
    csv_writer = csv.DictWriter(outfile, csv_columns)
    
    csv_writer.writeheader()
    for taxa in sorted(master_taxa_matchvals.keys()):
        
        #Artificially add the taxa to the dict (I approached this wierd, and this is how CSV is expecting it, do blah)
        vals_for_taxa = master_taxa_matchvals[taxa]
        vals_for_taxa["Taxa"] = taxa
        
        csv_writer.writerow(master_taxa_matchvals[taxa])
        


