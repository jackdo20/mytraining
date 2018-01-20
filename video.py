#-*- encoding:utf-8-*-

import requests
from bs4 import BeautifulSoup


def playerUrl_get(webUrl):
    response = requests.get(webUrl)
    response.encoding = "gbk"
    soup = BeautifulSoup(response.content,"html.parser")

    #get player url address
    playerTag = soup.find("button",attrs={"class":"hls"})
    playerUrl = str(playerTag.attrs["data-id"])
 
    #write to file to test
    """videoFile = open("videoResult.html","w",encoding="utf-8")
    videoFile.writelines(soup.prettify())
    videoFile.close()"""
    #print(playerUrl)
    return playerUrl

def m3u8Url_get(playerUrl):
    #url = "http://play.m3u8.co/x.php?hls=aHR0cDovL3ZvZC5tM3U4LmNvOjg4LzIwMTgwMTE2L3c0dGxCcXpuL2luZGV4Lm0zdTg="
    url = "http://play.m3u8.co/x.php?hls="+playerUrl
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    """
    videoFile = open("video.html","w",encoding='utf-8')
    videoFile.writelines(soup.prettify())
    videoFile.close()"""
    step1=soup.find("body")
    step2 = step1.script.get_text()
    step3 = step2.replace("\n",",").split(",")
    #print(step3)
    step4 = step3[-4].replace("video: ","")
    #print(step4[2:154])
    m3u8Url = step4[2:154]
    m3u8UrlRes = requests.get(m3u8Url)
    m3u8step1 = str(m3u8UrlRes.content)
    #print(m3u8step1.split(","))
    m3u8step2 = m3u8step1.split(",")[2]
    #print(m3u8step2)
    m3u8step3 = m3u8step2.split("\\n")
    #print(m3u8step3[1])
    m3u8UrlFinal = m3u8step3[1]
    return m3u8UrlFinal

webUrl = "http://www.ggmee.com/videos/detail/a/eyJpdiI6IlNxNWJDVUFYNXVnODdQdFAzVTFwQWc9PSIsInZhbHVlIjoiY1RVWEppMEZMZ1psdllhbVVxNkc2QT09IiwibWFjIjoiYzg0ZGI3NDYzY2Y0ODY2MTA0MDMyYzQxOGQyNjgxN2U1YmM1ZTY1OTg0NjgxNTFiYzMxNzBkM2UwNDJkYWMyMyJ9"
playerUrl=playerUrl_get(webUrl)
m3u8Url=m3u8Url_get(playerUrl)
movieUrl = "http://vod.m3u8.co:88"+m3u8Url
print(movieUrl)