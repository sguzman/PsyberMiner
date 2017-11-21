import re
import search


greqs = search.getrequestslist(['20174', i] for i in search.departments)

getty = search.map(greqs)
for g in getty:
    soup = search.resoup(g)
    coursetable = soup.find(id='pageContent_CourseList')
    coursesText = coursetable.find_all(attrs={'class': 'datatable'})
    coursesText = [i.text.strip() for i in coursesText]
    coursesText = [re.sub('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', 'WILLSPLITHERE', i) for i in
                   coursesText]
    coursesText = [re.sub('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', 'WILLSPLITHERE', i) for i in coursesText]
    coursesText = [re.sub('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n', 'WILLSPLITHERE', i) for i in coursesText]
    coursesText = [re.sub('\n\n\n\n\n\n\n\n\n\n', 'WILLSPLITHERE', i) for i in coursesText]
    coursesText = [re.sub('\n\n\n\n', 'WILLSPLITHERE', i) for i in coursesText]
    coursesText = [i.split('WILLSPLITHERE') for i in coursesText]
    print(coursesText)
