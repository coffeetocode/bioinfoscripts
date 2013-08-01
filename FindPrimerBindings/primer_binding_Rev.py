# same as primer_binding.py, except only uses reverse primer
from Bio import SeqIO
import sys
import re #must import regex functionality in order to search as a regex

input_filename = sys.argv[1]
print input_filename

#example values:
#input_filename = "Acinetobacter_baumannii_ATCC_17978.fasta"


#V4 primer - all degenerate options
PrmF = "GUGCCAGC[A|C]GCCGCGGUAA"
PrmR = "AUUAGA[A|U][U|A]CCC[C|G|U][A|G|U]GUAGUC" 
PrmRegex = "(%s)(.*)(%s)" % (PrmF, PrmR)

handle = open(input_filename)
#open one fasta file

records = list(SeqIO.parse(handle, "fasta"))
#Parse each fasta sequence within that file

for record in records:
    print ">", record.id
    rev_matches = list(re.finditer(PrmR, str(record.seq)))
    if not rev_matches:
        print "\tThe Rev primer does not bind                   !!!!!"
        continue
    print "\tNumber of times primer binds = %s" % len(rev_matches)
    for rev_match in rev_matches: #it could bind multiple places
        print "\tRev Primer binds starting at %s" % rev_match.start()
        print "\tRev Primer binds ends at %s" % rev_match.end()

