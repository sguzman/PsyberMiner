import argparse
import sys
import requests
import bs4
import re

parser = argparse.ArgumentParser(description='Pass your UCSB GOLD login information')

parser.add_argument('-u', '--user')
parser.add_argument('-p', '--password')
parser.add_argument('-o', '--old', action='store_true')

args = parser.parse_args(sys.argv[1:])

loginUrl = 'https://my.sa.ucsb.edu/gold/login.aspx'
r = requests.get(loginUrl)
soup = bs4.BeautifulSoup(r.text, 'html.parser')

hidden = [[x['name'], x['value']] for x in soup.find_all('input') if x['type'] == 'hidden'] + ([
    ['ctl00%24pageContent%24PermPinLogin%24userNameText', args.user],
    ['ctl00%24pageContent%24PermPinLogin%24passwordText', args.password],
    ['ctl00%24pageContent%24PermPinLogin%24loginButton.x', '0'],
    ['ctl00%24pageContent%24PermPinLogin%24loginButton.y', '0']
]) if args.old else ([
    ['ctl00%24pageContent%24userNameText', args.user],
    ['ctl00%24pageContent%24passwordText', args.password],
    ['ctl00%24pageContent%24loginButton.x', '0'],
    ['ctl00%24pageContent%24loginButton.y', '0']
])

preBody = [x[0] + '=' + requests.utils.quote(x[1], safe='') for x in hidden]
body = '&'.join(preBody)

head = {'Content-Type': 'application/x-www-form-urlencoded'}
r = requests.post(loginUrl, headers=head, data=body, cookies=r.cookies, allow_redirects=False)

cookie = r.cookies

courseUrl = 'https://my.sa.ucsb.edu/gold/BasicFindCourses.aspx'
resultsUrl = 'https://my.sa.ucsb.edu/gold/ResultsFindCourses.aspx'
r = requests.get(courseUrl, cookies=cookie, allow_redirects=False)
soup = bs4.BeautifulSoup(r.text, 'html.parser')

quarters = [x['value'] for x in soup.find(id='pageContent_quarterDropDown').find_all('option')]
depts = [x['value'] for x in soup.find(id='pageContent_subjectAreaDropDown').find_all('option')][1:]


def search(quarter, dept):
    formHidden = [[x['name'], x['value']] for x in soup.find_all('input') if x['type'] == 'hidden'] + [
        ['ctl00%24pageContent%24quarterDropDown', str(quarter)],
        ['ctl00%24pageContent%24subjectAreaDropDown', str(dept)],
        ['ctl00%24pageContent%24searchButton.x', '0'],
        ['ctl00%24pageContent%24searchButton.y', '0']
    ]

    form = [x[0] + '=' + requests.utils.quote(x[1], safe='') for x in formHidden]
    formBody = '&'.join(form)
    r = requests.post(courseUrl, headers=head, data=formBody, cookies=cookie, allow_redirects=False)
    r = requests.get(resultsUrl, cookies=cookie, allow_redirects=False)

    return r


qurtDepts = [[x, y] for x in quarters for y in depts]

r = search(quarters[0], depts[0])
soup = bs4.BeautifulSoup(r.text, 'html.parser')
coursetable = soup.find(id='pageContent_CourseList')
courses = coursetable.find_all(attrs={'class': 'datatable'})
for i in courses:
    print(i.text)
