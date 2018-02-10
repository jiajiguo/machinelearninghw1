# -*- coding: utf-8 -*-
"""
Created on Fri Feb 09 17:00:06 2018

@author: Jiaji Guo
"""

import csv
import numpy

f_in = 'tic-tac-toe.data.txt'
f_test = 'tic-tac-toe.test.txt'
#readfile to list
def read_file(filename):
    data =[]
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row[0].split())    
    return data

#vector_zoom (list, float)
def vector_zoom(vector, times):
    new_vect = numpy.zeros((len(vector), len(vector[0])))
    for i in range(len(vector)):
        for j in range(len(vector[0])):
            new_vect[i][j] = vector[i][j] * times
    return new_vect

posi_total = 0
nega_total = 0
posi_times = numpy.zeros((9,3))
nega_times = numpy.zeros((9,3))

raw_data = read_file(f_in)
raw_test = read_file(f_test)

for i in range(len(raw_data)):
    if raw_data[i][9] == 'positive':
        posi_total = posi_total + 1
    if raw_data[i][9] == 'negative':
        nega_total = nega_total + 1
        
for i in range(len(raw_data)):
    for j in range(len(raw_data[0])-1):
        if raw_data[i][j] == 'x' and raw_data[i][9] == 'positive':
            posi_times[j][0] = posi_times[j][0] + 1
        if raw_data[i][j] == 'o' and raw_data[i][9] == 'positive':
            posi_times[j][1] = posi_times[j][1] + 1 
        if raw_data[i][j] == 'b' and raw_data[i][9] == 'positive':
            posi_times[j][2] = posi_times[j][2] + 1 
        if raw_data[i][j] == 'x' and raw_data[i][9] == 'negative':
            nega_times[j][0] = nega_times[j][0] + 1
        if raw_data[i][j] == 'o' and raw_data[i][9] == 'negative':
            nega_times[j][1] = nega_times[j][1] + 1 
        if raw_data[i][j] == 'b' and raw_data[i][9] == 'negative':
            nega_times[j][2] = nega_times[j][2] + 1
            
#conditional probability => c_prob
posi_c_prob = vector_zoom(posi_times, float(1)/float(posi_total))
nega_c_prob = vector_zoom(nega_times, float(1)/float(nega_total))

right_num = 0
for i in range(len(raw_test)):
    curr = raw_test[i]
    #evidence also names as normalizing constant, from wikipedia 
    # https://en.wikipedia.org/wiki/Naive_Bayes_classifier
    #evidence = evidence_part1 + evidence_part2 = evi_p + evi_n
    evi_p = float(posi_total)/float(len(raw_data))
    evi_n = float(nega_total)/float(len(raw_data))
    for row in range(len(raw_test[0])-1):
        if curr[row]  == 'x':
            evi_p = evi_p * posi_c_prob[row][0]
            evi_n = evi_n * nega_c_prob[row][0]
        if curr[row] == 'o':
            evi_p = evi_p * posi_c_prob[row][1]
            evi_n = evi_n * nega_c_prob[row][1]
        if curr[row] == 'b':
            evi_p = evi_p * posi_c_prob[row][2]
            evi_n = evi_n * nega_c_prob[row][2]
    #count the number of correct times, evaluate the model
    if evi_p > evi_n :
        temp = 'positive'
    else:
        temp = 'negative'
    if temp == curr[9]:
        right_num = right_num + 1

print 'so the correct rate is ', right_num, '/', len(raw_test)
print 'correct rate is', float(right_num) / float(len(raw_test))
            
