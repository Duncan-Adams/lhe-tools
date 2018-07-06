#!/usr/bin/env python3
###### TODO ######
## Figure out header stuff
## Write number of events written in header
## Write LHE version info at top
## add checks for bad inputs
## clean code
###################

import sys, argparse, os.path, time
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description="Split LHE file")
parser.add_argument("path", help="Path to lhe file")
parser.add_argument("tot_events", help="Number of total events in original LHE file", type=int)
parser.add_argument("evts_per_file", help="Number of events to write to each output file", type=int)
parser.add_argument("--keep_header", help="write lhe header to file", action="store_true")
args = parser.parse_args()

n_evts = args.tot_events
evts_per_file = args.evts_per_file

lhe_tree = ET.parse(args.path)
root = lhe_tree.getroot()

# Find Header and Init block
header = root.find('header')
init = root.find('init')

#For every n_events, make a file
no_files = n_evts/evts_per_file
extra_evts = n_evts % evts_per_file

evt_i = 0
events = root.findall('event')

for f_i in range(int(no_files)):
    out_file = open('out_lhe_' + str(f_i) + '.lhe', 'w')
    
    if args.keep_header:
        out_file.write(ET.tostring(header).decode('utf-8'))
    out_file.write(ET.tostring(init).decode('utf-8'))

    for i in range(evts_per_file):
        out_file.write(ET.tostring(events[i + f_i*evts_per_file]).decode('utf-8'))

    out_file.close()


if extra_evts > 0:
    #loop counters don't go out of scope in python :)
    f_i += 1

    out_file = open('out_lhe_' + str(f_i) + '.lhe', 'w')
    
    if args.keep_header:
        out_file.write(ET.tostring(header).decode('utf-8'))
    out_file.write(ET.tostring(init).decode('utf-8'))

    for i in range(int(extra_evts)):
        out_file.write(ET.tostring(events[i + f_i*evts_per_file]).decode('utf-8'))

    out_file.close()

