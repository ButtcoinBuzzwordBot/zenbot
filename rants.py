import string, re, random
import config as cfg, templates

class Rants:
    """ Class to generate rants using various methods. """

    def __init__(self, db=None):
        self.db = db

    def test(self) -> None:
        """ Prints a set of random templates for testing. """

        for i in range(0,3):
            print(self.getTemplate() + "\n----\n")
    
    def getTerm(self, table):
        """ Pulls a random term for a placeholder. """

        terms = self.db.fetchStmt("* FROM lex_"+ table +" ORDER BY RANDOM() LIMIT 5")
        term = random.choice(terms)
        return(term.replace("''", "'"))

    def importData(self, fname):
        """ Parses a text file with entries for multiple tables. """

        [numtables, numlines] = [0, 0]
        with open(fname + ".txt", "r", encoding="utf-8") as f:
            for line in f:
                regex = re.compile("\[(\w+)\]")
                table = "lex_" + regex.match(line).group(1)
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
            print("Imported", numlines, "rant entries into", numtables, "tables")
            exit()

    def getTemplate(self) -> str:
        """ Loads a random template and replaces placeholders with random terms. """

        text = self.db.readRandom(cfg.TEMPLATE_STORE).replace("\n", " ")
        regex = re.compile("([^<]*)<(\w+)>(.*)")
        template = ""

        while (len(text) > 0):
            try:
                ltext = regex.match(text).group(1)
                key = regex.match(text).group(2)
                text = regex.match(text).group(3)
            except:
                break

            if key == "int":
                val = str(random.randrange(2, 200))
            else:
                val = self.getTerm(key)
            template += ltext + val

        return(template.replace("\\n", "\n") + text)
