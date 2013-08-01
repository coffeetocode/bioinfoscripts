#You need to navigate to the correct folder before you enter mother. Once in the correct file location type mothur
#Create a Stability.file like so: (tab deliminated
	#SampleName	Name_sample_L001_R1_001.fasta	Name_sample_L001_R1_001.fasta
make.contigs(file=stability.files, processors=8)
	#this will read each fastq file in the stability.files and make the contigs. This can take some time, depending on how many files are in the stability file.
summary.seqs(fasta=stability.trim.contigs.fasta)
summary.seqs(fasta=stability.trim.contigs.good.fasta)
screen.seqs(fasta=stability.trim.contigs.fasta, group=stability.contigs.groups, maxambig=0, minlength=275, maxlength=300, processors=8)
unique.seqs(fasta=stability.trim.contigs.good.fasta)
count.seqs(name=stability.trim.contigs.good.names, group=stability.contigs.good.groups)
summary.seqs(count=stability.trim.contigs.good.count_table)
pcr.seqs(fasta=silva.bacteria.fasta, start=11894, end=25319, keepdots=F, processors=8)
system(mv silva.bacteria.pcr.fasta silva.v4.fasta)
summary.seqs(fasta=silva.v4.fasta)
align.seqs(fasta=stability.trim.contigs.good.unique.fasta, reference=silva.v4.fasta)
	#can you run this with the file already created? or do you create it everytime?
	# got this message at the end:
		#Some of you sequences generated alignments that eliminated too many bases, a list is provided in stability.trim.contigs.good.unique.flip.accnos. If you set the flip parameter to true mothur will try aligning the reverse compliment as well.
		#It took 108 secs to align 32562 sequences.
summary.seqs(fasta=stability.trim.contigs.good.unique.align, count=stability.trim.contigs.good.count_table)
screen.seqs(fasta=stability.trim.contigs.good.unique.align, count=stability.trim.contigs.good.count_table, summary=stability.trim.contigs.good.unique.summary, start=1968, end=11550, maxhomop=8)
summary.seqs(fasta=current, count=current)
filter.seqs(fasta=stability.trim.contigs.good.unique.good.align, vertical=T, trump=.)
unique.seqs(fasta=stability.trim.contigs.good.unique.good.filter.fasta, count=stability.trim.contigs.good.good.count_table)
pre.cluster(fasta=stability.trim.contigs.good.unique.good.filter.unique.fasta, count=stability.trim.contigs.good.unique.good.filter.count_table, diffs=2)
chimera.uchime(fasta=stability.trim.contigs.good.unique.good.filter.unique.precluster.fasta, count=stability.trim.contigs.good.unique.good.filter.unique.precluster.count_table, dereplicate=t)
	#/usr/local/bin/uchime file does not exist. Checking path...
	#[ERROR]:  file does not exist. mothur requires the uchime executable.
	#[ERROR]: did not complete chimera.uchime.
remove.seqs(fasta=stability.trim.contigs.good.unique.good.filter.unique.precluster.fasta, accnos=stability.trim.contigs.good.unique.good.filter.unique.precluster.uchime.accnos)
summary.seqs(fasta=current, count=current)
classify.seqs(fasta=stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.fasta, count=stability.trim.contigs.good.unique.good.filter.unique.precluster.uchime.pick.count_table, reference=trainset9_032012.pds.fasta, taxonomy=trainset9_032012.pds.tax, cutoff=80)
remove.lineage(fasta=stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.fasta, count=stability.trim.contigs.good.unique.good.filter.unique.precluster.uchime.pick.count_table, taxonomy=stability.trim.contigs.good.unique.good.filter.unique.precluster.pick.pds.wang.taxonomy, taxon=Chloroplast-Mitochondria-unknown-Archaea-Eukaryota)

#Note: If you get the following error it means you are no longer in mothur and need to re-enter
	#syntax error near unexpected token `('