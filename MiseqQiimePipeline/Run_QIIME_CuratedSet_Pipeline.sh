#QIIME Pipeline for Curated Data
# 
# Original version (mizilliox, 2013-03-08)
# Input filenames factored out, comments added, (this version not yet tested) (pthomas, 2013-03-10) 

MAPPING_FILE = AllMockCom_map.txt
FASTA_DATA_DIRECTORY = data

echo "add_qiime_labels" > ./monitor.txt
date >> ./monitor.txt
add_qiime_labels.py -i $FASTA_DATA_DIRECTORY -m $MAPPING_FILE -o combined_fasta
date >> ./monitor.txt
echo "add_qiime_labels end" >> ./monitor.txt
echo "pick_otus" >> ./monitor.txt
date>>./monitor.txt
pick_otus_through_otu_table.py -i combined_fasta/combined_seqs.fna -o otus
date>>./monitor.txt
echo "pick_otus end">>./monitor.txt
echo "filter_otus">>./monitor.txt
date>>./monitor.txt
filter_otus_from_otu_table.py -i otus/otu_table.biom -o otus/otu_table_ns.biom -n 2
date>>./monitor.txt
echo "filter_otus end">> ./monitor.txt
echo "per_library_stats">>./monitor.txt
date>>./monitor.txt
per_library_stats.py -i otus/otu_table.biom
date>>./monitor.txt
echo "per_library_stats end">>./monitor.txt
echo "sort_otu_table">>./monitor.txt
date>>./monitor.txt
sort_otu_table.py -i otus/otu_table.biom -o sorted_otu_table.biom -l $MAPPING_FILE
date>>./monitor.txt
echo "sort_otu_table end">>./monitor.txt
echo "make_otu_heatmap">>./monitor.txt
date>>./monitor.txt
make_otu_heatmap_html.py -i sorted_otu_table.biom -o otus/OTU_Heatmap/
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