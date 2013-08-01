import csv

#Consolidates data from multiple files so that the QIIME_ID, Input_ID, OTU, and Taxa string can all be read in one place

INPUT_ID_CSV_FILENAME = "Silva_V2-V3_AllSeqs.csv"
SEQ_OTU_MAP_FILENAME = "combined_seqs_otus.txt"
OTU_TAXA_MAP_FILENAME = "combined_seqs_rep_set_tax_assignments.txt"
OUTPUT_CSV_FILENAME = "Final_Doc_OTU-ID-Classification_Output.csv"

aggregated_sample_data = {}

with open(INPUT_ID_CSV_FILENAME, 'rb') as csvfile:
    csvdictreader = csv.DictReader(csvfile, delimiter=',')
    aggregated_sample_data = {}
    #Build a dictionary to look up each sample; 
    #the lookup key for each sample will be the Qiime_ID
    for row in csvdictreader:
        qiime_id = row['Qiime_ID'].lstrip(">")
        aggregated_sample_data[qiime_id] = row


with open(SEQ_OTU_MAP_FILENAME, 'rb') as csvfile:
    csvdictreader = csv.DictReader(csvfile, fieldnames=["OTU"], restkey="QIIME_IDS", delimiter='\t') #First column is OTU, rest of columns are a list called QIIME_IDS
    rows = [row for row in csvdictreader]
    #Each row is a single OTU and several QIIME IDs
    for row in rows:
        for qiime_id in row["QIIME_IDS"]:
            #Look up each QIIME ID and add the OTU as a new key
            otu = row["OTU"]
            try:
                aggregated_sample_data[qiime_id]["OTU"] = otu
            except KeyError as ke:
                print "Error: Failed to find QIIME ID '%s' in aggregated_sample_data when trying to apply OTU from '%s' to record. Check to see that it exists in '%s'" % (qiime_id, SEQ_OTU_MAP_FILENAME, INPUT_ID_CSV_FILENAME)
                raise ke


with open(OTU_TAXA_MAP_FILENAME, 'rb') as csvfile:
    csvdictreader = csv.DictReader(csvfile, fieldnames=["OTU", "Taxa", "Confidence"], delimiter='\t')
    #Build a dictionary of OTU (key) to Taxa (value)
    otu_to_taxa = {row["OTU"]:row["Taxa"] for row in csvdictreader}

for sample in aggregated_sample_data.values():
    #look up the taxa in the otu_to_taxa, and add it to the sample record
    sample["Taxa"] = otu_to_taxa[sample["OTU"]]

#write it all out
with open(OUTPUT_CSV_FILENAME, "wb") as csvfile:
    csvdictwriter = csv.DictWriter(csvfile, ["Qiime_ID", "Input_ID", "Genus", "OTU", "Taxa"])
    csvdictwriter.writeheader()
    for row in aggregated_sample_data.values():
        #print "writing Qiime_ID", row
        csvdictwriter.writerow(row)

