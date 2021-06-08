#!/usr/bin/python
#encoding:utf-8

# Python Package destinated to convert a html-str-table to pandas dataframe  
# Developed by Wesley Silva
# License: GPLv2

import re
import pandas as pd
from bs4 import BeautifulSoup

def DfCreator(html='', first_line_header=True):
    try:
        if type(html)!= type('str'):
            raise Exception('Html param need be str type')
        if html == '':
            raise Exception ('Html param is required!')    

        parser = BeautifulSoup(html, 'xml')
        lines = parser.find_all('tr')
        
        for id, l in enumerate(lines):
            aux=[]
            aux = str(l).split('</td>')
            aux = str(l).split('</th>') if len(aux)==1 else aux 
            aux = aux[:-1]
            for i,a in enumerate(aux):
                data_clean = re.sub('(\n|<tr>|</tr>|<td>|<th>|<thead>|<tr [a-z]*=.*>|<thead [a-z]*=.*>|<th [a-z]*=.*>|<td [a-z]*=.*>)','', a)
                if data_clean != '': aux[i] = data_clean
            lines[id] = aux
        
        headers=[]
        if first_line_header:
            headers = lines.pop(0)
            result = pd.DataFrame(lines, columns=headers)
        else:
            result = pd.DataFrame(lines)
      
        return result
    except Exception as e:
        if hasattr(e, 'message'):
            print(' > ',e.message)
        else:
            print(' > ',e)
        