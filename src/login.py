import requests
import bs4


def cookie(args):
    login_url = 'https://my.sa.ucsb.edu/gold/login.aspx'
    r = requests.get(login_url)
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

    pre_body = [x[0] + '=' + requests.utils.quote(x[1], safe='') for x in hidden]
    body = '&'.join(pre_body)

    head = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(login_url, headers=head, data=body, cookies=r.cookies, allow_redirects=False)

    return r
