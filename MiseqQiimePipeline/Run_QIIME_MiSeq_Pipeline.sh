#QIIME Pipeline for MiSeq Data
# 
# Original version (mizilliox, 2013-03-08)
# Input filenames factored out, comments added, (this version not yet tested) (pthomas, 2013-03-10) 

MAPPING_FILE = Urinemicrobiome_MiSeq_Map.txt
FASTQ_READ_FILE = C3_S3_L001_R2_001.fastq
FASTQ_INDEX_FILE = C3_S3_L001_I2_001.fastq

echo "check_id_map" > ./monitor.txt
date >> ./monitor.txt
check_id_map.py -m $MAPPING_FILE -o mapping_output -v
date >> ./monitor.txt
echo "check_id_map.py end" >> ./monitor.txt
echo "split_libraries_fastq.py">> ./monitor.txt
date>> ./monitor.txt
split_libraries_fastq.py -i $FASTQ_READ_FILE -o Out/ -b $FASTQ_READ_FILE -m $MAPPING_FILE -r 6  --barcode_type 8
date>> ./monitor.txt
echo "split_libraries_fastq.py end" >> ./monitor.txt
echo "pick_otus" >> ./monitor.txt
date>>./monitor.txt
pick_otus_through_otu_table.py -i Out/seqs.fna -o otus
date>>./monitor.txt
echo "pick_otus end">>./monitor.txt
echo "filter_otus">>./monitor.txt
date>>./monitor.txt
filter_otus_from_otu_table.py -i otus/otu_table.biom -o otus/otu_table_ns.biom -n 10
date>>./monitor.txt
echo "filter_otus end">> ./monitor.txt
echo "per_library_stats">>./monitor.txt
date>>./monitor.txt
per_library_stats.py -i otus/otu_table_ns.biom
date>>./monitor.txt
echo "per_library_stats end">>./monitor.txt
echo "make_otu_heatmap">>./monitor.txt
date>>./monitor.txt
make_otu_heatmap_html.py -i otus/otu_table_ns.biom -o otus/OTU_Heatmap/
date>>./monitor.txt
echo "make_otu_heatmap end">> ./monitor.txt
echo "summarize_taxa_through_plots" >>./monitor.txt
date>>./monitor.txt
echo "plot_taxa_summary:chart_type pie,bar" > taxa_params.txt
summarize_taxa_through_plots.py -i otus/otu_table_ns.biom -o wf_taxa_summary -m $MAPPING_FILE -p taxa_params.txt
date>>./monitor.txt
echo "summarize_taxa_through_plots end">>./monitor.txt
echo "alpha_rarefaction">>./monitor.txt
date>>./monitor.txt
echo "alpha_diversity:metrics shannon,PD_whole_tree,chao1,observed_species" >alpha_params.txt
alpha_rarefaction.py -i otus/otu_table_ns.biom -m $MAPPING_FILE -o wf_arare/ -p alpha_params.txt -t otus/rep_set.tre
date>>./monitor.txt
echo "alpha_rarefaction end">>./monitor.txt
