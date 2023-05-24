import bte
import sys
import argparse

parser = argparse.ArgumentParser(description='Process some data.')
parser.add_argument('-a','--annotation_file', type=str,
                    help='Path to a tab-delimited file containing sample annotation pairs')
parser.add_argument('-t','--tree', type=str,
                    help='Path to a MAT file with a .pb extension, optionally gzipped (*.pb.gz)')

args = parser.parse_args()

def parse_clade_set(cf):
    clades = set()
    with open(cf) as inf:
        for entry in inf:
            spent = entry.strip().split()
            clades.add(spent[1])
    return clades
sd = parse_clade_set(args.annotation_file)
t = bte.MATree(args.tree)
annd = t.dump_node_annotations()
for nid, annv in annd.items():
    annd[nid] = [a for a in annv if a in sd]
t.apply_node_annotations(annd)
t.save_pb('cleaned.'+args.tree)