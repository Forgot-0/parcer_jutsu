import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://jut.su/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

def pages() -> list:
    spisok = []

    for i in range(1, 10**9):
        url = f'https://jut.su/anime/page-{i}'
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'lxml')
        soup = soup.find_all('div', class_='all_anime_global')
        
        if soup == []:
            return spisok

        for content in soup:
            info = {
                'title': content.find('div', class_='aaname').text,
                'url_jutsu': content.find('a')['href'],
            }

            media = content.find('div', class_='aailines').get_text(separator=' ').split()
            for n in range(0, len(media), 2):
                info[media[n+1]] = media[n]  

            info['anime_info'] = info_anime('https://jut.su/'+info['url_jutsu'])
            print(info)
            spisok.append(info)

def info_anime(url:str) -> dict:
    info = {'content': {}}
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'lxml')
    spisok = soup.find('div', class_='under_video_additional').get_text(separator=' ').replace('Аниме', '').split(' . ')

    for el in spisok:
        try:
            key, val = el.split(':')
            info[key.strip()] = val.replace("    ", '').replace('  и', ', ').replace(' ,', ', ')

        except:
            info['Оригинальное название'] = el.replace('Оригинальное название:', '').split(" Возрастной рейтинг")[0][2:]
            info['Возрастной рейтинг'] = el.split("Возрастной рейтинг:  ")[-1].strip()

    all_videos = soup.find_all('a', class_='short-btn')

    for video in all_videos:
        info['content'][video.text] = info_video('https://jut.su' + video['href'])
 
    info['description'] = soup.find('p', class_='under_video').text

    return info

def info_video(url:str) -> dict:
    info = {}
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'lxml')
    info['title'] = soup.find('div', class_='video_plate_title').text

    for video in soup.find_all('source'):
        info[video['res']] = video['src']

    return info




if __name__ == '__main__':
    # url = 'https://binary2hex.ru/calc/calcyadro.php?calculator=7&calcid=24'
    # data = {
    #     'chislo1': '12',
    #     'chislo2': '10',
    #     'num_base1': '3',
    #     'num_base2': '2',
    #     'operaciya': 4,
    # }
    # print(requests.post(url=url, data=data).text)
    print(info_anime('https://jut.su/full-metal-alchemist/'))