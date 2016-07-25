

Script state:
 - [x] Script short description
 - [ ] Script full description
 - [ ] Accepts command line params
 - [x] Sample inputs
 - [x] Sample outputs
 - [x] Commented

 
# DNA Walk

Basic idea: map GTAC to left/up/down/right on a 2D surface, and visualize sequence similarity. 

![DNA walk using matplotlib](dna_walk.png?raw=true "DNA walk using matplotlib")

Tons of problems with this idea and trying to infer any meaning from it, but it's fun and maybe useful in some cases.

Apparently repeats the work of http://athena.bioc.uvic.ca/virology-ca-tools/graphdna/. Oh well. 

# Requirements

Written for Python 2.7.x. Requires [matplotlib](http://matplotlib.org/users/installing.html).

# Usage Example

Filename is set in dna_walk_utils.py; by default uses the included "All seqs.fasta" file I had lying around (16S from a bunch of organisms). 

```
$ dna_walk_matplotlib2.py
Walking Treponema_pallidum subsp. pertenue 16S ribosomal RNA gene, partial sequence
Walking Brucella_melitensis strain MY/2009/1483 16S ribosomal RNA gene, partial sequence
Walking R.rickettsii 16S rRNA gene, partial sequence
Walking gnl|ECOLI|EG30084 rrsA "RRSA-RRNA" 4033554..4035095 Escherichia coli K-12 substr. MG1655
Walking Clostridium_botulinum
Walking Staphylococcus_intermedius gene for 16S rRNA, partial sequence, strain: ATCC 29663 (= MAFF 911388)
Walking Salmonella_enterica_typhi subsp. enterica serovar Typhi strain SS 02 16S ribosomal RNA gene, partial sequence
Walking Mycobacterium_intracellulare 16S rRNA gene
Walking Streptococcus_gordonii 16S rRNA gene
<etc, etc>
```
