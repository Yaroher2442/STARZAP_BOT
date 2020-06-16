import requests 
from datetime import datetime
from datetime import time
from datetime import date
from time import sleep
import json
import pprint
import config
import dbworker
from bs4 import BeautifulSoup
import os
        
def read_foto(u_id,href):
    r=requests.get(href)
    html=BeautifulSoup(r.text,'lxml')
    first_foto_href=html.find('a').get('href')
    new_name=first_foto_href.replace('/','_')
    fot=requests.get('http://stzp.ru'+first_foto_href).content
    with open('Users_foto\\'+'{}{}'.format(u_id,new_name),'wb') as file_handler:
        file_handler.write(fot)
        return str(u_id)+new_name

def create_way(way):
	new_way=os.getcwd()+'\\Users_foto\\'+way
	return new_way

def delite_foto(way):
	os.remove(way)
	return 'dell_foto_ok'

def main():
    # way=read_foto(446387634, 'http://stzp.ru/api/foldersindex/18967')
    # print(create_way(way))
    # delite_foto(way)
    pass

if __name__ == '__main__':
    main()