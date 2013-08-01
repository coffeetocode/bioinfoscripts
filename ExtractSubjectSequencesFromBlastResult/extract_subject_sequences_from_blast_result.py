# Very simple script to turn output of sequence alignments from BLAST into a FASTA-sytyle format
# There may already be better tools that do this, but hope it helps for now.
#
# Operates on the current directory, consuming all *.in files and producing corresponding *.out files
# Does not clobber input files, alwasy clobbers output files
# Usage (no params):
#     > python extract_subject_sequences_from_blast_result.py

import sys
import os

EXTENSION_FOR_INPUT_FILES = ".in"
EXTENSION_FOR_OUTPUT_FILES = ".out"

def extract_subject_sequences(filename):
    file = open(filename)
    lines = file.read().split("\n")
    
    filename_without_extension = os.path.splitext(filename)[0]
    extracted_lines = []
    
    for line in lines:
        if line.startswith(">"):
            extracted_lines.append("\n")
            extracted_lines.append(line)
        elif line.startswith("Sbjct"):
            extracted_lines.append(line.split()[2])
    
    out_file = open(filename_without_extension + EXTENSION_FOR_OUTPUT_FILES, "w")
    for line in extracted_lines:
        out_file.write(line + "\n")
    out_file.close()


for filename in os.listdir("."):
    if filename.endswith(EXTENSION_FOR_INPUT_FILES):
        extract_subject_sequences(filename)

####################
#  EXAMPLE INPUT
####################
"""
>emb|AL009126.3| Download subject sequence AL009126 spanning the HSP Bacillus subtilis subsp. subtilis str. 168 complete genome
Length=4215606

 Features in this part of subject sequence:
   oxalate decarboxylase

 Score = 2172 bits (1176),  Expect = 0.0
 Identities = 1176/1176 (100%), Gaps = 0/1176 (0%)
 Strand=Plus/Minus

Query  1        ATGCTGTTGGAACAACAACCAATCAATCATGAAGACAGAAACGTGCCGCAGCCTATTCGA  60
                ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
Sbjct  2038779  ATGCTGTTGGAACAACAACCAATCAATCATGAAGACAGAAACGTGCCGCAGCCTATTCGA  2038720

Query  61       AGTGATGGAGCTGGAGCTATTGATACAGGCCCGCGAAATATAATACGGGATATTCAAAAT  120
                ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
Sbjct  2038719  AGTGATGGAGCTGGAGCTATTGATACAGGCCCGCGAAATATAATACGGGATATTCAAAAT  2038660        
"""

##################
# EXAMPLE OUTPUT
##################
"""
>B. subtilis 168|BG13484|yoaN: 1176 bp - unknown; similar to unknown proteins
atgctgttggaacaacaaccaatcaatcatgaagacagaaacgtgccgcagcctattcga
agtgatggagctggagctattgatacaggcccgcgaaatataatacgggatattcaaaat
ccgaatatatttgttccgcctgttacagatgagggtatgattcctaacttgagattttca
ttctcagacgctcccatgaaattagatcacggcggctggtcaagagaaatcaccgtaaga
cagcttccgatttcgactgcgattgcaggtgtaaacatgagcttaactgcgggaggcgtc
cgcgagcttcattggcataagcaagcggagtgggcttatatgcttttgggacgggcacgt
atcaccgctgttgaccaagacggacgaaatttcattgctgatgttggtcccggcgacctt
tggtacttcccggcaggaattccgcattccatacagggattggaacactgcgagtttctg
ctcgttttcgatgatgggaacttttctgagttttcaacgttaaccatttcagattggctt
gcacacacaccaaaagatgttctgtctgcaaatttcggtgtcccggagaatgctttcaac
tctcttccgtctgagcaagtctatatctaccaagggaatgtgccgggatcagtcgccagt
gaagacattcagtcaccatatggaaaagtccccatgacctttaaacacgagctgttaaat
caacccccaattcaaatgccaggggggagtgtacgaattgtggattcttctaacttccca
atttcaaaaacgatagccgctgcacttgttcagattgagcctggcgcgatgagagagctt
cattggcatcccaatagcgatgagtggcaatattatctaacaggacagggacgaatgacg
gtatttatcggaaatgggactgcccgcacatttgattatagagcaggcgacgttggatac
gtgccttctaatgccggacactatatacaaaacactggtacagaaacattatggttttta
gaaatgttcaaaagtaaccgctatgcagatgtgtcactcaatcagtggatggcattgacg
cctaaagaattagtacaaagcaacttgaatgctggatcagtcatgcttgattctctgcgc
aagaagaaagtgcctgttgtgaaatatcccggtacg
"""

#An alternate, better way to do this using SeqIO
#Note: I haven't actually tested this code yet
"""
from Bio import SeqIO
for filename in os.listdir("."):
    if filename.endswith(".gbk"):
        filename_without_extension = os.path.splitext(filename)[0]
        SeqIO.convert(filename, "genbank", filename_without_extension + ".fasta", "fasta")


from Bio.Blast import NCBIStandalone
blast_parser = NCBIStandalone.BlastParser()
blast_record = blast_parser.parse(open("BLAST_seq.txt").read())

outfile = open("fasta_seq.txt", "w")

outfile.write(">" + str(blast_record.descriptions))
for alignment in blast_record.alignments:
    outfile.write 
"""    

