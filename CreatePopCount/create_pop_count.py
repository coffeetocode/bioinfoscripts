import os
import re
import sys
import csv
from collections import defaultdict
import pprint


"""
Turn a directory of files containing library match percent data into a 
single spreadsheet.

USAGE:
Pass target directory as only parameter.
> python create_pop_count.py .
Processed 5 samples with 379 total libraries.

INPUT: 

A directory of files with names like "Title_C003.txt", "Title_C004.txt" 
which contain lines like:
lib9	popfrac	0.345029
lib10	popfrac	0.289740
lib34	popfrac	0.165338
lib46	popfrac	0.116427
lib509	popfrac	0.010633
lib157	popfrac	0.007443

OUTPUT:
A single file CountTable.csv in the target directory which contains a column 
for every library that existed in any sample, and a row per sample of the 
percent from that sample's file.

Eg:
sample_name,lib_1,lib_10032,lib_10185,lib_102
C005,0.249803,0.0,0.0,0.0
C004,0.267776,0.0,0.0

TODO:
- This is an ugly way to do it, but it doesn't rely on scipy (installing that 
  is a nonstarted for some grad students). Pandas would make it cleaner for 
  sure.
- Should confirm that popfracs sum up to 100%
"""


INPUT_FILE_REGEX = re.compile("Title_(C\d+).txt")
OUTPUT_FILE_NAME = "CountTable.csv"


def load_samples(dir):
    samples = {}
    all_libraries = set()
    sample_filenames = [f for f in os.listdir(dir) if INPUT_FILE_REGEX.match(f)]
    
    for sample_filename in sample_filenames:
        sample_name, sample_data = parse_sample_file(sample_filename)
        samples[sample_name] = sample_data
        all_libraries.update(sample_data.keys())
    
    #pprint.pprint(samples)
    return samples, all_libraries

def parse_sample_file(sample_filename):
    sample_name = INPUT_FILE_REGEX.match(sample_filename).group(1)
    lines = open(sample_filename).readlines() 
    sample_data = defaultdict(float)
    for lib, percent in parse_sample_lines(lines):
        sample_data[lib] = percent
    #pprint.pprint(sample_data)
    sample_data["sample_name"] = sample_name
    return sample_name, sample_data

def parse_sample_lines(lines):
    line_parts = (line.split() for line in lines) # lib_1	pop_frac	0.267776
    return [(parts[0], parts[2]) for parts in line_parts] # (lib_1, 0.267776)
                       
def write_summary(samples, all_libraries, target_dir):
    #pprint.pprint(samples.keys())
    field_names = ["sample_name"] + list(sorted(all_libraries))
    csvfile = open(os.path.join(target_dir, 'CountTable.csv'), 'wb')
    csvwriter = csv.DictWriter(csvfile, fieldnames=field_names)
    csvwriter.writeheader()
    for sample_name, sample_values in samples.items():
        #print sample_name
        #print sample_name
        to_write = {k:sample_values[k] for k in all_libraries}
        #pprint.pprint(sample_values["lib_247"])
        csvwriter.writerow(to_write)
    csvfile.close()
    print "Processed {} samples with {} total libraries.".format(len(samples), len(all_libraries))

def usage():
    print "Usage: {} dir".format(sys.argv[0])

def main(dir):
    samples, all_libraries = load_samples(dir)
    write_summary(samples, all_libraries, dir)
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        usage()