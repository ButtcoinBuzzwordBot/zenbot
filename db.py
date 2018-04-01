import os
import random
import sqlite3
# TODO: import PyMySQL as mysql
# TODO: test file support after rewrite, globs to config file.

class DB:
    """ Database class. Supports SQLite and MySQL. """
    
    def __init__ (self, dbtype=None):
        self.dbtype = dbtype
        self.store = store
        dbexists = True

        if dbtype is "sqlite":
            self.DATABASE = "buzzword.db"
            if not os.path.isfile(self.DATABASE):
                dbexists = False
        try:
            self.store = sqlite3.connect(self.DATABASE)
        except sqlite3.Error (err):
            print(err)
            print("ERROR: Cannot create or connect to " + self.DATABASE)
            exit()

        if not dbexists:
            self.createDB(self)
            print("Database created. Please import koans/haiku before running.")
            exit()

    def createDB(self) -> None:
        """ Create the database and tables. """

        cur = self.store.cursor()
        stmts = [
            "CREATE TABLE " + cfg.VISITED_STORE + " (scored VARCHAR(16) NOT NULL)",
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
