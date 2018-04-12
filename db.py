import os, re
import sqlite3
#import pymysql as mysql
#import memcache
import config as cfg

class DB:
    """ Database class. Supports SQLite and MySQL. """
    
    def __init__ (self, dbtype=None) -> None:
        self.dbtype = dbtype
        dbexists = True
        
        if dbtype is "sqlite":
            cfg.DATABASE += ".db"
            if not os.path.isfile(cfg.DATABASE):
                dbexists = False
            try:
                self.store = sqlite3.connect(cfg.DATABASE)
            except sqlite3.Error as err:
                print(err)
                print("ERROR: Cannot create or connect to "+ cfg.DATABASE)
                exit()

        elif dbtype is "mysql":
            try:
                self.store = mysql.connect(host=cfg.MYSQL_HOST,
                                           user=cfg.MYSQL_USER,
                                           password=cfg.MYSQL_PW,
                                           db=cfg.DATABASE,
                                           charset='utf8')
            except mysql.Error as err:
                print(err)
                print("ERROR: Cannot create or connect to "+ cfg.DATABASE)
                exit()

            cur = self.store.cursor()
            cur.execute("SHOW TABLES LIKE '"+ cfg.VISITED_STORE +"'")
            result = cur.fetchone()
            if result is None:
                dbexists = False
            cur.close()

        elif dbtype is "memcache":
            try:
                self.store = memcache.Client(['127.0.0.1:11211'], debug=1)
            except memcache.Error as err:
                print(err)
                print("ERROR: Unable to initialize memcache.")
                exit()
            self.createDB()

        else:
            print("Database type "+ dbtype +" not supported.")
            exit()

        if not dbexists:
            self.createDB()
            print("Database created. Please import all tables before running.")
            exit()

        cfg.already_visited = self.readVisited()

    def executeStmt(self, stmt) -> None:
        """ Executes an atomic database operation. """
        
        try:
            cur = self.store.cursor()
            cur.execute(stmt)
        except (sqlite3.Error, mysql.Error) as err:
            print(err)
            print("ERROR: Cannot execute " + stmt)
            exit()
        finally:
            cur.close()

    def fetchStmt(self, stmt) -> list:
        """ Executes a SELECT statement and returns fetched results. """

        try:
            cur = self.store.cursor()
            cur.execute("SELECT "+ stmt)
            data = cur.fetchall()
        except sqlite3.Error as err:
            print(err)
            print("ERROR: Cannot execute SELECT " + stmt)
            exit()
        finally:
            cur.close()
        return(data)

    def checkTable(self, table) -> int:
        """ Checks to see if a table exists. """

        try:
            cur = self.store.cursor()
            cur.execute("SELECT COUNT(*) FROM "+ table)
            [count] = cur.fetchall()
        except sqlite3.Error as err:
            print(err)
            return(0)
        finally:
            cur.close()
        return(count)
        
    def deleteTable(self, table) -> None:
        """ Deletes all entries from a table. """

        try:
            cur = self.store.cursor()
            cur.execute("DELETE FROM "+ table)
        except:
            return
        finally:
            cur.close()

    def dropTable(self, table) -> None:
        """ Drops a table whether or not it exists. """

        try:
            cur = self.store.cursor()
            cur.execute("DROP TABLE "+ table)
        except:
            return
        finally:
            cur.close()

    def closeDB(self) -> None:
        """ Commits and closes database. """

        self.store.commit()
        self.store.close()

    def createDB(self) -> None:
        """ Create the database and tables. """

        if self.dbtype is "memcache":
            keys = [cfg.KOAN_STORE, cfg.HAIKU_STORE, cfg.REPLY_STORE]
            for key in keys:
                try:
                    dataf = open(key + ".txt", "r", encoding=cfg.ENCODING)
                except:
                    print("ERROR: Data file "+ key +".txt does not exist.")
                    exit()
                data = dataf.read().split("|")
                dataf.close()
                self.store.set(key, data)

        else:
            stmts = [
                "CREATE TABLE "+ cfg.VISITED_STORE +" (visited VARCHAR(16) NOT NULL)",
                "CREATE TABLE "+ cfg.KOAN_STORE +" (koan TEXT NOT NULL)",
                "CREATE TABLE "+ cfg.HAIKU_STORE +" (haiku TEXT NOT NULL)",
                "CREATE TABLE "+ cfg.REPLY_STORE +" (replies TEXT NOT NULL)"
            ]

            for stmt in stmts:
                self.executeStmt(stmt)
            self.store.commit()

    def checkDB(self) -> None:
        """ Checks that the required tables are populated. """

        keys = [cfg.KOAN_STORE, cfg.HAIKU_STORE, cfg.REPLY_STORE, cfg.RANT_TABLE]
        for key in keys:
            if self.dbtype is "memcache":
                if self.store.get(key) is None:
                    print("ERROR: Need to load "+ table +" data before running.")
                    exit()
            else:
                result = self.checkTable(key)
                if int(result) < 1:
                    print("ERROR: Need to import "+ key +" before running.")
                    exit()

    def readRandom(self, name) -> str:
        """ Gets a random entry from a list. """

        if self.dbtype is "memcache":
            return(random.choice(self.store.get(name)))
        else:
            self.store.row_factory = None
            if self.dbtype is "sqlite": rand = "RANDOM()"
            else: rand = "RAND()"
            data = self.fetchStmt("* FROM "+ name +" ORDER BY "+ rand +" LIMIT 1")
            if data is None:
                print("ERROR: Please import " + name + " into database.")
                exit()
            return(data[0][0].replace("''", "'"))

    def readVisited(self) -> list:
        """ Gets list of posts already visited. """

        if self.dbtype is "memcache":
            return(self.store.get(cfg.VISITED_STORE))
        else:
            self.store.row_factory = lambda cursor, row: row[0]
            visited = self.fetchStmt("* FROM "+ cfg.VISITED_STORE)
            if len(visited) == 0: return([])
            return(visited)

    def writeVisited(self) -> None:
        """ Saves list of posts already visited. """

        length = len(cfg.already_visited)
        if length > cfg.MAX_VISITED:
            cfg.already_visited = cfg.already_visited[length - cfg.MAX_VISITED:length]

        if self.dbtype is "memcache":
            self.store.set(cfg.VISITED_STORE, cfg.already_visited)
        else:
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
