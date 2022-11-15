from httpx import Client
from bs4 import BeautifulSoup
import os
# from util import try_soup_select_text, try_select
import base64
# from rich import print

output_dir = os.path.join(os.path.dirname(__file__), 'results')


col_names = ['Appl', 'Goog', 'FB', 'Wind', 'Twtr', 'Joy', 'Sams', 'GMail', 'SB', 'DCM', 'KDDI']
col_names = [os.path.join(output_dir, col) for col in col_names]
for col in col_names:
    if not os.path.exists(col):
        os.makedirs(col)
        print(f'Created dir "{col}"')


def get_data():
    client = Client()
    url = 'https://unicode.org/emoji/charts/full-emoji-list.html'
    data = []
    res = client.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    body = soup.select('table')[0]

    for row in body.select('tr'):
        r_data = get_row(row)
        if r_data:
            data.append(r_data)
    return data


def get_row(row):
    cols = [i for i in row.select('td') if i != '\n']
    if not cols:
        return
    code = cols[1].text.replace(' ', '-')
    # print('Do row ' + code)
    col_data = {'code': code, 'icons': []}
    for i,col in enumerate(cols[3:-1]):
        # print(col_names[i])
        if col and col.img:
            src = col.img['src']
        else:
            src = None
        col_data['icons'].append(src)
        if col.get('colspan'):
            colspan = int(col['colspan'])
            for _ in range(1, colspan):
                col_data['icons'].append(src)
    return col_data


def download_img(src: str, dir: str, filename: str):
    head, data = src.split(',')
    file_ext = head.split(';')[0].split('/')[1]
    filename = os.path.join(dir, filename + '.' + file_ext)
    data = base64.b64decode(data)
    with open(filename, 'wb') as f:
        f.write(data)


def save_icons_from_data(data):
    for row in data:
        code = row['code']
        for i,i_data in enumerate(row['icons']):
            if i_data:
                download_img(i_data, col_names[i], code)


def main():
    data = get_data()
    save_icons_from_data(data)
    print("Saved all icons")

if __name__ == '__main__':
    main()
