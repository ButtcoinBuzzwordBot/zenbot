import os
import random
import pickle
import sqlite3
# TODO: import PyMySQL as mysql
# TODO: test file support after rewrite, globs to config file.

import config as cfg
import scoring as scr

class db:
    """ Database class. Support SQLite and MySQL. """
    
    def __init__ (self, dbtype=None, store=None):
        self.dbtype = dbtype
        self.store = store

        def createDB(self) -> None:
            """ Create the database and tables. """

            cur = self.store.cursor()
            stmts = [
                "CREATE TABLE " + cfg.KOAN_STORE + " (koan TEXT NOT NULL)",
                "CREATE TABLE " + cfg.HAIKU_STORE + " (haiku TEXT NOT NULL)"
            ]
    
            try:
                for stmt in stmts:
                    cur.execute(stmt)
                # TODO: except (sqlite3.Error, mysql.connector.Error) as err:
            except sqlite3.Error:
                print(err)
                print("ERROR: Cannot create tables in " + cfg.DATABASE)
                exit()
            finally:
                cur.close()
            self.store.commit()

        def readRandom(self, name) -> str:
            """ Gets a random row from a table. """

            self.store.row_factory = None
            cur = self.store.cursor()
            try:
                cur.execute("SELECT * FROM " + name + " ORDER BY RANDOM() LIMIT 1")
                data = cur.fetchall()
                if data is None:
                    print("ERROR: Please import " + name + " into database.")
                    exit()
                return(data[0][0])
            except sqlite3.Error:
                print("ERROR: Cannot retrieve " + name + " from db.")
            finally:
                cur.close()
