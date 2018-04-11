import string, re, random
import config as cfg, templates

class Rants:
    """ Class to generate rants using various methods. """

    def __init__(self, db=None):
        self.db = db

    def getTerm(self, table):
        """ Pulls a random term for a placeholder. """

        [term] = self.db.fetchStmt("* FROM "+ table +" ORDER BY RANDOM() LIMIT 1")
        return(str(term.replace("''", "'")))

    def importData(self, fname):
        """ Parses a text file with entries for multiple tables. """

        [numtables, numlines] = [0, 0]
        with open(fname + ".txt", "r", encoding="utf-8") as f:
            for line in f:
                regex = re.compile("\[(\w+)\]")
                table = regex.match(line).group(1)
                self.db.dropTable(table)
                stmt = "CREATE TABLE "+ table +" (phrases varchar(255) NOT NULL)"
                self.db.executeStmt(stmt)
                while True:
                    line = f.readline().replace("\n", "")
                    if line == "": break
                    stmt = "INSERT INTO "+ table +" VALUES ('"+ line + "')"
                    self.db.executeStmt(stmt)
                    numlines += 1
                numtables += 1
            self.db.store.commit()
            print(numlines, "entries imported into", numtables, "tables.")
            exit()

    def getTemplate(self) -> dict:
        """ Parses a template and replaces placeholders with random terms. """

        [keys, [template]] = random.choice(templates.templates)
        template = template.replace("''", "'")
        for key in keys:
            if key == "int":
                val = str(random.randrange(2, 200))
            else:
                val = self.getTerm(key)
            template = template.replace("["+ key +"]", val, 1)
            
        if cfg.DEBUG:
            print(template)
            exit()
        return(template)
