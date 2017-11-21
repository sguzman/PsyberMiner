import re
import search
import soup


def current_term_search():
    greqs = search.getrequestslist(['20174', i] for i in search.departments)
    getty = search.mapreq(greqs)
    return getty


def newlinerep(alist: list, n: int):
    return [re.sub('\n' * n, 'WILLSPLITHERE', i) for i in alist]


def process():
    getty = current_term_search()
    courses = []
    for g in getty:
        if g.url != 'https://my.sa.ucsb.edu/gold/ResultsFindCourses.aspx':
            print('Logged out :(')
            continue
        s = soup.re(g)
        coursetable = s.find(id='pageContent_CourseList')
        courses_text = coursetable.find_all(attrs={'class': 'datatable'})
        courses_text = [i.text.strip() for i in courses_text]
        if len(courses_text) is not 0:
            if len(courses_text[0]) is not 0:
                print(courses_text[0][0])
        else:
            print('Empty :(')
        courses_text = newlinerep(courses_text, 25)
        courses_text = newlinerep(courses_text, 24)
        courses_text = newlinerep(courses_text, 23)
        courses_text = newlinerep(courses_text, 10)
        courses_text = newlinerep(courses_text, 4)
        courses_text = [i.split('WILLSPLITHERE') for i in courses_text]
        courses_split = []
        for c in courses_text:
            course_item = []
            for row in c:
                newRow = row.strip().split('\n')
                course_item.append([x.strip() for x in newRow])
            courses_split.append(course_item)

        print('Got list', courses_split)
        courses.append(courses_split)

    return courses
