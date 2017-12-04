#!/usr/bin/env python
print('importing...')

import csv
import os

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
nltk.download('stopwords')

import mincemeat

# read data
print('reading data...')
data = []
dirpath = './sherlock/'
tokenizer = RegexpTokenizer(r'\w+')
stops = set(stopwords.words("english"))
files = os.listdir(dirpath)
for filename in files:
    with open(os.path.join(dirpath, filename)) as f:
        pred = tokenizer.tokenize(f.read().lower())
        data.append([w for w in pred if w not in stops])
datasource = dict(enumerate(data))

# mapreduce
def mapfn(k, v):
    for word in v:
        # yield (k, word), 1
        yield word, (k, 1)

def reducefn(k, vs):
    from collections import defaultdict
    # return sum(vs)
    d = defaultdict(int)
    for elem in vs:
        d[elem[0]] += 1
    return d

s = mincemeat.Server()
s.datasource = datasource
s.mapfn = mapfn
s.reducefn = reducefn

# wait for workers
print('waiting for workers...')
results = s.run_server(password="changeme")

# write data
print('writing results...')
with open('inv_index.csv', 'wb') as csvout:
    w = csv.writer(csvout, delimiter=';')
    w.writerow(['word'] + files)
    n = len(files)
    for elem in sorted(results.iteritems()):
        w.writerow([elem[0]] + [elem[1][i] for i in range(n)])
print('finished')
