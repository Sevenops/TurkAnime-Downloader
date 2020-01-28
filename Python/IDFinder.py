# -*- coding: utf-8 -*-
import urllib2

#a=open("aa.txt","r").read()
a=urllib2.urlopen("http://www.turkanime.tv/icerik/tamliste").read()
i=0
l="Naruto"
#open("aa.txt","w").write(a)
for b in a.split('<a href="'):
    if i < 999999:
        link=b.split('"')[0]
        isim=b.split('">')[1].split('</a>')[0]
        
        if not link.startswith('<div'):
            try:
                
                if l in isim:
                    print isim
                    print link,isim
                    veri=urllib2.urlopen('http://www.turkanime.tv/'+link).read()
                    id=veri.split('listem&ID=')[1].split('&')[0]
                    print id
            except:pass
    i+=1
                   
