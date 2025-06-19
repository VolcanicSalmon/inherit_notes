#!/usr/bin/env python3
import argparse
from argparse import ArgumentParser
import os
parser=ArgumentParser()
parser.add_argument('--vcf',type=str)
parser.add_argument('--outvcf',type=str)
parser.add_argument('--tempfile',type=str)
parser.add_argument('--cores',type=int)
args=parser.parse_args()
os.system('perl /storage/plzen1/home/kli/annovar/table_annovar.pl --threads '+str(args.cores)+' '+args.vcf+' /storage/plzen1/home/kli/annovar/humandb/ -buildver hg19 -out '+args.outvcf +' -remove -protocol refGene,cytoBand,exac03,avsnp147,dbnsfp30a  '+ '-operation gx,r,f,f,f -nastring . -vcfinput')
annotated=args.outvcf+'.hg19_multianno.vcf'
if os.path.exists(annotated):
    print(f'annotated vcf is {annotated}')
else:
    print('no vcf output')
