# coding: utf-8
import re
with open('ResultsWithOutsideData.txt', 'r') as f:
    entries = []
    for line in f:
        data = re.split("( |\t|\n)", line);
        data = filter(lambda x: len(x) > 2, data)
        entries.append(data)

entries.sort(key=lambda x: (x[-2], -float(x[-1])))
for entry in entries:
    print entry
