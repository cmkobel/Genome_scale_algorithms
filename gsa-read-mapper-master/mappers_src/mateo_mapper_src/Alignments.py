#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 16:09:59 2017

@author: mateosokac
"""

import numpy as np
from random import randint
import csv


np.set_printoptions(threshold=np.nan)


class Alignment:
    
    transition_cost = 0
    transversion_cost = 0
    gap_cost = 0 
    match_award = 0
    
    alignment1 = ""
    alignment2 = ""
    max_or_min = ""
    
    score_matrix = []
    D_matrix = []
    I_matrix = []
    gap_extend = 0
    gap_open = 0
    affine_score = 0

    
    
    def __init__(self, max_or_min = "min", match_award = 0, transition_cost = 2, 
                 transversion_cost = 5, gap_cost = 5, gap_extend = 5, gap_open = 5):
        self.transition_cost = transition_cost
        self.transversion_cost = transversion_cost
        self.gap_cost = gap_cost
        self.match_award = match_award
        self.max_or_min = max_or_min
        self.gap_extend = gap_extend
        self.gap_open = gap_open
    
    def load_config_from_file(self, file):
        with open(file, 'r') as file:
            for line in file.readlines():
                parts = line.split(' = ')
                if parts[0] == "transition_cost":
                    self.transition_cost = int(parts[1])
                elif parts[0] == "transversion_cost":
                    self.transversion_cost = int(parts[1])
                elif parts[0] == "gap_cost":
                    self.gap_cost = int(parts[1])
                elif parts[0] == "match_award":
                    self.match_award = int(parts[1].rstrip())
                elif parts[0] == "max_or_min":
                    self.max_or_min = parts[1].rstrip()
                elif parts[0] == "gap_open":
                    self.gap_open = int(parts[1].rstrip())
                elif parts[0] == "gap_extend":
                    self.gap_extend = int(parts[1].rstrip())
                    
    def read_score_matrix_from_text_file(self, file="", max_or_min=""):
        
        self.max_or_min = max_or_min
        
        cols = [1,2,3,4]
        with open(file) as f:
            num_of_rows = f.readline()
            matrix = np.loadtxt(f, usecols = cols)

        
        self.match_award = matrix[0][0]
        self.transition_cost = matrix[0][2]
        self.transversion_cost = matrix[0][1]
        
    def generate_random_string_of_length_n(self, n):
        mystring = ""
        chars = ["A","C","T","G"]
        for i in range(0,n):
            mystring += chars[randint(0, 3)]
        
        return mystring
        
        
    def write_current_time_to_file(self, file, my_dict):
        
        with open(file, 'w') as f:
            for i in range(0,len(my_dict)):
                f.writelines(str(i)+","+str(my_dict[i])+"\n")
            
        
        
    """
        Return matrix full of 0 depeding on size of sequences
    """
    def get_zero_matrix(self, len1, len2):
        matrix = []
        for x in range(0, len1):
            matrix.append([])
            for y in range(0, len2):
                matrix[-1].append(None)
        return matrix
    
    def get_plusInf_matrix(self, len1, len2):
        matrix = []
        for x in range(0, len1):
            matrix.append([])
            for y in range(0, len2):
                matrix[-1].append(float('+inf'))
        return matrix
    
    """This method returns values depending compared characters
       If they are the same we will get an award
       if there is mismatch we will get penalty depending on 
       transversion or transition
    """
    def check_if_match(self, char1, char2):
        if char1 == char2:
            return self.match_award
        elif (char1 == 'C' and char2 == 'T') or (char1 == 'T' and char2 == 'C'): #Transition
            return self.transition_cost
        elif (char1 == 'A' and char2 == 'G') or (char1 == 'G' and char2 == 'A'): #Transition
            return self.transition_cost
        
        return self.transversion_cost
    
    def fill_first_row_and_column(self, score_matrix, m, n):
         #fill the horizontal line
        for i in range(0, m + 1):
            score_matrix[i][0] = self.gap_cost * i
            
        #fill the vertical line
        for j in range(0, n + 1):
            score_matrix[0][j] = self.gap_cost * j
        
        return score_matrix
            
    
    def generate_score_matrix(self, seq1, seq2):
        #Get the lengths of sequences
        m, n = len(seq1), len(seq2)
        global score_matrix
        
        
        score_matrix = self.get_zero_matrix(m+1, n+1)  
        score_matrix = self.fill_first_row_and_column(score_matrix,m , n)
       
        """
            Go thourgh matrix and calculate cost for each
            i -> vertical(m)
            j -> horizontal(n)
        """
        self.cnt = 0
        for i in range(1, m+1):
            for j in range(1, n+1):
                if(score_matrix[i][j] == None):
                    delete = score_matrix[i - 1][j] + self.gap_cost
                    insert = score_matrix[i][j - 1] + self.gap_cost
                    match = score_matrix[i - 1][j - 1] + self.check_if_match(seq1[i-1], seq2[j-1])
                    if self.max_or_min == "min":
                        score_matrix[i][j] = min(match, delete, insert)
                    elif self.max_or_min == "max":
                        score_matrix[i][j] = max(match, delete, insert)
                    elif self.max_or_min == "local":
                        score_matrix[i][j] = max(match, delete, insert, 0)
                
    

        self.score_matrix = score_matrix
        
        return score_matrix
        
    
        
    """
    Recursive method which checks the smallest or largest number in matrix within 3 offered number
    depending on location in matrix. Upon decinding which one is the smallest 
    the method calls itself on that location and proceeds
    """
    def backtrack(self, score_matrix, m, n, seq1, seq2):
        self.cnt = 0
        current_val = score_matrix[m][n]
        diagonal_val = score_matrix[m-1][n-1]
        delete_val = score_matrix[m-1][n]
        insert_val = score_matrix[m][n-1]
        
            
        if (m > 0) and (n > 0) and (current_val ==  diagonal_val + self.check_if_match(seq1[m-1], seq2[n-1])):
            self.alignment1 = seq1[m-1] + self.alignment1
            self.alignment2 = seq2[n-1] + self.alignment2
            self.backtrack(score_matrix, m-1, n-1, seq1, seq2)
        elif (m > 0) and (n >= 0) and (current_val == delete_val + self.gap_cost):
            self.alignment2 =  "-" + self.alignment2
            self.alignment1 = seq1[m-1] + self.alignment1
            self.backtrack(score_matrix, m-1, n, seq1, seq2)
        elif (m >= 0) and (n > 0) and (current_val == insert_val + self.gap_cost):
            self.alignment2 = seq2[n-1] + self.alignment2
            self.alignment1 = "-" + self.alignment1
            self.backtrack(score_matrix, m, n-1, seq1, seq2)            
    

    
    def find_max_value_position(self, score_matrix,m,n):
        
        max_val = 0
        max_i = 0
        max_j = 0
        for i in range(1, m+1):
            for j in range(1, n+1):
                if score_matrix[i][j] > max_val:
                    max_val = score_matrix[i][j]
                    max_i = i
                    max_j = j


        return max_val,max_i,max_j
                
    
    def align_2_sequences_linear(self, seq1, seq2):
        m, n = len(seq1), len(seq2)
        
        seq1 = seq1.upper()
        seq2 = seq2.upper()
        
        if self.max_or_min == "local":
            self.generate_score_matrix(seq1,seq2)
            vals = self.find_max_value_position(score_matrix,m,n)
            print(vals)
            max_val = vals[0]
            i = vals[1]
            j = vals[2]
            self.backtrack(score_matrix, i, j, seq1, seq1)
        else:
            self.backtrack(self.generate_score_matrix(seq1,seq2), m,n, seq1, seq2)

    
    
    
    
    
    def align_2_sequences_affine(self, seq1, seq2):
        self.cnt = 0
        m, n = len(seq1), len(seq2)
        seq1 = seq1.upper()
        seq2 = seq2.upper()

        
        self.score_matrix = self.get_plusInf_matrix(m+1, n+1) 
        self.D_matrix = self.get_plusInf_matrix(m+1, n+1) 
        self.I_matrix = self.get_plusInf_matrix(m+1, n+1) 
        
        self.score_matrix[0][0] = 0
        v1,v2,v3,v4 = float('+inf'),float('+inf'),float('+inf'),float('+inf')
        
        for i in range(0, m+1):
            for j in range(0, n+1):
            
                if(self.score_matrix[i][j] == float('+inf')):
                    if i > 0 and j > 0:
                        v2 = self.score_matrix[i - 1][j - 1] + self.check_if_match(seq1[i-1], seq2[j-1])
                    if i > 0 and j >= 0:
                        self.D_matrix[i][j] = self.calcD(i, j)
                        v3 = self.D_matrix[i][j]
                    if i >= 0 and j > 0:
                        self.I_matrix[i][j] = self.calcI(i, j)
                        v4 = self.I_matrix[i][j]
                    

                    self.score_matrix[i][j] = min(v1, v2, v3, v4)
                        
        self.affine_score = self.score_matrix[m][n]        
        self.backtrack_affine_score_matrix(seq1, seq2)

    
        
    def calcD(self,i,j):
        v1,v2 = float('+inf'),float('+inf')
        if i > 0 and j >= 0: 
            v1 = self.score_matrix[i-1][j] + (self.gap_extend + self.gap_open)
        if i > 1 and j >= 0:
            v2 = self.D_matrix[i - 1][j] + self.gap_extend
            
        return min(v1,v2)

    def calcI(self, i,j):
        v1,v2 = float('+inf'),float('+inf')
        
        if i >= 0 and j > 0: 
            v1 = self.score_matrix[i][j-1] + (self.gap_extend + self.gap_open)
        if i >= 0 and j > 1:
            v2 = self.I_matrix[i][j-1] + self.gap_extend
            
        return  min(v1,v2)
       
    def backtrack_affine_score_matrix(self, seq1, seq2):

        m, n = len(seq1), len(seq2)
        self.cnt = 0
        while (m > 0 or n > 0):
            if (m > 0 and n > 0) and (self.score_matrix[m][n] == self.score_matrix[m-1][n-1] 
            + self.check_if_match(seq1[m-1], seq2[n-1])):
                self.alignment1 = seq1[m-1] + self.alignment1
                self.alignment2 = seq2[n-1] + self.alignment2
                m -= 1
                n -= 1
            else: 
                k = 1
                while True:
                    
                    if (m >= k) and self.score_matrix[m][n] == (self.score_matrix[m-k][n]
                    + self.gap_open + self.gap_extend * k):
                        
                        self.alignment2 =  (k * "-") + self.alignment2 
                        self.alignment1 = seq1[k-1:m] + self.alignment1
                        m -= k
                        break
                    elif (n >= k) and self.score_matrix[m][n] == (self.score_matrix[m][n-k] 
                    +  self.gap_open + self.gap_extend * k):
                        
                        self.alignment2 =  seq2[k-1:n] + self.alignment2 
                        self.alignment1 =  (k * "-") + self.alignment1 
                        n -= k
                        break
                    else:
                        k += 1
