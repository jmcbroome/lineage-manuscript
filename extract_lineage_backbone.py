import bte
import argparse

def argparser():
    parser = argparse.ArgumentParser(description='Extract the set of nodes with lineage annotations from a MAT and export it to another MAT or nextstrain JSON format.')
    parser.add_argument("-i","--input",help="Name of the input MAT protobuf.",required=True)
    parser.add_argument("-o","--output",help="Name of the output file.",required=True)
    parser.add_argument("-j","--json",action='store_true',help='Use to export in Auspice JSON instead of MAT pb format.')
    return parser.parse_args()

def main():
    args = argparser()
    t = bte.MATree(args.input)
    nodes_to_keep = list(t.dump_annotations().values())
    if args.json:
        t.write_json(args.output,nodes_to_keep)
    else:
        subtree = t.subtree(nodes_to_keep)
        subtree.save_pb(args.output)

if __name__ == "__main__":
    main()