#Makefile for QIIME Pipeline
# (not yet tested)
#
#Usage: 
# - Fill in the MAPPING_FILE variable with the name of your mapping file
# - If running MiSeq data, fill in FASTQ_READ_FILE and FASTQ_INDEX_FILE variables 
# - If running Curated data, fill in the FASTA_DATA_DIRECTORY variable
#
# Run as follows:
# $ make miseq
#     or
# $ make curated

#A mapping file is used in all cases
MAPPING_FILE = Urinemicrobiome_MiSeq_Map.txt

#Read and Index files are only used for MiSeq data 
#(fill in correct filenames for your data)
FASTQ_READ_FILE = C3_S3_L001_R2_001.fastq
FASTQ_INDEX_FILE = C3_S3_L001_I2_001.fastq

#A Data directory is only used for curated data
#(make sure your curated data with valid fasta extensions lives in here)
FASTA_DATA_DIRECTORY = data

#All targets (steps) used when processing curated data
curated: add_qiime_labels pick_otus_through_otu_table filter_otus_from_otu_table per_library_stats make_otu_heatmap_html summarize_taxa_through_plots alpha_rarefaction

#All targets (steps) used when processing miseq data
miseq: check_id_map split_libraries_fastq pick_otus_through_otu_table filter_otus_from_otu_table per_library_stats make_otu_heatmap_html summarize_taxa_through_plots alpha_rarefaction

add_qiime_labels: data $(MAPPING_FILE) 
	add_qiime_labels.py

combined_fasta/combined_seqs.fna: add_qiime_labels

check_id_map: $(MAPPING_FILE)
	check_id_map.py -m $(MAPPING_FILE) -o mapping_output -v

split_libraries_fastq:
	split_libraries_fastq.py -i $(FASTQ_READ_FILE) -o Out/ -b $(FASTQ_INDEX_FILE) -m $(MAPPING_FILE) -r 6 --barcode_type 8

Out/seqs.fna: split_libraries_fastq

pick_otus_through_otu_table: Out/seqs.fna
	pick_otus_through_otu_table.py -i Out/seqs.fna -o otus

otus/otu_table.biom: pick_otus_through_otu_table

filter_otus_from_otu_table: otu_table.biom
	filter_otus_from_otu_table.py -i otus/otu_table.biom -o otus/otu_table_ns.biom -n 10

otu_table_ns.biom: filter_otus_from_otu_table

per_library_stats: otu_table_ns.biom
	per_library_stats.py -i otus/otu_table_ns.biom

make_otu_heatmap_html: otus/otu_table_ns.biom
	make_otu_heatmap_html.py -i otus/otu_table_ns.biom -o otus/OTU_Heatmap/

taxa_params.txt:
	echo "plot_taxa_summary:chart_type pie,bar" > taxa_params.txt

summarize_taxa_through_plots: otu_table_ns.biom $(MAPPING_FILE) taxa_params.txt
	summarize_taxa_through_plots.py -i otus/otu_table_ns.biom -o wf_taxa_summary -m $(MAPPING_FILE) -p taxa_params.txt

alpha_params.txt:
	echo "alpha_diversity:metrics shannon,PD_whole_tree,chao1,observed_species" >alpha_params.txt

alpha_rarefaction: otu_table_ns.biom $(MAPPING_FILE) alpha_params.txt
	alpha_rarefaction.py -i otus/otu_table_ns.biom -m $(MAPPING_FILE) -o wf_arare/ -p alpha_params.txt -t otus/rep_set.tre
