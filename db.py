import os
import random
import sqlite3
# TODO: import PyMySQL as mysql
# TODO: test file support after rewrite, globs to config file.

class DB:
    """ Database class. Supports SQLite and MySQL. """
    
    def __init__ (self, dbtype=None):
        self.dbtype = dbtype
        dbexists = True
        
        if dbtype is "sqlite":
            cfg.DATABASE = "buzzword.db"
            if not os.path.isfile(cfg.DATABASE):
                dbexists = False
        else:
            print("Database type "+ dbtype +" not supported.")
            exit()

        if not dbexists:
            self.createDB(self)
            print("Database created. Please import koans/haiku before running.")
            exit()

        if dbtype is "sqlite":
            try:
                self.store = sqlite3.connect(cfg.DATABASE)
            except sqlite3.Error (err):
                print(err)
                print("ERROR: Cannot create or connect to "+ cfg.DATABASE)
                exit()

        already_visited = readVisited()

    def executeStmt(self, stmt) -> None:
        """ Executes an atomic database operation. """
        
        try:
            cur = self.store.cursor()
            cur.execute(stmt)
        except sqlite3.Error (err):
            # TODO: except (sqlite3.Error, mysql.connector.Error) as err:
            print(err)
            print("ERROR: Cannot execute " + stmt)
            raise Exception(SQLExecuteError "Execute error")
        cur.close()

    def fetchStmt(self, stmt) -> List:
        """ Executes a SELECT statement and returns fetched results. """

        try:
            cur = self.store.cursor()
            cur.execute("SELECT "+ stmt)
            data = cur.fetchall()
            cur.close()
        except sqlite3.Error (err):
            # TODO: except (sqlite3.Error, mysql.connector.Error) as err:
            print(err)
            print("ERROR: Cannot execute SELECT " + stmt)
            raise Exception(SQLExecuteError "Execute error")
        
    def createDB(self) -> None:
        """ Create the database and tables. """

        stmts = [
            "CREATE TABLE "+ cfg.VISITED_STORE +" (scored VARCHAR(16) NOT NULL)",
            "CREATE TABLE "+ cfg.KOAN_STORE +" (koan TEXT NOT NULL)",
            "CREATE TABLE "+ cfg.HAIKU_STORE +" (haiku TEXT NOT NULL)",
            ("CREATE TABLE "+ cfg.HIGHSCORES_STORE +" (score int NOT NULL "+
             "name VARCHAR(32) NOT NULL, url VARCHAR(256) NOT NULL)")
        ]

        for stmt in stmts:
            executeStmt(self, stmt).close()
        self.store.commit()

    def readHighscores(self) -> list:
        """ Retrieves the list of highscores. """

        self.store.row_factory = None
        if self.dbtype is "sqlite":
            return(fetchStmt(self, "score,name,url FROM "+ cfg.HIGHSCORES_STORE))

    def writeHighscores(self) -> None:
        """ Stores list of highscores. """

        if self.dbtype is "sqlite":
            hs = readHighscores(self)
            executeStmt(self, "DELETE FROM "+ cfg.HIGHSCORES_STORE)
            for score, name, url in hs:
                stmt = (
                    "INSERT INTO "+ cfg.HIGHSCORES_STORE +" VALUES ("+ str(score) +
                    ", '"+ name +"', '"+ url +"')"
                )
                executeStmt(self, stmt)
            self.store.commit()

    def readRandom(self, name) -> str:
        """ Gets a random row from a table. """

        self.store.row_factory = None
        if self.dbtype is "sqlite":
            data = fetchStmt(self, "* FROM "+ name +" ORDER BY RANDOM() LIMIT 1")
            if data is None:
                print("ERROR: Please import " + name + " into database.")
                exit()
            return(data[0][0])

    def readVisited(self) -> list:
        """ Gets list of posts already visited. """

        self.store.row_factory = lambda cursor, row: row[0]
        if self.dbtype is "sqlite":
            return(fetchStmt(self, "* FROM "+ cfg.VISITED_STORE))

    def writeVisited(self) -> None:
        """ Saves list of posts already visited. """
    
        length = len(cfg.already_visited)
        if length > cfg.MAX_VISITED:
            already_visited = cfg.already_visited[length - cfg.MAX_VISITED:length]

        if self.dbtype is "sqlite":
            executeStmt(self, "DELETE FROM "+ cfg.VISITED_STORE)
            for visited in cfg.already_visited:
                stmt = "INSERT INTO "+ cfg.VISITED_STORE +" VALUES ('"+ visited +"')"
                executeStmt(self, stmt)
