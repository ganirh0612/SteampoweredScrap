import os

import pandas as pd
import requests
import bs4
import json

url = 'https://store.steampowered.com/search/?snr=1_4_4__12&term=Counter+Strike'

def get_data(url):
    r = requests.get(url)
    return r.text

# Processing Data
def parse(data):
    result = []
    soup = bs4.BeautifulSoup(data, 'html.parser')

    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

    contents = soup.find('div', attrs={'id': 'search_resultsRows'})
    games = contents.find_all('a')

    for game in games:
        link = game['href']

    # Parsing Data
        title = game.find('span', {'class': 'title'}).text.strip().split('£')[0]
        price = game.find('div', {'class': 'search_price'}).text.strip().split('£')[0]
        release = game.find('div', {'class': 'search_released'}).text.strip().split('£')[0]

        if release == '':
            release = 'None'

    # Sorting Data
        data_dict = {
            'title' : title,
            'price' : price,
            'release' : release,
            'link'  : link
    }

# Append
        result.append(data_dict)
    return result

# Writing json
    with open('json_result.json', 'w') as outfile:
        json.dump(result, outfile)
    return result

# Read json
def load_data():
    with open('json_result.json') as json_file:
        data = json.load(json_file)

# Clean Data Process from Parser
def output(gameData: list):
    for i in gameData:
        print(i)

#Create .xlsx data
def generate_data(result, filename):
    df = pd.DataFrame(result)
    df.to_excel(f'{filename}.xlsx', index=False)

if __name__ == '__main__':
    data = get_data(url)
    final_data = parse(data)
    namefile = input('Enter File Name:')
    generate_data(final_data, namefile)
    output(final_data)