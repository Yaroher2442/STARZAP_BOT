import requests 
import json

from datetime import datetime
from datetime import time
from datetime import date
from time import sleep

import sqlite3

import pprint
import config
import dbworker
        
connection = sqlite3.connect(config.db_user_dataset)
dump_connection= sqlite3.connect(config.db_database_dump_file)

search_dict={0:'brand',1:'model',2:'year',3:'category',4:'subcategory',5:'name'}

def create_table_user(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE USERS_CHOSE
             (u_id INTEGER, chose_id INTEGER, brand text, model text,year text, category text, subcategory text, name text )''')
    connection.commit()
def create_table_dump(dump_connection):
    cursor = dump_connection.cursor()
    cursor.execute('''CREATE TABLE DUMP
             (id {0}, provider {0}, OEM {0}, category {0}, name {0}, brand {0}, model {0}, year {0}, restyling {0}, state {0}, 
             note {0}, applicability {0}, quantity {0}, price {0}, photo {0}, subcategory {0})'''.format('text'))
    connection.commit()
def create_table_ways(dump_connection):
    cursor = dump_connection.cursor()
    cursor.execute('''CREATE TABLE WAYS (id, way)''')
    connection.commit()

def delite_table(connection_del,name):
    cursor = connection_del.cursor()
    cursor.execute('''DROP TABLE {}'''.format(name))
    connection.commit()

def update_ways(dump_connection):
    delite_table(dump_connection,'WAYS')
    create_table_ways(dump_connection)
    cursor = dump_connection.cursor()
    cursor.execute('''SELECT id,brand,model,year,category,subcategory,name FROM DUMP''')
    w_data=cursor.fetchall()
    new_data=[]
    for i in w_data:
        l=list(i)
        if '' in l:
            l.remove('')
            new_data.append(tuple(l))
        else:
            new_data.append(tuple(l))
    tpl_list=[]
    for i in new_data:
        w='/'.join(i[1:])
        tpl_list.append((i[0],w))
    cursor.executemany('''INSERT INTO WAYS VALUES (?,?)''',tpl_list)
    connection.commit()
def update_dump(dump_connection):
    delite_table(dump_connection,'DUMP')
    create_table_dump(dump_connection)
    r=requests.get('http://stzp.ru/api/api/getAllProduct')
    data=json.loads(r.text)
    up_list=[]
    for d in data:
        lst=[]
        for i in d.items():
            lst.append(i[1])
        up_list.append(tuple(lst))
    cursor = dump_connection.cursor()
    cursor.executemany('''INSERT INTO DUMP VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', up_list)
    dump_connection.commit()

def search_unic_data(connection,dump_connection,u_id):
    cursor_user= connection.cursor()
    cursor_user.execute('''SELECT * FROM USERS_CHOSE WHERE u_id=?''',(u_id,))
    drop=cursor_user.fetchone()
    choise=drop[1]
    brand=drop[2]
    model=drop[3]
    year=drop[4]
    category=drop[5]
    subcategory=drop[6]
    name=drop[7]
    cursor_dump=dump_connection.cursor()
    endpoint=False
    if choise==0:
        cursor_dump.execute('''SELECT {} FROM DUMP '''.format(search_dict[choise]))
    if choise==1:
        cursor_dump.execute('''SELECT {} FROM DUMP WHERE brand=?'''.format(search_dict[choise]),(brand,))
    if choise==2:
        cursor_dump.execute('''SELECT {} FROM DUMP WHERE brand=? AND model=?'''.format(search_dict[choise]),(brand,model,))
    if choise==3:
        cursor_dump.execute('''SELECT {} FROM DUMP WHERE brand=? AND model=? AND year=?'''.format(search_dict[choise]),(brand,model,year,))
    if choise>=4:
        if choise==4:
            cursor_dump.execute('''SELECT {}, name FROM DUMP WHERE brand=? AND model=? AND year=? AND category=?  '''.format(search_dict[choise]),(brand,model,year,category,))
            buf_lst=cursor_dump.fetchall()
            up_lst=[]
            for i in buf_lst:
                if i[0]=='':
                    up_lst.append('name: '+ i[1])
                else:
                    up_lst.append('subcategory: '+i[0])
            return sorted(list(set(up_lst)))
        if choise==5:
            if 'subcategory' in subcategory:
                subcategory=subcategory.split(' ')[1]
                cursor_dump.execute('''SELECT name FROM DUMP WHERE brand=? AND model=? AND year=? 
                    AND category=? AND subcategory=?'''.format(search_dict[choise]),(brand,model,year,category,subcategory,))
            elif 'name' in subcategory:
                subcategory=subcategory.split(':')[1].lstrip()
                cursor_dump.execute('''SELECT * FROM DUMP WHERE brand=? AND model=? AND year=? 
                    AND category=? AND name=? ''',(brand,model,year,category,subcategory,))
                dict_list=[]
                for i in cursor_dump.fetchall():
                    ls=['id', 'provider' , 'OEM', 'category', 'name', 'brand', 'model', 'year', 'restyling', 'state','note' , 'applicability', 'quantity', 'price' , 'photo' , 'subcategory']
                    dct={}
                    for n in ls:
                        dct[n]=i[ls.index(n)]
                    dict_list.append(dct)
                return dict_list
        if choise==6:
            subcategory=subcategory.split(':')[1].lstrip()
            cursor_dump.execute('''SELECT * FROM DUMP WHERE brand=? AND model=? AND year=? 
                AND category=? AND subcategory=? AND name=? ''',(brand,model,year,category,subcategory,name,))
            dict_list=[]
            for i in cursor_dump.fetchall():
                ls=['id', 'provider' , 'OEM', 'category', 'name', 'brand', 'model', 'year', 'restyling', 'state','note' , 'applicability', 'quantity', 'price' , 'photo' , 'subcategory']
                dct={}
                for n in ls:
                    dct[n]=i[ls.index(n)]
                dict_list.append(dct)
            return dict_list
        # if cursor_dump.fetchall()[0][0]=='':
        #    print('111')
        #    user_chose_update(connection,u_id)
        #    print(search_dict[choise+1])
        #    cursor_dump.execute('''SELECT {} FROM DUMP WHERE brand=? AND model=? AND year=? AND category=? '''.format(search_dict[choise+1]),(brand,model,year,category,))
        #    endpoint=True
        # else: 
        #     print('n')

        # else:
            # print('name')
            # cursor_dump.execute('''SELECT {} FROM DUMP WHERE brand=? AND model=? AND year=? AND category=? AND subcategory=?'''.format(search_dict[choise]),(brand,model,year,category,subcategory,))
    d=[]
    for i in cursor_dump.fetchall():
        d.append(i[0])
    connection.commit()
    dump_connection.commit()
    n_d=[]
    for i in d:
        n_d.append(i.replace('\xa0',''))
    return sorted(list(set(n_d)))

def add_user(connection,u_id):
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO USERS_CHOSE (u_id,chose_id) VALUES (?,?)''',(u_id,0))
    connection.commit()
def user_chose_update(connection,u_id):
    cursor = connection.cursor()
    cursor.execute('''SELECT chose_id FROM USERS_CHOSE WhERE u_id=?''',(u_id,))
    state=cursor.fetchone()
    cursor.execute('''UPDATE USERS_CHOSE SET chose_id=? WHERE u_id=?''',(state[0]+1,u_id,))
    connection.commit()
def user_chose_reset(connection,u_id):
    cursor = connection.cursor()
    cursor.execute('''UPDATE USERS_CHOSE SET chose_id=? ,brand='', model='', year='', category='', subcategory='', name='' WHERE u_id=?''',(0,u_id,))
    connection.commit()
def chek_pik(connection,dump_connection,u_id,pik_id):
    cursor = connection.cursor()
    user_pik=search_unic_data(connection,dump_connection,u_id)
    connection.commit()
    return user_pik[pik_id]
def user_pik_append(connection,u_id,pik):
    cursor = connection.cursor()
    cursor.execute('''SELECT chose_id FROM USERS_CHOSE WhERE u_id=?''',(u_id,))
    state=cursor.fetchone()
    cursor.execute('''UPDATE USERS_CHOSE SET {}=? WHERE u_id=?'''.format(search_dict[state[0]]),(pik,u_id,))
    connection.commit()


def main():
    start_time = datetime.now()
    u_id=446387634

    # delite_table(dump_connection,'DUMP')
    # create_table_dump(dump_connection)
    # create_table_ways(dump_connection)
    # update_ways(dump_connection)
    # update_dump(dump_connection)
    # delite_table(connection,'USERS_CHOSE')
    # create_table_user(connection)
    # add_user(connection,u_id)
    a=search_unic_data(connection,dump_connection,u_id)
    print(a)
    # user_chose_update(connection,u_id)
    # pik='lol'
    # user_pik(connection,u_id,pik)
    # print(chek_pik(connection,dump_connection,u_id,1))

    connection.commit()
    connection.close()
    dump_connection.commit()
    dump_connection.close()
    print(datetime.now() - start_time)

if __name__ == '__main__':
    main()