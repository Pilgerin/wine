# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 13:10:36 2020

@author: Daria
"""
def read_seq(inputfile):
    '''Reads data from a file and returns it in a sequence 
    with special characters removed'''   
    with open(inputfile,'r') as f:
        seq = f.read()
    seq = seq.strip()
    print (seq)
    return seq


def translate(seq):
    '''Translates a string containing nucleotide sequence into a string 
    containing the corresponding sequence of amino acids. 
    Nucleotids are translated into triplets using the table dictionary, 
    each amino acid is encoded with a single letter'''
    
    protein=''    
    table = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
        'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
    }
    if len(seq)%3==0:
        pass
    
    for i in range(0,len(seq),3):
        codon = seq [i:i+3]
        print (codon)
        protein += table[codon]
    print (protein)
    return protein

prt = read_seq("protein.txt")
dna = read_seq('dna.txt')
translate(dna[20:938])[:-1]


    

