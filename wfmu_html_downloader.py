import os
import urllib.request

url = "https://www.wfmu.org/playlists/shows/"

files = [int(file.split('.')[0]) for file in os.listdir('wfmu_html')]
files.sort()
#k = files[-1]
k=97000

for n in range(k,113000):
    try:
        tries = 0
        wfmu_file = ''
        while tries<10 and len(wfmu_file) == 0:
            if not str(n)+'.html' in files:
                req = urllib.request.Request(url+str(n), headers={'User-Agent': 'Mozilla/5.0'})
                wfmu_file = urllib.request.urlopen(req).read().decode("utf-8")
            tries += 1
        wfmu_file = wfmu_file.replace('\r','')
        file = open('wfmu_html/'+str(n)+'.html','w+')
        file.write(wfmu_file)
        file.close()
        print(n)
    except:
        print('error', n)
