import requests
import grequests
import login
import bs4


cookie = login.cookie


def resoup(r):
    return bs4.BeautifulSoup(r.text, 'html.parser')


def quarterscrape():
    global soup
    quarters = [x['value'] for x in soup.find(id='pageContent_quarterDropDown').find_all('option')]
    return quarters


def departmentscrape():
    global soup
    depts = [x['value'] for x in soup.find(id='pageContent_subjectAreaDropDown').find_all('option')][1:]
    return depts


def search(quarter, dept):
    global soup
    global cookie

    form_hidden = [[x['name'], x['value']] for x in soup.find_all('input') if x['type'] == 'hidden'] + [
        ['ctl00%24pageContent%24quarterDropDown', str(quarter)],
        ['ctl00%24pageContent%24subjectAreaDropDown', str(dept)],
        ['ctl00%24pageContent%24searchButton.x', '0'],
        ['ctl00%24pageContent%24searchButton.y', '0']
    ]

    head = {'Content-Type': 'application/x-www-form-urlencoded'}
    form = [x[0] + '=' + requests.utils.quote(x[1], safe='') for x in form_hidden]
    form_body = '&'.join(form)
    courseUrl = 'https://my.sa.ucsb.edu/gold/BasicFindCourses.aspx'
    greq = grequests.post(courseUrl, headers=head, data=form_body, cookies=cookie)

    return greq


def init():
    global cookie

    courseUrl = 'https://my.sa.ucsb.edu/gold/BasicFindCourses.aspx'
    r = requests.get(courseUrl, cookies=cookie, allow_redirects=False)
    return r


def getrequests(list):
    global cookie

    return (search(x[0], x[1]) for x in list)

def getrequestslist(list):
    global cookie

    return [search(x[0], x[1]) for x in list]


def map(reqs):
    return grequests.map(reqs, size=32)

soup = resoup(init())
departments = departmentscrape()
quarters = quarterscrape()
qurtDepts = [[x, y] for x in quarters for y in departments]
