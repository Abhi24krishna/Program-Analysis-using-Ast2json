import json
from ast import parse
from ast2json import ast2json

ast=ast2json(parse(open("/path/test1.py").read())) #path of the testcase

with open("sample.json", "w") as outfile: 
    json.dump(ast, outfile) 
