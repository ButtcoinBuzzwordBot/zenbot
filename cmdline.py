import sys, getopt

import config as cfg
import rants

def printUsage(usage, args):
    """ Prints usage message for command line. """

    print("Usage: " + sys.argv[0] + " [", end="")
    print(" | ".join(usage) + "]")
    print("    where <file> = "+ " | ".join(args) + " | all")
    exit(2)

def testData(db, arg) -> None:
    """ Pulls a set of random data for testing. """

    if arg == "templates":
        rant = rants.Rants(db)
        rant.test()
    else:
        print("Tests for "+ arg +" not implemented yet.")
    exit()

def processOpts(db, argv) -> None:
    """ Check optional arguments to import text files into database. """

    if cfg.STORE_TYPE is "memcache":
        print("Data is imported at runtime when memcache is used.")
        exit()

    OPTIONS = [["import", "file"],
               ["test", "file"],
    ]

    ARGS = ["koans", "haiku", "replies", "templates", "rants"]

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
        printUsage(usage, ARGS)

    if argv[1] == "--test":
        testData(db, argv[2])
    elif argv[1] != "--import":
        printUsage(usage, ARGS)

    datafiles = [argv[2]]
    if argv[2] not in ARGS and argv[2] != "all":
        printUsage(usage, ARGS)
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
                try:
                    db.executeStmt("INSERT INTO " + df + " VALUES ('" + line + "')")
                except:
                    print("ERROR: likely single quote in:\n" + line)
                    exit()
            print("Imported " + str(len(data)) + " entries into " + df)

    db.closeDB()
    exit()
