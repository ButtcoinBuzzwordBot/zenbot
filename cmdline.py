import os, getopt
import config as cfg, rants

def printUsage(usage):
    """ Prints usage message for command line. """

    name = os.path.basename(__file__)
    print("Usage: " + name + " [", end="")
    print("|".join(usage) + "]")
    print("    where <file> = koans|haiku|rants|replies")
    exit(2)
        
def processOpts (db, argv) -> None:
    """ Check optional arguments to import text files into database. """

    OPTIONS = [["import", "file"]]
    ARGS = ["koans", "haiku", "rants", "replies"]
        
    opts, usage = [],[]
    for opt,arg in OPTIONS:
        syntax = "--" + opt
        if arg is not "":
            syntax += " <" + arg + ">"
            opt += "="
        opts.append(opt)
        usage.append(syntax)

    # Process command line options, print usage info on errors.
    try:
        [(option, file)] = getopt.getopt(argv[1:], "", opts)[0]
    except getopt.GetoptError:
        printUsage(usage)

    datafiles = [argv[2]]
    if argv[2] not in ARGS:
        printUsage(usage)
    elif argv[2] == "all":
        datafiles = ARGS

    for df in datafiles:
        if df == "rants":
            rant = rants.Rants(db)
            rant.importData(table)
            if argv[2] == "rants":
                exit()
        else:
            dataf = open(table + ".txt", "r", encoding=cfg.ENCODING)
            data = dataf.read().split("|")
            dataf.close()

            db.deleteTable(table)
            for line in data:
                if cfg.DEBUG: print("Adding: " + line)
                db.executeStmt("INSERT INTO " + table + " VALUES ('" + line + "')")
            db.closeDB()
            print("Imported " + str(len(data)) + " entries into " + table)
    exit()
