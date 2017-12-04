#!/usr/bin/env python
print('importing...')

import csv
import os
import argparse

from collections import defaultdict

import mincemeat

# read data
print('reading data...')
parser = argparse.ArgumentParser()
parser.add_argument('--file', help='csv file with matricies', required = True)
parser.add_argument('--m1', help='first matrix name', required = True)
parser.add_argument('--m2', help='second matrix name', required = True)
args= parser.parse_args()

dirpath = './matricies/'
filename = args.file
matrix1 = args.m1
matrix2 = args.m2

dataA = defaultdict(dict)
dataB = defaultdict(dict)
with open(os.path.join(dirpath, filename), 'rb') as f:
    r = csv.reader(f, delimiter=',')
    r.next()
    for row in r:
        if row[0] == matrix1:
            dataA[int(row[1])][int(row[2])] = float(row[3])
        elif row[0] == matrix2:
            dataB[int(row[2])][int(row[1])] = float(row[3])

# no presence and size check

data = []
for key, val in dataA.iteritems():
    vec = [v for k, v in sorted(val.iteritems())]
    data.append((1, key, vec))
for key, val in dataB.iteritems():
    vec = [v for k, v in sorted(val.iteritems())]
    data.append((2, key, vec))
datasource = dict(enumerate(data))

# mapreduce
def mapfn(k, v):
    if v[0] == 1:
        for j in range(len(v[2])):
            yield (v[1], j), v[2]
    else:
        for i in range(len(v[2])):
            yield (i, v[1]), v[2]

def reducefn(k, vs):
    res = 0.0
    for k in range(len(vs[0])):
        res += vs[0][k] * vs[1][k]
    return res

s = mincemeat.Server()
s.datasource = datasource
s.mapfn = mapfn
s.reducefn = reducefn

# wait for workers
print('waiting for workers...')
results = s.run_server(password="changeme")
print(results)

# write data
print('writing results...')
with open('C.csv', 'wb') as csvout:
    w = csv.writer(csvout, delimiter=',')
    w.writerow(['matrix', 'row', 'column', 'value'])
    for k, v in sorted(results.iteritems()):
        w.writerow(['C', k[0], k[1], v])
print('finished')
