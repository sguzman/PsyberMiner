import requests
import grequests
import bs4
import re
import argv
import login
import dropdown

args = argv.parse()
cookie = login.cookie(args)

courseUrl = 'https://my.sa.ucsb.edu/gold/BasicFindCourses.aspx'
resultsUrl = 'https://my.sa.ucsb.edu/gold/ResultsFindCourses.aspx'
r = requests.get(courseUrl, cookies=cookie, allow_redirects=False)
soup = bs4.BeautifulSoup(r.text, 'html.parser')

quarts = dropdown.quarters(soup)
depts = dropdown.departments(soup)


def search(quarter, dept):
    form_hidden = [[x['name'], x['value']] for x in soup.find_all('input') if x['type'] == 'hidden'] + [
        ['ctl00%24pageContent%24quarterDropDown', str(quarter)],
        ['ctl00%24pageContent%24subjectAreaDropDown', str(dept)],
        ['ctl00%24pageContent%24searchButton.x', '0'],
        ['ctl00%24pageContent%24searchButton.y', '0']
    ]

    form = [x[0] + '=' + requests.utils.quote(x[1], safe='') for x in form_hidden]
    form_body = '&'.join(form)
    greq = grequests.post(courseUrl, headers=head, data=form_body, cookies=cookie)

    return greq


qurtDepts = [[x, y] for x in quarters for y in depts]
gRequests = [search('20174', i) for i in depts]

getty = grequests.map(gRequests, size=32)
for g in getty:
    soup = bs4.BeautifulSoup(g.text, 'html.parser')
    coursetable = soup.find(id='pageContent_CourseList')
    courses = coursetable.find_all(attrs={'class': 'datatable'})
    coursesText = [i.text.strip() for i in courses]
    coursesText = [re.sub('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', 'WILLSPLITHERE', i) for i in
                   coursesText]
    coursesText = [re.sub('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', 'WILLSPLITHERE', i) for i in coursesText]
    coursesText = [re.sub('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', 'WILLSPLITHERE', i) for i in coursesText]
    coursesText = [re.sub('\n\n\n\n\n\n\n\n\n\n', 'WILLSPLITHERE', i) for i in coursesText]
    coursesText = [re.sub('\n\n\n\n', 'WILLSPLITHERE', i) for i in coursesText]
    coursesText = [i.split('WILLSPLITHERE') for i in coursesText]
