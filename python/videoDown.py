import requests
#import os

def tsList_get():
    m3u8 = "http://vod.m3u8.co:88/ppvod/3C8EF3AE3F21F1DD95313AC440A73A70.m3u8"
    #get info & list
    response = requests.get(m3u8)
    m3u8ReFormat = str(response.content).strip("\\n").strip("b'").replace("\\n","").split("#")
    tsFileList = m3u8ReFormat[5:1663]

    #seperate ts
    extInfo = []
    tsUrl = []
    tsFullList= []
    for ts in tsFileList:
        extInfo.append(ts.split(",")[0])
        tsUrl.append(ts.split(",")[1])

    for ts in tsUrl:
        tsFullList.append("http://vod.m3u8.co:88"+ts)

    return tsFullList
