import requests
import json
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
from multiprocessing import Pool


def movies_from_div(div):
    e = pq(div)
    rank = e('.board-index').text()
    img = e('.board-img').attr('data-src')
    name = e('.name').text()
    actors = e('.star').text().strip()[3:]
    time = e('.releasetime').text()
    score = e('.integer').text() + e('.fraction').text()
    result = {
        'rank': rank,
        'img': img,
        'name': name,
        'actors': actors,
        'time': time,
        'score': score,
    }

    return result


def movies_from_url(url):
    response = requests.get(url)
    try:
        if response.status_code == 200:
            html =  pq(response.text)
            items = html('dd').items()
            movies = [movies_from_div(item) for item in items]
            return movies
        return None
    except RequestException:
        return None


def write_to_file(content):
    with open('result2.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, indent=2, ensure_ascii=False) + '\n')


def main(offset):
    url = 'https://maoyan.com/board/4?offset={}'.format(offset)
    movies = movies_from_url(url)
    if movies:
        write_to_file(movies)


if __name__ == '__main__':
    # for i in range(10):
    #     main(i*10)
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])