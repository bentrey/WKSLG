import os
import urllib.request

url = "https://www.wfmu.org/playlists/shows/"

files = os.listdir('wfmu_html')

for n in range(0,110000):
    try:
        if not str(n)+'.html' in files:
            wfmu_file = urllib.request.urlopen(url+str(n)).read().decode("utf-8")
            wfmu_file = wfmu_file.replace('\r','')
            file = open('wfmu_html/'+str(n)+'.html','w+')
            file.write(wfmu_file)
            file.close()
            print(n)
    except:
        print('error', n)