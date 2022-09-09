# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 17:57:43 2022

@author: Yann Miquel
"""
import sys
from utils_cv import cv_to_markdown
from pathlib import Path

if len(sys.argv)!=2:
    print("the path is missing or too many args")
    sys.exit(0)

p = Path(sys.argv[1])
files = list(p.glob('**/*.hdbcalculationview'))
#markdown = cv_to_markdown(FILE,lang="EN")

markdown = ""
for file in list(p.glob('**/*.hdbcalculationview')):
    with file.open(encoding="UTF-8") as f:
        markdown += cv_to_markdown(f,lang="FR") # EN is possible

with open(sys.argv[1]+"/doc.md", "w") as f:
    f.write(markdown)
    print("done!")
