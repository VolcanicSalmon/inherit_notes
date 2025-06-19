#!/usr/bin/env python3
import argparse
import os
from argparse import ArgumentParser
parser=ArgumentParser()
parser.add_argument('--hwe',type=str,description="the hardy output from the vcf files obtained from vcftools")
parser.add_argument('--temphwe',type=str)
parser.add_argument('--outname',type=str)
args=parser.parse_args()
os.system(f"awk -v OFS='\t' '{{print $1,$2,$3}}' {args.temphwe} > {args.hwe}")
with open(args.temphwe,'r') as hweinput:
    lines=hweinput.readlines()
    outputrows=[]
    header = ['N', 'p', 'q', 'exphet', 'exphet_ind', 'p', 'q', 'pfreq', 'qfreq', 'exphet_hohenlohe', 'exphet_ind_hohenlohe', 'ohet', 'fis', 'fis_hohenlohe']
    for line in lines[1:]:
        chrom=line.strip().split('\t')[0]
        pos=line.strip().split('\t')[1]
        obs=line.strip().split('\t')[2]
        ohom1=int(obs.split('/')[0])
        ohet=int(obs.split('/')[1])
        ohom2=int(obs.split('/')[2])
        N=2*(ohom1+ohet+ohom2)
        p=(2*ohom1+ohet)/int(N) 
        q=(2*ohom2+ohet)/int(N) 
        exphet=2*p*q 
        exphet_ind=exphet*N/2 
        pfreq=(p*N*(p*N-1))/(N*(N-1))
        qfreq=(q*N*(q*N-1))/(N*(N-1))
        exphet_Hohenlohe=1-(pfreq+qfreq)
        exphet_ind_hohenlohe=exphet_Hohenlohe*N/2 
        ohet=ohet/(N/2)
        if exphet>0:
            fis=1-(ohet/exphet)
        else:
            fis=0
        if exphet_Hohenlohe >0:
            fis_hohenlohe=1-(ohet/exphet_Hohenlohe)
        else:
            fis_hohenlohe=0
        row=[int(N),chrom, pos, p,q,exphet,exphet_ind,pfreq,qfreq,exphet_Hohenlohe,exphet_ind_hohenlohe,ohet,fis,fis_hohenlohe]
        if not(ohet>=1 or fis<= -1 or fis_hohenlohe<= -1):
            outputrows.append(row)
with open(args.outname,'w') as outfile:
    outfile.write('\t'.join(header)+'\n')
    for row in outputrows:
        outfile.write('\t'.join(str(element) for element in row)+'\n')

