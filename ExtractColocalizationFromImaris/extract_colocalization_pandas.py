__author__ = 'psthomas'

import sys
import os
import re
import csv
import pandas as pd
import itertools
import pprint
import logging
logging.basicConfig(filename='extract_colocalization.log',level=logging.INFO)


r"""
Extracts colocalization data from each channel of an Imaris run and writes summary files to current dir.
Requires a config file called EXPERIMENT_CONFIG.cfg

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
    timepoint_metadata = get_timepoint_metadata(config)

    for timepoint_metadatum in timepoint_metadata:
        path = timepoint_metadata_to_datafile_path(config, timepoint_metadatum)
        if not os.path.exists(path):
            print "File not found for {}: {}".format(timepoint_metadatum, path)


def get_timepoint_metadata(config):
    """
    Using details in the config file, combine all the dimensions of data (eg, viruses, channels, timepoints, cells)
    and produce a list of all the valid measurements to include in the summary.

    Result is a list of (channel, virus, timepoint, cell) entries.
    Can be turned into a path to the file using timepoint_metadata_to_datafile_path()
    """
    timepoint_metadata = []
    for channel in [1]:  # only care about the virus-centric channel right now (channel 1)
        for virus in config.viruses:
            for timepoint in config.timepoints:
                for cell in config.timepointcells[timepoint]:
                    timepoint_metadata.append((channel, virus, timepoint, cell))

    return timepoint_metadata


def timepoint_metadata_to_datafile_path(config, timepoint_metadata):
    channel, virus, timepoint, cell = timepoint_metadata
    datafile_path = os.path.join(config.target_dir,
                                 config.channel_dirname_pattern.format(channel_num=channel),
                                 config.timepoint_dirname_pattern.format(timepoint=timepoint, virus=virus,
                                                                         cell_num=cell),
                                 config.timepoint_filename_pattern.format(timepoint=timepoint, virus=virus,
                                                                          cell_num=cell, channel_num=channel))
    return datafile_path


class ExperimentConfig(object):
    def __init__(self, config_parser):
        self.target_dir = ""
        self.experiment_name = config_parser.get("config", "experiment_name")
        self.channels = [int(c) for c in config_parser.get("config", "channels").split(",")]
        self.viruses = [v.strip() for v in config_parser.get("config", "viruses").split(",")]
        self.timepointcells = {}
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
    config_parser.read(os.path.join(target_dir, "EXPERIMENT_CONFIG2.cfg"))
    config = ExperimentConfig(config_parser)
    config.target_dir = target_dir
    config.channel_thresholds = {}
    for channel in config.channels:
        config.channel_thresholds[channel] = config_parser.getint("config", "channel{}_threshold".format(channel))
        config.channel_names[channel] = config_parser.get("config", "channel{}_name".format(channel))
    for timepoint in config.timepoints:
        config.timepointcells[timepoint] = [int(c) for c in config_parser.get(
            "config", "timepoint{}_cells".format(timepoint)).split(",")]

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