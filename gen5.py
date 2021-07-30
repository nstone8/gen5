import io
import pandas as pd
import numpy as np

def _get_one_table(f):
    #trim any leading whitespace
    this_line=f.readline()
    if not this_line:
        print('EOF')
        return
    while not this_line.strip():
        this_line=f.readline()

    #first non-empty line should be our table title
    title=this_line.strip()
    print(title)
    #get rid of any intervening empty lines

    this_line=f.readline()
    while not this_line.strip():
        this_line=f.readline()
    
    #now gobble up every line until we hit a new empty line

    text_buf=io.StringIO()

    while this_line.strip():
        text_buf.write(this_line)
        this_line=f.readline()

    text_buf.seek(0)
    table=pd.read_csv(text_buf,sep='\t',low_memory=False,dtype={'Well':str})
    #fill in well info
    new_well_col=[]
    cur_well=None
    for cell in table['Well']:
        if type(cell)==str:
            cur_well=cell
        new_well_col.append(cur_well)
    table.loc[:,'Well']=new_well_col

    return title,table
        

def get_tables_from_file(filepath):
    tables={}
    with open(filepath,'rt') as f:
        res=_get_one_table(f)
        while res:
            tables[res[0]]=res[1]
            res=_get_one_table(f)
    return tables
            
