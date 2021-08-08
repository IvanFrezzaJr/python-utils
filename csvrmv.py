#!/usr/bin/env python
import os
import csv
import argparse

def main(args:argparse.Namespace):
    input = args.input
    output = args.out
    pattern = args.pattern

    _cleanup_csv(input, output, pattern)

def _cleanup_csv(input:str, output:str, pattern:str) -> None:  

    if input == output:
        print("input and output should be different")
        return False

    if not os.path.isfile(input):
        print("File not found.")
        return False

    filename = os.path.basename(input) 
    output_file = build_output_file(input, filename)
    if output:
        output_file = build_output_file(output, filename)
    
    with open(input, "r", newline='') as infile, open(output_file, "w") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        conversion = set(pattern)
        for row in reader:
            newrow = [''.join(' ' if c in conversion else c for c in entry) for entry in row]
            writer.writerow(newrow)


def build_output_file(path, name):
        dirname = os.path.dirname(path)
        return os.path.join(dirname, "repaired-" + name)

if "__main__" == __name__:
    """run main funciotn

    cmd e.g: python csvrmv.py -i path/to/file.csv -o dir/to/save -p \n\t
    """
    parser = argparse.ArgumentParser(description='Clean up the csv.')
    parser.add_argument('-i', '--input', required=True, type=str, help='Path to .csv file to clean')
    parser.add_argument('-o', '--out', required=False, default=".", type=str, help='path to save the output csv')
    parser.add_argument('-p', '--pattern', required=False, type=str, default="\n", help='List of characters to remove from csv')
    args = parser.parse_args()
    main(args)