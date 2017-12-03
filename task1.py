#!/usr/bin/env python
print('importing...')
import mincemeat
import csv
import re
import nltk
from nltk.tokenize import RegexpTokenizer

# read data
print('reading data...')
data = []
with open('./southpark/All-seasons.csv') as f:
    r = csv.reader(f, delimiter=',')
    r.next()
    tokenizer = RegexpTokenizer(r'\w+')
    for row in r:
        s = row[2].replace('Eric Cartman', 'Cartman').replace('Kyle Broflovski', 'Kyle')
        res = [w.strip() for w in re.split(',|/| and ', s)]
        data.append((res, tokenizer.tokenize(row[3].lower())))
datasource = dict(enumerate(data))

# mapreduce
def mapfn(k, v):
    for name in v[0]:
        for word in v[1]:
            yield name, word

def reducefn(k, vs):
    result = [len(set(vs)), len(vs)]
    result.append(float(result[0]) / float(result[1]))
    return result

s = mincemeat.Server()
s.datasource = datasource
s.mapfn = mapfn
s.reducefn = reducefn

# wait for workers
print('waiting for workers...')
results = s.run_server(password="changeme")

# write data
def sortByPercentage(elem):
    return elem[1][-1]

def sortByUnique(elem):
    return elem[1][0]

def sortByTotal(elem):
    return elem[1][1]

print('writing results...')
with open('lang_divers.csv', 'wb') as csvout:
    w = csv.writer(csvout, delimiter=';')
    w.writerow(['name', 'unique', 'total', 'ratio'])
    for elem in sorted(results.iteritems(), key=sortByUnique, reverse=True):
        w.writerow([elem[0]] + elem[1])
print('finished')
