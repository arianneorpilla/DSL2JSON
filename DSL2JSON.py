import sys
import os
import re
import zipfile
import subprocess
import sys

'''
DSL2JSON - A script for converting DSL format dictionaries compatible
with GoldenDict to the Migaku Dictionary format.

Written for the language learning community 
by Leo Rafael Orpilla

github.com/lrorpilla
leorafaelorpilla@gmail.com

This software is free to use with no warranties.
'''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Entry:
    def __init__(self, term, altterm = "", pronunciation = "", definition = "", pos = "", examples = "", audio = ""):
        self.term = term
        self.altterm = altterm
        self.pronunciation = pronunciation
        self.definition = definition
        self.pos = pos
        self.examples = examples
        self.audio = audio

    def print_entry(self, outFile):
        q = "\""
        openBracket = "{"
        closeBracket = "}"

        with open(outFile, 'a+', encoding=encoding) as o:
            o.write(f"{openBracket}{q}term{q}: {q}{self.term}{q}, {q}altterm{q}: "
                f"{q}{self.altterm}{q}, {q}pronunciation{q}: {q}{self.pronunciation}{q}, "
                f"{q}definition{q}: {q}{self.definition}{q}, {q}pos{q}: {q}{q}, {q}examples{q}: "
                f"{q}{self.examples}{q}, {q}audio{q}: {q}{self.audio}{q}{closeBracket}")
            

def import_entries(data, dictionaryName, outFile):
    unimported = data.split("\n")

    unimported.insert(0, "DSL2JSON")
    unimported.insert(1, "\tnoun")
    unimported.insert(2, "\tThis dictionary was imported with DSL2JSON. This is a dummy value for the DSL2JSON converter, ignore this term.")

    unimported.append("DSL2JSON-end")
    unimported.append("\tnoun")
    unimported.append("\tThis dictionary was imported with DSL2JSON. This is a dummy value for the DSL2JSON converter, ignore this term..")

    i = 0
    term = ""
    definition = ""

    while unimported:
        if term == "":
            term = unimported[0]
            del unimported[0]
            continue

        if unimported[0].startswith("\t"):
            append = unimported[0].replace("\t", "")
            append = append.replace("~", term)
            append = append + "<br>"

            definition = definition + append
            del unimported[0]
            continue
        else:
            if "DSL2JSON" not in term:
                i = i + 1

                if i != 0:
                    with open(outFile, 'a+', encoding=encoding) as o:
                        o.write(f",")

                print(f"[{i}] {bcolors.OKCYAN}[DSL2JSON]{bcolors.ENDC} Processed dictionary entry from {bcolors.OKCYAN}{dictionaryName}{bcolors.ENDC}: {term}")

            entry = Entry(term.replace("\t", ""), "", "", definition, "", "", "")
            entry.print_entry(outFile)

            term = ""
            definition = ""

    return i

def get_lines(inFile):
    with open(inFile, 'r', encoding=encoding) as i:
        data = i.readlines()
        dictionaryName = data[0].replace("#NAME", "").replace("\t", "").replace("\"", "")

        return data, dictionaryName

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

print(f'''
{bcolors.OKGREEN}DSL2JSON{bcolors.ENDC} - A script for converting DSL format dictionaries compatible
with GoldenDict to the Migaku Dictionary format.

Written for the language learning community 
by {bcolors.OKGREEN}Leo Rafael Orpilla{bcolors.ENDC}

{bcolors.OKGREEN}github.com/lrorpilla
leorafaelorpilla@gmail.com{bcolors.ENDC}

This software is free to use with no warranties.

The script may take some time before it starts. Please be patient.''')

inFile = sys.argv[1]
outFile = "DSL2JSON.json"

install_and_import("chardet")
chardet = globals()["chardet"]

rawdata = open(inFile, 'rb').read()
result = chardet.detect(rawdata)
encoding = result['encoding']

data, dictionaryName = get_lines(inFile)

del data[2]
del data[1]
del data[0]

allLines = ""
allLines = allLines.join(data)

allLines = allLines.replace("[", "<")
allLines = allLines.replace("]", ">")
allLines = allLines.replace("{{", "<")
allLines = allLines.replace("}}", ">")
allLines = allLines.replace("<m0>", "")
allLines = allLines.replace("<m1>", "  ")
allLines = allLines.replace("<m2>", "    ")
allLines = allLines.replace("<m3>", "      ")
allLines = allLines.replace("\\", "/")
allLines = allLines.replace("\"", "\\\"")

allLines = re.sub('<[^<]+?>', '', allLines)

with open(outFile, 'a', encoding=encoding) as o:
    o.truncate(0)
    o.write(f"[")

total_entries = import_entries(allLines, dictionaryName, outFile)

with open(outFile, 'a', encoding=encoding) as o:
    o.write(f"]")

zipfile.ZipFile('DSL2JSON.zip', mode='w').write("DSL2JSON.json")

print(f"\n{bcolors.OKGREEN}[DONE] {bcolors.OKCYAN}[DSL2JSON]{bcolors.ENDC} Processed {total_entries} dictionary entries from{bcolors.OKCYAN}{dictionaryName}{bcolors.ENDC}: Dictionary can be imported with DSL2JSON.zip")
