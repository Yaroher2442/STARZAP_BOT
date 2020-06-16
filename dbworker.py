from vedis import Vedis
import config
import json
import sqlite3

def get_current_state(user_id):
    with Vedis(config.db_users_state_file) as db:
        try:
            return db[user_id].decode()
        except KeyError:
            return config.States.S_START.value
def set_state(user_id, state):
    with Vedis(config.db_users_state_file) as db:
        try:
            db[user_id] = state
            return True
        except:
            print('set_state_Error')
            return False
def get_data():
    pass
def main():
    pass

if __name__ == '__main__':
    main()