import argparse
import sys

parser = argparse.ArgumentParser(description='Pass your UCSB GOLD login information')

parser.add_argument('-u', '--user')
parser.add_argument('-p', '--pass')
parser.add_argument('-o', '--old', action='store_true')

args = parser.parse_args(sys.argv[1:])
print(args)
