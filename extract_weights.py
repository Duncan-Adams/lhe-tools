#!/usr/bin/env python3

import sys, argparse, os.path, time
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description="Split LHE file")
parser.add_argument("path", help="Path to lhe file")
parser.add_argument("outfile", help="Path to output file")
args = parser.parse_args()

lhe_tree = ET.parse(args.path)
root = lhe_tree.getroot()

# Find Header and Init block
header = root.find('header')
init = root.find('init')

out_file = open(args.outfile, 'w')

out_file.write("<LesHouchesEvents version=\"3.0\">\n")
out_file.write(ET.tostring(header).decode('utf-8'))

for event in root.findall('event'):
    out_file.write(ET.tostring(event.find('mgrwt')).decode('utf-8'))
    out_file.write(ET.tostring(event.find('rwgt')).decode('utf-8'))

out_file.write("</LesHouchesEvents>\n")
   
out_file.close()
