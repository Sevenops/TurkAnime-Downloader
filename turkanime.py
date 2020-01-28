import os
import re

import httpx

import base64
from urllib.parse import unquote
import hashlib

cookies = {
    "yew490": "1",
    "_ga": "GA1.2.284686093.1564216182",
    "_gid": "GA1.2.1256976049.1564216182",
    "__PPU_SESSION_1_1683592_false": "1564216202929|1|1564216202929|1|1",
    "_gat": "1",
}

headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Origin": "http://www.turkanime.net",
    "Upgrade-Insecure-Requests": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Referer": "http://www.turkanime.net/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
}


class TurkAnime:

    url = "http://www.turkanime.net"


    def anime_ara(self, ara):

        data = {"arama": ara}
        veri = httpx.post(
            self.url + "/arama", headers=headers, cookies=cookies, data=data
        ).content.decode("utf-8")
        liste = []
        r = re.findall(
            '<div class="panel-ust-ic"><div class="panel-title"><a href="\/\/www\.turkanime\.net\/anime\/(.*?)" (.*?)>(.*?)<\/a>',
            veri,
        )

        for slug, _, title in r:
            liste.append([title, slug])
        if len(liste) == 0:
            try:
                slug = veri.split('window.location = "anime/')[1].split('"')[0]
                liste.append([ara, slug])
            except:
                pass
        return liste

    def bolumler(self, slug):
        veri = httpx.get(
            self.url + "/anime/" + slug, headers=headers, cookies=cookies
        ).content.decode("utf8")
        h = headers.copy()
        h.update({"X-Requested-With": "XMLHttpRequest", "Accept": "*/*"})
        animeId = veri.split("ajax/bolumler&animeId=")[1].split('"')[0]
        liste = []
        a = httpx.get(
            f"http://www.turkanime.net/ajax/bolumler&animeId={animeId}",
            headers=h,
            cookies=cookies,
        ).content.decode("utf8")
        r = re.findall(
            '<a href="\/\/www\.turkanime\.net\/video\/(.*?)" (.*?)><span class="bolumAdi">(.*?)<\/span><\/a>',
            a,
        )
        for slug, _, title in r:
            liste.append([title, slug])
        return liste