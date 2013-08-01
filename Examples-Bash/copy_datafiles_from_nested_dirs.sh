#Or just use: 
#find . -name "target.txt" -exec echo {} \;
#you can skim the man page to get an idea of what it's doing
#there's an EXAMPLES section at the bottom
#http://linux.die.net/man/1/find
 
#!/bin/bash
#set up program configuration
TARGET_FILE_GLOB="*_L5.txt"
DATAFILE_DUMP_DIR="All_L5"
TOP_LEVEL_DIR_PREFIX="ABC_"
NESTED_DIR_SUFFIX="_Qiime"

mkdir -p $DATAFILE_DUMP_DIR

echo "Copying all $TARGET_FILE_GLOB files..."
echo " ... out of nested directories that look like: $TOP_LEVEL_DIR_PREFIX*/$TOP_LEVEL_DIR_PREFIX*$NESTED_DIR_SUFFIX/wf_taxa_summary/"
echo " ... and into $DATAFILE_DUMP_DIR/$TOP_LEVEL_DIR_PREFIX*_L5.txt"

for sample_dir in $(ls -d $TOP_LEVEL_DIR_PREFIX*)
do
	cp $sample_dir/$sample_dir$NESTED_DIR_SUFFIX/wf_taxa_summary/$TARGET_FILE_GLOB $DATAFILE_DUMP_DIR/${sample_dir}_L5.txt
	
done

