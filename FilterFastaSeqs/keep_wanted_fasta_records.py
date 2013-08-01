#A script to keep sequences which contain a particular name from a larger fasta file
from Bio import SeqIO
import sys

#check number of arguments passed on the command line
if not len(sys.argv) == 4:
    print "Usage: keep_wanted_seqs.py record_name_to_keep input_filename output_filename"
    exit()
    
wanted_sample_name = sys.argv[1]
input_filename = sys.argv[2]
output_filename = sys.argv[3]

#example values:
#input_filename = "All_Acinetobacter_Silva.fasta"
#output_filename = "Acinetobacter_baumannii.fasta"
#wanted_sample_name = "Acinetobacter_baumannii"

handle = open(input_filename)
#open one fasta file

records = list(SeqIO.parse(handle, "fasta"))
#Parse each fasta sequence within that file

wanted_records = []
print "Found %i records" % len(records)
for record in records:
    if wanted_sample_name in record.name:
        wanted_records.append(record)

output_handle = open(output_filename, "w")
SeqIO.write(wanted_records, output_handle, "fasta")
output_handle.close()
print "Kept %i records" % len(wanted_records)