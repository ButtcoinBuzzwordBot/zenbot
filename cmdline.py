import os, getopt
import config as cfg, rants

def printUsage(usage):
    """ Prints usage message for command line. """

    name = os.path.basename(__file__)
    print("Usage: " + name + " [", end="")
    print("|".join(usage) + "]")
    print("    where <file> = koans|haiku|rants|replies|all")
    exit(2)
        
def processOpts (db, argv) -> None:
    """ Check optional arguments to import text files into database. """

    if cfg.STORE_TYPE is "memcache":
        print("Data is imported at runtime when memcache is used.")
        exit()

    OPTIONS = [["import", "file"]]
    ARGS = ["koans", "haiku", "replies", "rants"]

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
    if argv[2] not in ARGS and argv[2] != "all":
        printUsage(usage)
    elif argv[2] == "all":
        datafiles = ARGS

    for df in datafiles:
        if df == "rants":
            rant = rants.Rants(db)
            rant.importData(df)
            if argv[2] == "rants":
                exit()
        else:
            dataf = open(df + ".txt", "r", encoding=cfg.ENCODING)
            data = dataf.read().split("|")
            dataf.close()

            db.deleteTable(df)
            for line in data:
                if cfg.DEBUG: print("Adding: " + line)
                db.executeStmt("INSERT INTO " + df + " VALUES ('" + line + "')")
            print("Imported " + str(len(data)) + " entries into " + df)

    db.closeDB()
    exit()
