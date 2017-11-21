import requests
import grequests
import login
import bs4


cookie = login.cookie


def resoup(r):
    return bs4.BeautifulSoup(r.text, 'html.parser')


def quarterscrape():
    global soup
    quarter_list = [x['value'] for x in soup.find(id='pageContent_quarterDropDown').find_all('option')]
    return quarter_list


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
    course_url = 'https://my.sa.ucsb.edu/gold/BasicFindCourses.aspx'
    greq = grequests.post(course_url, headers=head, data=form_body, cookies=cookie)

    return greq


def init():
    global cookie

    course_url = 'https://my.sa.ucsb.edu/gold/BasicFindCourses.aspx'
    r = requests.get(course_url, cookies=cookie, allow_redirects=False)
    return r


def getrequests(alist):
    global cookie

    return (search(x[0], x[1]) for x in alist)


def getrequestslist(alist):
    global cookie

    return [search(x[0], x[1]) for x in alist]


def mapreq(reqs):
    return grequests.map(reqs, size=32)


soup = resoup(init())
departments = departmentscrape()
quarters = quarterscrape()
qurtDepts = [[x, y] for x in quarters for y in departments]
