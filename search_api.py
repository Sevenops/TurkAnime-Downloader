import httpx
import os
import re

from Crypto.Cipher import AES
import base64
from urllib.parse import unquote
import hashlib

def decode_iframe(a):
    # Fonksiyonun sahibi gokaybiz
    a = {"ct": "P5rh7okRVe0uBsN+M8LCi11SFSnojXxDAv88ZX7TQtMYslz0OAWF+KPAA2d1uQES",
         "iv": "94d71d7bc0975ec13724edabf2fe1885", "s": "48a8c852f99b1ee6"}

    p = b"7Q+5&VnG1a{)-UWd)u$_}TiXINqCw|1HG,qfQvDgbK>W(O)m 2^B{5U|@+%tQ<;F"
    salt = bytes.fromhex(a["s"])
    ct = base64.b64decode(a["ct"])
    iv = bytes.fromhex(a["iv"])
    cp = p+salt
    md5 = []
    m = hashlib.md5()
    m.update(cp)
    md5.append(m.digest())
    result = md5[0]
    for x in range(3):
        m = hashlib.md5()
        m.update(md5[x]+cp)
        md5.append(m.digest())
        result += md5[x+1]
    key = result[0:32]
    obj = AES.new(key, AES.MODE_CBC, iv)
    message = ct
    a = obj.decrypt(ct)
    return a.strip().decode("utf8").replace('\/', '/')


class TurkAnime:

    url = "http://www.turkanime.tv/"
    cookies = {
        '__cfduid': 'deb9e04ac510c1b707412b1fd7daadec91564216182',
        'yew490': '1',
        '_ga': 'GA1.2.284686093.1564216182',
        '_gid': 'GA1.2.1256976049.1564216182',
        '__PPU_SESSION_1_1683592_false': '1564216202929|1|1564216202929|1|1',
        '_gat': '1',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Alt-Used': 'www.turkanime.tv:443',
        'Connection': 'keep-alive',
        'Referer': 'http://www.turkanime.tv/',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
        'Cookie': "_ga=GA1.2.1278321181.1564136960; _gat=1; _gid=GA1.2.1445927356.1563524213; PHPSESSID=tqpqo4smru3mhfej4pdkqf85n0; __cfduid=dec57aab208a3f67382bb2ed120c0ef081564136948"
    }

    def __init__(self):
        pass

    def anime_ara(self, ara):

        data = {
            'arama': ara
        }
        veri = httpx.post(self.url+"/arama", headers=self.headers,
                          cookies=self.cookies, data=data).content.decode("utf8")

        liste = []
        r = re.findall(
            '<div class="panel-ust-ic"><div class="panel-title"><a href="\/\/www\.turkanime\.tv\/anime\/(.*?)" (.*?)>(.*?)<\/a>', veri)
        for slug, _, title in r:
            liste.append([title, slug])
        if len(liste) == 0:
            slug = veri.split('window.location = "anime/')[1].split('"')[0]
            liste.append([ara, slug])
        return liste

    def bolumler(self, slug):
        veri = httpx.get(self.url+"/anime/"+slug, headers=self.headers,
                         cookies=self.cookies).content.decode("utf8")
        h = self.headers.copy()
        h.update({"X-Requested-With": "XMLHttpRequest", "Accept": "*/*"})
        animeId = veri.split("ajax/bolumler&animeId=")[1].split('"')[0]
        liste = []
        a = httpx.get(
            f"http://www.turkanime.tv/ajax/bolumler&animeId={animeId}", headers=h, cookies=self.cookies).content.decode("utf8")
        r = re.findall(
            '<a href="\/\/www\.turkanime\.tv\/video\/(.*?)" (.*?)><span class="bolumAdi">(.*?)<\/span><\/a>', a)
        for slug, _, title in r:
            liste.append([title, slug])
        return liste

    def deneme(self):
        h = self.headers.copy()
        h.update({"X-Requested-With": "XMLHttpRequest", "Accept": "*/*"})
        url = "http://www.turkanime.tv/ajax/videosec&b=eTodJK2BS5KTMnDUiV3Dw3AIJ_k6yMwZ1fkyk1uZD5M&v=PThSgK5ErnD1t4PDUH488Y6gYyxpOZqbrhx9B-ao-XE&f=kvLxEP-QJkVNREiSNmb9iX397m9OqncJvJcxKlt1NGg"
        #url = "http://www.turkanime.tv/iframe?url=NF_1ZgbJgUy1K2JT8EJE1HnFKwWq6yYmPV31ZhtRXJC1UqjjJ7TJuYn3INrkuZMU5VJ2s9dh6NZJGREVq84I-hG2O71V8uDcXUZzggi0uUhdzcOhvrS813MJPiltPjUeuhGMxySXpPB1cOMXYOL9hz1zh5Eq_0P8CPEvGGpe1mVYwXQ8Nhb2_noWFBVObWJgYDeyL-FH6pS7bB5-PIp8UA&sec=1"

        a = httpx.get(url, headers=h,
                      cookies=self.cookies).content.decode("utf8")
        video = "http:"+a.split('<iframe src="')[1].split('"')[0]
        a = httpx.get(video, headers=h,
                      cookies=self.cookies).content.decode("utf8")
        print(a)
        a = httpx.get("http://www.turkanime.tv/iframe?url=Sk3SXAueRmkPY_ghJ9h0kv-utaoKPi4lKnaUvyh2S40DY3JOMHfyTRcil1NK6lXPKaM38Ah0oJy3sZYl_lhMAkk2EOpkUxbfIbWXRw_dBcXizkJGj5pIaChARkz5NPZq884i7Cq-mwwWjvkOoIqUvkoTQhC_JAC9wPaRt6d79cuQVWPYIvLGaWlwC38cqMy2YyakI3pu0NGd-y7a7ODkjzzNlWqKjzhzRN0QLHRQRlCyteI0TmrJTxebjbTjVNdN", headers=h, cookies=self.cookies).content.decode("utf8")
        # print(a)