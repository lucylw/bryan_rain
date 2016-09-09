#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Determine whether it rains in Seattle when Bryan is here
# created: 2016.8.29 lucylw@uw.edu

import os, sys
import csv
import math
from datetime import datetime
import pickle

climateData = []

with open("/Users/lwang/Projects/bryan_rain/nws_seattle_plus_bryan.csv","rb") as dataFile:
    dataReader = csv.reader(dataFile, delimiter=',')
    headers = dataReader.next()
    for row in dataReader:
        climateData.append(row)

date = []
highTemp = []
lowTemp = []
precipAmt = []
precipitation = []
bryanInTown = []

for row in climateData:
    date.append(datetime.strptime(row[0], '%Y-%m-%d'))
    highTemp.append(int(row[1]))
    lowTemp.append(int(row[2]))
    if row[7]=='T':
        precipAmt.append(0.0)
    else:
        precipAmt.append(float(row[7]))
    precipitation.append(int(row[8]))
    bryanInTown.append(int(row[11]))


N = len(climateData)
n00 = 0
n10 = 0
n01 = 0
n11 = 0

a0 = [0.0,0]
a1 = [0.0,0]

for b,p,a in zip(bryanInTown,precipitation,precipAmt):
    if (b==0) and (p==0):
        n00 += 1
    elif (b==1) and (p==0):
        n10 += 1
    elif (b==0) and (p==1):
        n01 += 1
    elif (b==1) and (p==1):
        n11 += 1
    else:
        print("Problem... b=%i, p=%i" % (b,p))

    if (a>0):
        if (b==0):
            a0[0] += a
            a0[1] += 1
        else:
            a1[0] += a
            a1[1] += 1

n1_ = n11+n10
n0_ = n01+n00
n_1 = n01+n11
n_0 = n00+n10

phi = float(n11*n00 - n10*n01)/math.sqrt(float(n1_*n0_*n_0*n_1))
chi_sq = float(N) * (phi**2)
chi_crit = 3.84

print("\nProbability of rain:")
print("Bryan here: %.f%%" % (100.0*float(n11)/float(n1_)))
print("Bryan gone: %.f%%" % (100.0*float(n01)/float(n0_)))

print("\nAmount of rain per rainy day:")
print("Bryan here: %.2f in" % (a1[0]/float(a1[1])))
print("Bryan gone: %.2f in" % (a0[0]/float(a0[1])))

print("\nContingency Table:")
print("|---------------|-----------|-----------|-----------|")
print("|\t\t\t\t|\tRain\t|\tNo rain\t|\tTotal\t|")
print("|---------------|-----------|-----------|-----------|")
print("|\tBryan here\t|\t%i\t\t|\t%i\t\t|\t%i\t\t|" % (n11,n10,n1_))
print("|\tBryan gone\t|\t%i\t\t|\t%i\t\t|\t%i\t\t|" % (n01,n00,n0_))
print("|---------------|-----------|-----------|-----------|")
print("|\tTotal\t\t|\t%i\t\t|\t%i\t\t|\t%i\t\t|" % (n_1,n_0,N))
print("|---------------|-----------|-----------|-----------|")

print("\nPhi coefficient: %.2f" % phi)
print("\nChi square value: %.2f" % chi_sq)
print("Critical value: %.2f" % chi_crit)

if chi_sq>chi_crit:
    print("\nChi square value greater than critical value, reject null hypothesis at alpha = 0.05")
else:
    print("\nChi square value less than critical value, do not reject null hypothesis")


