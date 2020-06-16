from telebot import types
import telebot

from vedis import Vedis
import sqlite3

import time
import json
import sys

from pprint import pprint

import dbworker
import config
import dump_worker
import foto_worker


connection = sqlite3.connect(config.db_user_dataset)
dump_conection= sqlite3.connect(config.db_database_dump_file)

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE USERS_CHOSE
             (u_id INTEGER, chose_id INTEGER, brand text, model text, category text, subcategory text, name text )''')
    connection.commit()
def delite_table(connection):
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE USERS_CHOSE''')
    connection.commit()

def add_user(connection,u_id):
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO USERS_CHOSE (u_id,chose_id) VALUES (?,?)''',(u_id,0))
    connection.commit()



def main():
    u_id=446387634
    add_user(connection,u_id)
    # create_table(connection)
    # delite_table(connection)
    connection.close()

if __name__ == '__main__':
    main()