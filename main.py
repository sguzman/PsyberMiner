import argparse
import sys

parser = argparse.ArgumentParser(description='Pass your UCSB GOLD login information')

parser.add_argument('--user')
parser.add_argument('--pass')
parser.add_argument('--old', action='store_true')

args = parser.parse_args(sys.argv[1:])
print(args)
