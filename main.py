import argparse
import sys
import requests
import bs4

parser = argparse.ArgumentParser(description='Pass your UCSB GOLD login information')

parser.add_argument('-u', '--user')
parser.add_argument('-p', '--password')
parser.add_argument('-o', '--old', action='store_true')

args = parser.parse_args(sys.argv[1:])

r = requests.get('https://my.sa.ucsb.edu/gold/login.aspx')
soup = bs4.BeautifulSoup(r.text, 'html.parser')
hidden = [[x['name'], x['value']] for x in soup.find_all('input') if x['type'] == 'hidden']
null = [print(x) for x in hidden]

hiddenBody = '&'.join(x[0] + '=' + requests.utils.quote(x[1], safe='') for x in hidden)
creds = [
    'ctl00%24pageContent%24PermPinLogin%24userNameText=' + args.user,
    'ctl00%24pageContent%24PermPinLogin%24passwordText=' + args.password,
    'ctl00%24pageContent%24PermPinLogin%24loginButton.x=0'
    'ctl00%24pageContent%24PermPinLogin%24loginButton.y=0'
]
credsBody = '&'.join(creds)
body = hiddenBody + credsBody
print(body)