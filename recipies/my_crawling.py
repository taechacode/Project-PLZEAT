from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse


def gogogo(recipe_name):
    real_result = []
    change = urllib.parse.quote_plus(recipe_name)
    while len(real_result) != 3:
        response = urlopen(
            f'https://www.youtube.com/results?search_query={change}+%EB%A0%88%EC%8B%9C%ED%94%BC')
        soup = BeautifulSoup(response, 'html.parser')
        links = []
        result_links = []
        no_have_result = soup.select(".search-message")
        if(no_have_result != []):
            return ""
        for anchor in soup.find_all('a'):
            if 'watch?v' in anchor.get('href', '/'):
                links.append(anchor.get('href', '/'))
            if len(links) == 6:
                break

        for link in links:
            if ('list' in link.split('=')[1]):
                result_links.append("비어있음")
            else:
                result_links.append(link.split('=')[1])
        count = 0
        for x in result_links:
            if (count == 0 or count == 2 or count == 4):
                real_result.append(x)
            count = count + 1
            if count == 5:
                break
    return real_result
