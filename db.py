import os
import re
import random
import sqlite3
# TODO: import PyMySQL as mysql
# TODO: test file support after rewrite, globs to config file.

import config as cfg

class DB:
    """ Database class. Supports SQLite and MySQL. """
    
    def __init__ (self, dbtype=None) -> None:
        self.dbtype = dbtype
        dbexists = True
        
        if dbtype is "sqlite":
            cfg.DATABASE = "zenbot.db"
            if not os.path.isfile(cfg.DATABASE):
                dbexists = False
            try:
                self.store = sqlite3.connect(cfg.DATABASE)
            except sqlite3.Error as err:
                print(err)
                print("ERROR: Cannot create or connect to "+ cfg.DATABASE)
                exit()
        else:
            print("Database type "+ dbtype +" not supported.")
            exit()

        if not dbexists:
            self.createDB()
            print("Database created. Please import koans/haiku before running.")
            exit()

        cfg.already_visited = self.readVisited()

    def setType(self, dbtype):
        self.dbtype = dbtype

    def executeStmt(self, stmt) -> None:
        """ Executes an atomic database operation. """
        
        try:
            cur = self.store.cursor()
            cur.execute(stmt)
        except sqlite3.Error as err:
            # TODO: except (sqlite3.Error, mysql.connector.Error) as err:
            print(err)
            print("ERROR: Cannot execute " + stmt)
            exit()
            #raise Exception(SQLExecuteError ("Execute error"))
        cur.close()

    def fetchStmt(self, stmt) -> list:
        """ Executes a SELECT statement and returns fetched results. """

        try:
            cur = self.store.cursor()
            cur.execute("SELECT "+ stmt)
            data = cur.fetchall()
            cur.close()
            return(data)
        except sqlite3.Error as err:
            # TODO: except (sqlite3.Error, mysql.connector.Error) as err:
            print(err)
            print("ERROR: Cannot execute SELECT " + stmt)
            exit()
            #raise Exception(SQLExecuteError "Execute error")

    def closeDB(self) -> None:
        """ Commits and closes database. """

        self.store.commit()
        self.store.close()

    def createDB(self) -> None:
        """ Create the database and tables. """

        stmts = [
            "CREATE TABLE "+ cfg.VISITED_STORE +" (scored VARCHAR(16) NOT NULL)",
            "CREATE TABLE "+ cfg.KOAN_STORE +" (koan TEXT NOT NULL)",
            "CREATE TABLE "+ cfg.HAIKU_STORE +" (haiku TEXT NOT NULL)",
        ]

        for stmt in stmts:
            self.executeStmt(stmt)
        self.store.commit()

    def readRandom(self, name) -> str:
        """ Gets a random row from a table. """

        self.store.row_factory = None
        if self.dbtype is "sqlite":
            data = self.fetchStmt("* FROM "+ name +" ORDER BY RANDOM() LIMIT 1")
            if data is None:
                print("ERROR: Please import " + name + " into database.")
                exit()
            return(data[0][0].replace("''", "'"))

    def readVisited(self) -> list:
        """ Gets list of posts already visited. """

        self.store.row_factory = lambda cursor, row: row[0]
        if self.dbtype is "sqlite":
            visited = self.fetchStmt("* FROM "+ cfg.VISITED_STORE)
        if visited is None:
            return([])
        return(visited)

    def writeVisited(self) -> None:
        """ Saves list of posts already visited. """

        if cfg.DEBUG: print("Writing visited list to table.")
        length = len(cfg.already_visited)
        if length > cfg.MAX_VISITED:
            cfg.already_visited = cfg.already_visited[length - cfg.MAX_VISITED:length]

        if self.dbtype is "sqlite":
            self.executeStmt("DELETE FROM "+ cfg.VISITED_STORE)
            for visited in cfg.already_visited:
                stmt = "INSERT INTO "+ cfg.VISITED_STORE +" VALUES ('"+ visited +"')"
                self.executeStmt(stmt)
        self.store.commit()

    def readSnappy(self, r) -> list:
        """ Reads and parses Snapshillbot entries. """

        wiki = r.subreddit('Snapshillbot').wiki['extxt/buttcoin']
        quotes = wiki.content_md
        return [q.strip() for q in re.split('\r\n-{3,}\r\n', quotes) if q.strip()]
