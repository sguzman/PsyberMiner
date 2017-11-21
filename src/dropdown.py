def quarters(soup):
    quarters = [x['value'] for x in soup.find(id='pageContent_quarterDropDown').find_all('option')]
    return quarters


def departments(soup):
    depts = [x['value'] for x in soup.find(id='pageContent_subjectAreaDropDown').find_all('option')][1:]
    return depts