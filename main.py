import argparse
import sys
import requests
import bs4

parser = argparse.ArgumentParser(description='Pass your UCSB GOLD login information')

parser.add_argument('-u', '--user')
parser.add_argument('-p', '--pass')
parser.add_argument('-o', '--old', action='store_true')

args = parser.parse_args(sys.argv[1:])

r = requests.get('https://my.sa.ucsb.edu/gold/login.aspx')
soup = bs4.BeautifulSoup(r.text, 'html.parser')
print(soup.prettify())
