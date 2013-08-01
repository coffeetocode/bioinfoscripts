#Example code to find sequences less than a given length
from Bio import SeqIO
short_sequence_threshold = 1300

file = open("arb-silva.de_2013-02-27_id83003.fasta")
records = list(SeqIO.parse(file, "fasta"))

for record in records:
    if len(record.seq) < short_sequence_threshold:
        print record.name, "is short:", len(record.seq), "bases"