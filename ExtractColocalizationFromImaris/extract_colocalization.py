__author__ = 'psthomas'

import sys
import os
import re
import csv
import itertools
import pprint
import logging
logging.basicConfig(filename='extract_colocalization.log',level=logging.INFO)


r"""
Extracts colocalization data from each channel of an Imaris run and writes summary files to current dir.
Requires a config file called EXPERIMENT_CONFIG.cfg and expects to find it at the top of the data dir

Expects directory structure like:
    2013.08.10\                                                 # date of start of experiment
        Virus Gate\                                             # dir of data for this gate (channel), eg Virus, Lc3, Gal3
            1h-104-1_R3D_D3D_Statistics\                        # multiple dirs in the form <timepoint>-<virus number>-<cell number>
                1h-104-1_R3D_D3D_Intensity_Max_Ch=1.csv         # File giving max intensity of each point present in this gate
                1h-104-1_R3D_D3D_Intensity_Max_Ch=2.csv         # File giving max intensity of other points colocalized with points in 1h-104-1_R3D_D3D_Intensity_Max_Ch=1.csv
                1h-104-1_R3D_D3D_Intensity_Max_Ch=3.csv         # File giving max intensity of other points colocalized with points in 1h-104-1_R3D_D3D_Intensity_Max_Ch=1.csv
        LC3 Gate\
            1h-104-1_R3D_D3D_Statistics\
                1h-104-1_R3D_D3D_Intensity_Max_Ch=1.csv
                1h-104-1_R3D_D3D_Intensity_Max_Ch=2.csv
                1h-104-1_R3D_D3D_Intensity_Max_Ch=3.csv
        Gal3 Gate
            1h-104-1_R3D_D3D_Statistics\
                1h-104-1_R3D_D3D_Intensity_Max_Ch=1.csv
                1h-104-1_R3D_D3D_Intensity_Max_Ch=2.csv
                1h-104-1_R3D_D3D_Intensity_Max_Ch=3.csv

Sample EXPERIMENT_CONFIG.cfg file:
---------------
[config]
experiment_name: 2013.08.10
channels: 1,2,3
viruses: 104,Ad12
timepoints: 05,1,2,4
cells: 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
channel_dirname_pattern: ch{channel_num}
timepoint_dirname_pattern: {timepoint}h-{virus}-{cell_num}_R3D_D3D_Statistics
timepoint_filename_pattern: {timepoint}h-{virus}-{cell_num}_R3D_D3D_Intensity_Max_Ch={channel_num}.csv
channel1_threshold: 200
channel2_threshold: 300
channel3_threshold: 300
channel1_name: Virus
channel2_name: Gal3
channel3_name: LC3
---------------


"""


def main(target_dir):
    #channels, timepoints, virus_nums, cell_nums = load_experiment_config(target_dir)
    config = load_experiment_config(target_dir)
    logging.debug(pprint.pformat(config.__dict__))

    for channel in [1]: #config.channels:
        print "[*] Processing colocalization of channel {}".format(channel)
        channel_localization_summary = {}
        datapoints = itertools.product(config.timepoints, config.viruses, config.cells)
        coloc_rollup = []
        for timepoint, virus, cell in datapoints:
                datafile_dir = os.path.join(target_dir,
                                            config.channel_dirname_pattern.format(channel_num=channel),
                                            config.timepoint_dirname_pattern.format(timepoint=timepoint, virus=virus,
                                                                                    cell_num=cell))
            try:
                colo_dict = compute_timepoint_colocalization(datafile_dir, timepoint, virus, cell, config)
                coloc_rollup.append(ColocalizationData(virus, channel, cell, timepoint, data=colo_dict))
            except IOError as e:
                logging.error(e)
                print e

        # Roll up statistics in order to make coloc over time csvs
        for virus in config.viruses:
            channel_combos = [(1,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
            for channel_combo in channel_combos:
                channel_combo_name = "+".join([config.channel_names[i] for i in channel_combo])
                channel_combo_numeric = "+".join([str(i) for i in channel_combo])
                filename = "{}_{}_{}.csv".format(config.experiment_name, virus, channel_combo_name)
                with open(filename, "wb") as outfile:
                    csvwriter = csv.DictWriter(outfile, fieldnames=["cell_id"] + config.timepoints)
                    print "[*] Writing colocalization summary file {}".format(filename)
                    csvwriter.writeheader()
                    for cell in sorted(config.cells):
                        relevant_records = [cr for cr in coloc_rollup if cr.cell == cell and cr.virus == virus]
                        row_data = {d.timepoint: d.data[channel_combo_numeric] for d in relevant_records}
                        row_data["cell_id"] = str(cell)
                        #print row_data
                        csvwriter.writerow(row_data)

        # Roll up statistics again, this time doing virus/coloc virus
        for virus in config.viruses:
            channel_combos = [(1, 2), (1, 3), (2, 3), (1, 2, 3)]
            for channel_combo in channel_combos:
                channel_combo_name = "+".join([config.channel_names[i] for i in channel_combo])
                channel_combo_numeric = "+".join([str(i) for i in channel_combo])
                filename = "{}_{}_{}_percent.csv".format(config.experiment_name, virus, channel_combo_name)
                with open(filename, "wb") as outfile:
                    csvwriter = csv.DictWriter(outfile, fieldnames=["cell_id"] + config.timepoints)
                    print "[*] Writing colocalization summary file {}".format(filename)
                    csvwriter.writeheader()
                    for cell in sorted(config.cells):
                        relevant_records = [cr for cr in coloc_rollup if cr.cell == cell and cr.virus == virus]
                        row_data = {d.timepoint: (d.data["1"] / float(d.data[channel_combo_numeric]))
                                    if d.data[channel_combo_numeric] != 0 else ""
                                    for d in relevant_records}
                        row_data["cell_id"] = str(cell)
                        #print row_data
                        csvwriter.writerow(row_data)



def compute_timepoint_colocalization(datafile_dir, timepoint, virus, cell, config):
    """
    Compute raw colocalization data for this timepoint and return a
    Writes colocalization_raw.csv to timepoint_dir and returns a dict of colocalization summary
    Return looks like: {'1': 12, '3': 14, '2': 13, '1+2+3': 11, '4': 0, '2+3': 13, '1+3': 12, '1+2': 11}
    """

    points = {}  # id -> {<ch>: <intensity>}

    # extract intensity data from channel data files
    for channel in config.channels:
        datafile_name = config.timepoint_filename_pattern.format(timepoint=timepoint, virus=virus,
                                                                 cell_num=cell, channel_num=channel)
        #print datafile_name
        datafile = open(os.path.join(datafile_dir, datafile_name), "rb")
        dictreader = csv.DictReader(datafile, ["Value", "Unit", "Category", "Channel", "Time", "ID"])
        dictreader.next()  # discard 4 junk rows at the top of each file
        dictreader.next()
        dictreader.next()
        for row in dictreader:
            point = points.setdefault(int(row["ID"]), {"id": row["ID"]})
            point[str(channel)] = float(row["Value"])
            #print point

    logging.info("[*] Processing intensity data for timepoint={}, virus={}, cell={}".format(timepoint, virus, cell))
    # process intensity data to identify colocalization
    # also produce colocalization summary for return
    CHANNEL_THRESHOLDS = {1: 200, 2: 300, 3: 300}
    colocalization_summary = {"1": 0, "2": 0, "3": 0, "4": 0, "1+2": 0, "1+3": 0, "2+3": 0, "1+2+3": 0}
    for point in points.values():
        point["1+2"] = point["1"] >= CHANNEL_THRESHOLDS[1] and point["2"] >= CHANNEL_THRESHOLDS[2]
        point["1+3"] = point["1"] >= CHANNEL_THRESHOLDS[1] and point["3"] >= CHANNEL_THRESHOLDS[3]
        point["2+3"] = point["2"] >= CHANNEL_THRESHOLDS[2] and point["3"] >= CHANNEL_THRESHOLDS[3]
        point["1+2+3"] = point["1+2"] and point["1+3"] and point["2+3"]

        colocalization_summary["1"] += 1 if point["1"] >= CHANNEL_THRESHOLDS[1] else 0
        colocalization_summary["2"] += 1 if point["2"] >= CHANNEL_THRESHOLDS[2] else 0
        colocalization_summary["3"] += 1 if point["3"] >= CHANNEL_THRESHOLDS[3] else 0

        colocalization_summary["1+2"] += 1 if point["1+2"] else 0
        colocalization_summary["1+3"] += 1 if point["1+3"] else 0
        colocalization_summary["2+3"] += 1 if point["2+3"] else 0
        colocalization_summary["1+2+3"] += 1 if point["1+2+3"] else 0

    # emit raw colocalization data
    with open(os.path.join(datafile_dir, 'colocalization_raw.csv'), 'wb') as outfile:
        dictwriter = csv.DictWriter(outfile, fieldnames=["id", "1", "2", "3", "4", "1+2", "1+3", "2+3", "1+2+3"])
        dictwriter.writeheader()
        for point_id in sorted(points.keys()):
            dictwriter.writerow(points[point_id])

    return colocalization_summary

class ExperimentConfig(object):
    def __init__(self, config_parser):
        self.experiment_name = config_parser.get("config", "experiment_name")
        self.channels = [int(c) for c in config_parser.get("config", "channels").split(",")]
        self.viruses = [v.strip() for v in config_parser.get("config", "viruses").split(",")]
        self.cells = [int(c) for c in config_parser.get("config", "cells").split(",")]
        self.timepoints = [t.strip() for t in config_parser.get("config", "timepoints").split(",")]
        self.channel_dirname_pattern = config_parser.get("config", "channel_dirname_pattern")
        self.timepoint_dirname_pattern = config_parser.get("config", "timepoint_dirname_pattern")
        self.timepoint_filename_pattern = config_parser.get("config", "timepoint_filename_pattern")
        self.channel_thresholds = {}
        self.channel_names = {}


class ColocalizationData(object):
    def __init__(self, virus, channel, cell, timepoint, data=None):
        self.virus = virus
        self.channel = channel
        self.cell = cell
        self.timepoint = timepoint
        self.data = data

    def __str__(self):
        return "<ColocalizationData virus={} channel={} cell={} timepoint={} data={}>".format(
            self.virus, self.channel, self.cell, self.timepoint, pprint.pformat(self.data)
        )

def load_experiment_config(target_dir):
    from ConfigParser import RawConfigParser
    config_parser = RawConfigParser()
    config_parser.read(os.path.join(target_dir, "EXPERIMENT_CONFIG.cfg"))
    config = ExperimentConfig(config_parser)
    config.channel_thresholds = {}
    for channel in config.channels:
        config.channel_thresholds[channel] = config_parser.getint("config", "channel{}_threshold".format(channel))
        config.channel_names[channel] = config_parser.get("config", "channel{}_name".format(channel))
    return config

def usage():
    print "Usage: {} dir".format(sys.argv[0])
    print "\nConsume the Imaris data from dir and generate colocalization summary files"
    print "Requires a config file called EXPERIMENT_PARAMETERS in the experiment root directory (dir)"
    print "See docs in this file for example"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        usage()