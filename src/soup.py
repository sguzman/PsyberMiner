import bs4

def re(r):
    return bs4.BeautifulSoup(r.text, 'html.parser')