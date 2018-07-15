
import os
from bs4 import BeautifulSoup


# Scrapes links to roster announcements from static html files of ussoccer websites
data_dir = '/Users/marcinic/american_messi/data'
files = os.listdir(data_dir)
files_p = [os.path.join(data_dir,file) for file in files]
files_p = files_p[::1]

out_links = []
for file in files_p:
    f = open(file)
    txt = f.read()
    soup = BeautifulSoup(txt,'lxml')
    divs = soup.find_all('div',class_='pod-text')
    links = ['https://ussoccer.com'+div.a['href'] for div in divs]
    out_links = out_links+links

out_file = open('usynt_links.txt','w+')
for link in out_links:
    out_file.write(link+'\n')

out_file.close()
