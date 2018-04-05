import os
import getopt
import sqlite3
#import PyMySQL

import config as cfg

def processOpts (db, argv) -> None:
    """ Check optional arguments to import text files into database. """

    OPTIONS = [
        ["import", "file"],
    ]

    opts, usage = [],[]
    for opt,arg in OPTIONS:
        syntax = "--" + opt
        if arg is not "":
            syntax += " <" + arg + ">"
            opt += "="
        opts.append(opt)
        usage.append(syntax)

    # Process command line options.
    try:
        [(option, file)] = getopt.getopt(argv[1:], "", opts)[0]
    except getopt.GetoptError:
        name = os.path.basename(__file__)
        print("Usage: " + name + " [", end="")
        print("|".join(usage) + "]")
        print("    where <file> = koans|haiku")
        exit(2)

    table = argv[2]
    dataf = open(table + ".txt", "r")
    data = dataf.read().split("|")
    dataf.close()

    for line in data:
        if cfg.DEBUG: print("Adding: " + line)
        db.executeStmt("INSERT INTO " + table + " VALUES ('" + line + "')")
    db.closeDB()
    print("Imported " + str(len(data)) + " lines into " + table)
    exit()
