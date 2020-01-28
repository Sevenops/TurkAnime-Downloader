# -*- coding: cp1254 -*-
import urllib2,os,urllib,re

folroot="./Animeler/"
anime="Naruto Shippuuden"
root="http://www.turkanime.tv/"
AID="76"#Bu Kod Naruto için IDFinder.py ile başka animelerin ID'sini bulabilirsiniz
bolumlist_url="http://www.turkanime.tv/icerik/bolumler&ID="+AID
bolumlist=[]

def create_folder_and_write_file(bol_string,link_string):
    if not os.path.exists(folroot+anime): os.makedirs(folroot+anime)
    bol_string=bol_string.replace("-", " ").replace("Bolum", "Bölüm")
    open(folroot+anime+"/"+bol_string,"wb").write(link_string)
    
def get_bolumlist():
    bolumlist_read=urllib2.urlopen(bolumlist_url).read()
    bolumlist_read=bolumlist_read.split('<div id="bolumlist">')[1].split("</div>")[0]
    for a in bolumlist_read.split('<a href="'):
        b=a.split('" class="btn"')[0]
        bolumlist.append(b)
    bolumlist.remove("")
    
def get_vklink(link):
    
    vk_links={}
    kalite=["720","480","360","240"]
    vklink_read=urllib2.urlopen(root+link).read()
    a=vklink_read.split("""','#video');"><i class="icon-play"></i> VK</a>""")
    if True:
        print root+link
        a=a[0]
        b=a.split("&video=")[-1]
        
        code=str(b)
        fansub=a.split("&fansub=")[1].split("&")[0].replace("Ä±", "ı")
        lnk=root+link+"&fansub="+fansub+"&giris=&video="+code
        
        vklink_read=urllib.urlopen(lnk).read()
        #print vklink_read
        print lnk
        vklink_rad=urllib.urlopen(lnk).read()
        #open("a.html", "w").write(vklink_rad)
        #print vklink_rad
        #print lnk
        try:
            vk_url=vklink_read.split('</i></a><iframe src="')[1].split('" width="')[0]
        except:
           
            vk_url=vklink_read.split('http://vk.com/video_ext.php')#.split('" width="')[0]
        
        vklink_read=urllib2.urlopen(vk_url).read()
        for x in kalite:
            sp=vklink_read.split('url'+x+'":"')
            if len(sp)!=1:
                vklink_mp4=sp[1].split('","')[0]
                vklink_mp4=vklink_mp4.replace("\\", "")
                print "-"*80
                print x
                print vklink_mp4
                print "-"*80

get_bolumlist()
for i,x in enumerate(bolumlist):
    try:
        _re=re.search('(-\d+-\d+-|-\d+-)',x)
        n=_re.group(1)
        print str(i)+" : "+n[1:-1]
    except:pass
num=raw_input(">>>")
get_vklink(bolumlist[int(num)])
