import argparse
import sys


def parse():
    parser = argparse.ArgumentParser(description='Pass your UCSB GOLD login information')

    parser.add_argument('-u', '--user')
    parser.add_argument('-p', '--password')
    parser.add_argument('-o', '--old', action='store_true')

    argv = parser.parse_args(sys.argv[1:])

    return argv

args = parse()