# http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc81

# http://www.ncbi.nlm.nih.gov/BLAST/blast_overview.html

#qblast(program, database, sequence, auto_format=None, composition_based_statisti
#cs=None, db_genetic_code=None, endpoints=None, entrez_query='(none)', expect=10.
#0, filter=None, gapcosts=None, genetic_code=None, hitlist_size=50, i_thresh=None
#, layout=None, lcase_mask=None, matrix_name=None, nucl_penalty=None, nucl_reward
#=None, other_advanced=None, perc_ident=None, phi_pattern=None, query_file=None,
#query_believe_defline=None, query_from=None, query_to=None, searchsp_eff=None, s
#ervice=None, threshold=None, ungapped_alignment=None, word_size=None, alignments
#=500, alignment_view=None, descriptions=500, entrez_links_new_window=None, expec
#t_low=None, expect_high=None, format_entrez_query=None, format_object=None, form
#at_type='XML', ncbi_gi=None, results_file=None, show_overview=None, megablast=No
#ne)



from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML


seq = """>B. subtilis 168|BG13484|yoaN: 1176 bp - unknown; similar to unknown proteins
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
aagaagaaagtgcctgttgtgaaatatcccggtacg"""

print "Candidate Sequence:\n", seq

print "\n\n\nQuerying BLAST..." 
#result_handle = NCBIWWW.qblast(program="blastn", database="nr", sequence=seq)
#save_file = open("my_blast.xml", "w")
#save_file.write(result_handle.read())
#save_file.close()
#result_handle.close()

result_handle = open("my_blast.xml")


blast_record = NCBIXML.read(result_handle)

E_VALUE_THRESH = 0 #or something like 1.0e-50
alignments = 0

for alignment in blast_record.alignments:
    for hsp in alignment.hsps:
        if hsp.expect <= E_VALUE_THRESH:
            print '****Alignment****'
            alignments += 1
            print 'sequence:', alignment.title
            print 'length:', alignment.length
            print 'e value:', hsp.expect
            print hsp.query[0:75] + '...'
            print hsp.match[0:75] + '...'
            print hsp.sbjct[0:75] + '...'

print "\n\n\nNum Alignments with e <= %f: %d" % (E_VALUE_THRESH, alignments)