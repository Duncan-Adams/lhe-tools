#!/usr/bin/env python3

import sys, argparse, os.path, time
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description="Split LHE file")
parser.add_argument("path", help="Path to lhe file")
parser.add_argument("weights", help="Path to weights file")
parser.add_argument("outfile", help="Path to output file")
args = parser.parse_args()

lhe_tree = ET.parse(args.path)
lhe_root = lhe_tree.getroot()

weight_tree = ET.parse(args.weights)
weight_root = weight_tree.getroot()

# Find Header and Init block
header = weight_root.find('header')
init = lhe_root.find('init')

out_file = open(args.outfile, 'w')

out_file.write("<LesHouchesEvents version=\"3.0\">\n")
out_file.write(ET.tostring(header).decode('utf-8'))
out_file.write(ET.tostring(init).decode('utf-8'))

mgrwt = weight_root.findall('mgrwt')
rwgt = weight_root.findall('rwgt')



for i, event in enumerate(lhe_root.findall('event')):
    event_str = ET.tostring(event).decode('utf-8')
    event_str = event_str[:-9]
    out_file.write(event_str)
    out_file.write(ET.tostring(mgrwt[i]).decode('utf-8'))
    out_file.write(ET.tostring(rwgt[i]).decode('utf-8'))
    out_file.write('</event>\n')
    
out_file.write("</LesHouchesEvents>\n")
   
out_file.close()
