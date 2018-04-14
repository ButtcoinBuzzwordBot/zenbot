import os, re, random
import config as cfg

if cfg.STORE_TYPE is "memcache":
    import memcache
elif cfg.STORE_TYPE is "sqlite":
    import sqlite3
elif cfg.STORE_TYPE is "mysql":
    import pymysql as mysql

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
                raise cfg.ExitException(
                    err + "\nERROR: Cannot create or connect to "+ cfg.DATABASE)

        elif dbtype is "mysql":
            try:
                self.store = mysql.connect(host=cfg.MYSQL_HOST,
                                           user=cfg.MYSQL_USER,
                                           password=cfg.MYSQL_PW,
                                           db=cfg.DATABASE,
                                           charset='utf8')
            except mysql.Error as err:
                raise cfg.ExitException(
                    err + "\nERROR: Cannot create or connect to "+ cfg.DATABASE)

            cur = self.store.cursor()
            cur.execute("SHOW TABLES LIKE '"+ cfg.VISITED_STORE +"'")
            result = cur.fetchone()
            if result is None:
                dbexists = False
            cur.close()

        elif dbtype is "memcache":
            try:
                self.store = memcache.Client(['localhost:11211'], debug=1)
                if cfg.DEBUG:
                    self.getMemcacheStats()
            except:
                raise cfg.ExitException("ERROR: Unable to initialize memcache.")
            self.createDB()

        else:
            raise cfg.ExitException("Database type "+ dbtype +" not supported.")

        if not dbexists:
            self.createDB()
            raise cfg.ExitException("Database created. Please import all tables.")

        cfg.already_visited = self.readVisited()

    def getMemcacheStats(self) -> None:
        """ Prints memcache stats for debugging. """

        for node_stats in self.store.get_stats():
            server, stats = node_stats
            print ('-----------------------------------------')
            print (server)
            print ('-----------------------------------------')
            for stat_name, value in sorted(stats.iteritems()):
                if not stat_name.startswith('ep'):
                    if stat_name not in ('libevent', 'version'):
                        print (stat_name.ljust(25), value.rjust(15))
                print ('-----------------------------------------')
            for stat_name, value in sorted(stats.iteritems()):
                if stat_name.startswith('ep'):
                    if stat_name not in ('ep_dbname', 'ep_version'):
                        print (stat_name.ljust(25), value.rjust(15))

    def executeStmt(self, stmt) -> None:
        """ Executes an atomic database operation. """

        try:
            cur = self.store.cursor()
            cur.execute(stmt)
        except:
            raise cfg.ExitException("ERROR: Cannot execute " + stmt)
        finally:
            cur.close()

    def fetchStmt(self, stmt) -> list:
        """ Executes a SELECT statement and returns fetched results. """

        try:
            cur = self.store.cursor()
            cur.execute("SELECT "+ stmt)
            data = cur.fetchall()
        except sqlite3.Error as err:
            raise cfg.ExitException(err + "\nERROR: Cannot execute SELECT " + stmt)
        finally:
            cur.close()
        return(data)

    def checkTable(self, table) -> int:
        """ Checks to see if a table/keystore exists. """

        if self.dbtype is "sqlite" or self.dbtype is "mysql":
            try:
                cur = self.store.cursor()
                cur.execute("SELECT COUNT(*) FROM "+ table)
                [count] = cur.fetchall()
            except:
                print("\nERROR: Cannot execute SELECT " + stmt)
                return(0)
            finally:
                cur.close()
        elif self.dbtype is "memcache":
            if self.store.get(table) is None:
                count = 0
        return(count)
        
    def deleteTable(self, table) -> None:
        """ Deletes all entries from a table. """

        if self.dbtype is "sqlite" or self.dbtype is "mysql":
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
                    raise cfg.ExitException(
                        "ERROR: Data file "+ key +".txt does not exist.")
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
                    raise cfg.ExitException(
                        "ERROR: Need to load "+ key +" data before running.")
            else:
                result = self.checkTable(key)
                if int(result) < 1:
                    raise cfg.ExitException(
                        "ERROR: Need to import "+ key +" before running.")

    def readRandom(self, name) -> str:
        """ Gets a random entry from a list. """

        if self.dbtype is "memcache":
            return(random.choice(self.store.get(name)))
        else:
            self.store.row_factory = None
            if self.dbtype is "sqlite": rand = "RANDOM()"
            else: rand = "RAND()"
            data = self.fetchStmt("* FROM "+ name +" ORDER BY "+ rand +" LIMIT 5")
            if data is None:
                raise cfg.ExitException(
                    "ERROR: Please import " + name + " into database.")
            entry = random.choice(data)
            return(entry[0].replace("''", "'"))

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
