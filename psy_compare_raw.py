# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 15:07:09 2016
@author: advena
"""
#import re
from datetime import datetime
#import numpy as np
import pandas as pd 
import os 
import sys
import shutil
from dateutil import parser

########################################################################
#                             User Inputs                              #
########################################################################
# Do not edit the PJM owner list (except to correct it)
pjm_owner_list=[202,205,209,212,215,222,225,320,345]

# Filter the data down to these owners.
# For PJM only, set compare_owner_list = pjm_owner_list
# For all untis, set compare_owner_list = []
compare_owner_list = pjm_owner_list

#src_dir = r'K:\AFC_MODEL_UPDATES\2016_S\IDC Models'
src_dir = r'K:\AFC_MODEL_UPDATES\2016_S\IDC Models'

# Working directory.  If src_dir != tgt_dir, a copy of the original raw
# files is copied to tgt_dir to prevent corruption of the originals.
# The copy here will have be modified; a new line will be added to the top 
# to allow for csv parsing without error.
tgt_dir = r'C:\temp'

# The raw files to compare
raw_file1 = r'sum16idctr1p4_v32.RAW'
raw_file2 = r'sum16idctr1p6_v32.RAW'

# Maximim number of columns in any row, likely 28.
max_cols = 28  # set to zero to automatically determine.

# The regex pattern (before compiling) the identifies the header to a new section of the log file.
end_of_section_pattern="0 / "

########################################################################
#               Function Dfinitions                 #
########################################################################
def max_col_cnt(filename):
    '''
    Finds row with mwx number of columns by counting commas
    '''
    max_commas = 0
    lines = open(filename)
    for line in lines:
        cnt = line.count(',')
        if cnt > max_commas:
            max_commas = cnt
    return max_commas + 1

def raw_to_df(src_dir, tgt_dir, filename, max_cols=28):
    '''
    src_dir: directory in which the raw files are located
    tgt_dir: directory in which to copy the files 
             (to prevent corrupting originals)
    filename: name of raw file (exluding path)
    ins_hdr: True to add a generic header to the file (col1, col2, ...)
             False if you already added a header to the file.  
    max_cols: The maximim number of columns in any row, likely 28.
    '''
    #create  generic column headers
    cols=["col"+str(i) for i in range(max_cols)]
    #concatenate path and filename
    src=os.path.join(src_dir,filename)
    #copy both files to the target directory
    if src_dir != tgt_dir and tgt_dir!=None and tgt_dir!='':
        print('        copying raw file to working directory: ' + tgt_dir)
        tgt=os.path.join(tgt_dir,filename)
        shutil.copyfile(src, tgt) 
    else:
        tgt=src
    # return dataframe    
    print('        reading raw file into datafrme: ' + tgt_dir)
    lst = pd.read_csv(open(tgt), names=cols, dtype= str )
    return pd.DataFrame(lst)

def define_sections(df, end_of_section_pattern=end_of_section_pattern):
    sections = []
    first_row = 3
    for row_num, row in df.iterrows():
        if row[0][:4] == end_of_section_pattern:
            #section_name = row[0][3:].replace("END OF","").strip()
            section_name = row[0][11:]
            #sections [from line, to line, section name]
            sections += [[first_row, row_num, section_name]]
            first_row = row_num+1
    return sections

def parse_raw_header(first_3_rows):
    data = list(first_3_rows.iloc[0,:][0:7])+[None]
    data[7] = data[6]
    data[5] = data[5].split('/')[1][-4].strip()
    data[5] = data[5].split('/')[0].strip()
    data += [first_3_rows.iloc[1,:][0]]
    data += [first_3_rows.iloc[2,:][0] + ',' + first_3_rows.iloc[2,:][1]]
    for i in range(len(data)):
        first_3_rows.iloc[0,i]=data[i]
    data=[item.strip(' ') for item in data]
    data[6]=parser.parse(data[6])
    data[7]=parser.parse(data[7])
    cols = ['col0','col1','col2','col3','col4','col5','Updated','Updated2',\
            'Case_Name','Updated3']    
    dtype_dict = {'col0':'float','col1':'float','col2':'float','col3':'float',\
                  'col4':'float','col5':'str','Updated':'str','Updated2':'str',\
                  'Case_Name':'str','Updated3':'str'}
    df = pd.DataFrame([data])
    #print('raw summary:')
    #print(df)
    df.columns = cols
    df.dtype = dtype_dict
    return df

def append_owner(df, owner_df):
    ''' Add Bus_Name columns to a Branch dataframe.
        Branch1/2 only has bus numbers.  Look up Bus_Name in the 
        Bus1 or Bus2 dataframe and apply
    '''
    ret = pd.merge(df, owner_df, left_on="Owner", right_on="Owner_Num", how="inner")
    ret.drop('Owner_Num', axis=1, inplace=True)
    return ret


def append_bus_info_to_branch(branch_df, bus_df):
    ''' Add Bus_Name columns to a Branch dataframe.
        Branch1/2 only has bus numbers.  Look up Bus_Name in the 
        Bus1 or Bus2 dataframe and apply
    '''
    bus_slim = bus_df.loc[:,['Bus_Num', 'Bus_Name']].copy()
    # FROM bus
    ret = pd.merge(branch_df, bus_slim, left_on="Fr_Bus_Num", right_on="Bus_Num", how="inner")
    ret = ret.rename(columns = {'Bus_Name':'Fr_Bus_Name'})
    ret.drop('Bus_Num', axis=1, inplace=True)
    # TO bus
    ret = pd.merge(ret, bus_slim, left_on="To_Bus_Num", right_on="Bus_Num", how="inner")
    ret = ret.rename(columns = {'Bus_Name':'To_Bus_Name'})
    ret.drop('Bus_Num', axis=1, inplace=True)
    ret = ret[ret['Fr_Bus_Num'].notnull()]
    return ret

def branch_df_compare(branch_df1, branch_df2):
    '''
    branch_cols=['Fr_Bus_Num','To_Bus_Num','ID','Line_R_pu',\
                 'Line_X_pu','Charging_pu','Rate_A_MVA',\
                 'Rate_B_MVA','Rate_C_MVA','Line_G_From_pu',\
                 'Line_B_From_pu','Line_G_To_pu','Line_B_To_pu',\
                 'In_Service','Code','Length','Owner',\
                 'Fraction']
    '''

    # dropped branch
    ret = pd.merge(branch_df1, branch_df2, how='left', on=['Fr_Bus_Num','To_Bus_Num'])
    ret['change_type'] = 'dropped branch (RateA)'
    ret['change_amt']=-ret['Rate_A_MVA_x']
    ret = ret[(ret['Rate_A_MVA_x'].notnull()) & (ret['Rate_A_MVA_y'].isnull())] 
    print('Dropped branch')
    ret['change_type'] = 'dropped branch (RateA)'
    ret['change_amt']=-ret['Rate_A_MVA_x']
    print(ret.loc[:,['Fr_Bus_Num','To_Bus_Num','Rate_A_MVA_x','change_type','change_amt']].head())
    # added
    added = pd.merge(branch_df1, branch_df2, how='right', on=['Fr_Bus_Num','To_Bus_Num'])
    added = added[(added['Rate_A_MVA_x'].isnull()) & (added['Rate_A_MVA_y'].notnull())] 
    added['change_type'] = 'added branch (RateA)'
    added['change_amt']=added['Rate_A_MVA_y']
    print('Added branch')
    print(added.loc[:,['Fr_Bus_Num','To_Bus_Num','Rate_A_MVA_y','change_type','change_amt']].head())
    ret = ret.append(added)
    added=None

    # changes in Rate_A
    delta = pd.merge(branch_df1, branch_df2, how='inner', on=['Fr_Bus_Num','To_Bus_Num'])
    delta = delta[delta['Rate_A_MVA_x'] != delta['Rate_A_MVA_y']]
    delta['change_type'] = 'delta branch RateA'
    delta['change_amt']=delta['Rate_A_MVA_x']-delta['Rate_A_MVA_y']
    print('Delta Rate_A')
    print(delta.loc[:,['Fr_Bus_Num','To_Bus_Num','Rate_A_MVA_x','Rate_A_MVA_y','change_type','change_amt']].head())
    print(delta.head())
    ret = ret.append(delta)
    delta=None
   
    return ret


def append_bus_info_to_gen(gen_df, bus_df):
    bus_slim = bus_df.loc[:,['Bus_Num', 'Bus_Name', 'Bus_kV','Area_Num','Zone_Num']].copy()
    bus_slim = bus_slim.rename(columns = {'Bus_Num':'Bus_Num2'})
    print("bus_slim.columns")
    print(bus_slim.columns)
    print("gen_df.columns")
    print(gen_df.columns)
    ret = pd.merge(gen_df, bus_slim, left_on="Bus_Num", right_on="Bus_Num2", how="inner")
    ret.drop('Bus_Num2', axis=1, inplace=True)
    ret = ret[ret['Bus_Num'].notnull()]
    return ret
    
def gen_df_compare(gen_df1, gen_df2, area_list=compare_owner_list):
    '''
    Compares the generation data from the two raw files.
    Parameters:
        gen_df1: dataframe containing the generation table from raw file1
        gen_df2: dataframe containing the generation table from raw file2
        cols: list of column names
    Returns dataframe with dropped gen, added gen and changes in Pgen, Pmax,
        Qgen, Qmax, In_Service.
        
    gen_cols=['Bus_Num', 'ID', 'Pgen', 'Qgen', 'Qmax', 'Qmin', 'VSched_pu',\
          'Remote_Bus_Num','Mbase', 'R_source_pu', 'X_source_pu',\
          'RTran_pu', 'XTran_pu','Gentap_pu', 'In_Service', 'RMPCT','Pmax',\
          'Pmin','Owner','Owner_Fraction']
    '''
    # dropped gen
    ret = pd.merge(gen_df1, gen_df2, how='left', on=['Bus_Num','ID'])
    ret = ret[(ret['Pgen_x'].notnull()) & (ret['Pgen_y'].isnull())] #I picked Pgen arbitrarily.
    print('Dropped gen')
    ret['change_type'] = 'dropped gen (Pgen)'
    ret['change_amt']=-ret['Pgen_x']
    #ret.insert(3, 'change_type', 'dropped gen (Pgen)')
    #ret.insert(3, 'change_amt', 'Pgen_x')
    print(ret.loc[:,['Bus_Num','ID','Pgen_x','change_type','change_amt']].head())
    # added
    added = pd.merge(gen_df1, gen_df2, how='right', on=['Bus_Num','ID'])
    added = added[(added['Pgen_x'].isnull()) & (added['Pgen_y'].notnull())] #I picked Pgen arbitrarily.
    added['change_type'] = 'added gen (Pgen)'
    added['change_amt']=added['Pgen_y']
    print('Added gen')
    print(added.loc[:,['Bus_Num','ID','Pgen_y','change_type','change_amt']].head())
    ret = ret.append(added)
    added=None

    # changes in Pgen
    delta = pd.merge(gen_df1, gen_df2, how='inner', on=['Bus_Num','ID'])
    delta = delta[delta['Pgen_x'] != delta['Pgen_y']]
    delta['change_type'] = 'delta gen Pgen'
    delta['change_amt']=delta['Pgen_x']-delta['Pgen_y']
    print('Delta Pgen')
    print(delta.loc[:,['Bus_Num','ID','Pgen_x','Pgen_y','change_type','change_amt']].head())
    print(delta.head())
    ret = ret.append(delta)
    delta=None
   
    return ret


########################################################################
#            Column Definitions               #
########################################################################
# Define the columns in each section
bus_dtype={'Bus_Num':'int', 'Bus_Name':'str', 'Bus_kV':'float', 'Code':'int', \
           'Area_Num':'int', 'Zone_Num':'int', \
           'Owner_Num':'int','Voltage_pu':'float','Angle':'float'}
bus_cols=['Bus_Num', 'Bus_Name', 'Bus_kV', 'Code', 'Area_Num', 'Zone_Num', \
          'Owner_Num','Voltage_pu','Angle']
load_dtype={'Bus_Num':'int','I_P_RC':'str','Code':'int','Area':'int','Zone':'int',\
           'P':'float','Q':'float','float1':'float','float1':'float',\
           'float3':'float','float4':'float','Owner':'int','In_Service':'int'}
fixed_shunt_dtype={'Bus_Num':'int', 'ID':'str','In_Service':'int',\
                  'float1':'float', 'float2':'float'}
gen_dtype={'Bus_Num':'int', 'ID':'str', 'Pgen':'float', 'Qgen':'float', \
          'Qmax':'float', 'Qmin':'float', 'VSched_pu':'float',\
          'Remote_Bus_Num':'int','Mbase':'float', \
          'R_source_pu':'float', 'X_source_pu':'float',\
          'RTran_pu':'float', 'XTran_pu':'float','Gentap_pu':'float', \
          'In_Service':'int', 'RMPCT':'float','Pmax':'float',\
          'Pmin':'float','Owner':'int','Owner_Fraction':'float'}
branch_dtype={'Fr_Bus_Num':'int','To_Bus_Num':'int','ID':'str','Line_R_pu':'float',\
             'Line_X_pu':'float','Charging_pu':'float','Rate_A_MVA':'float',\
             'Rate_B_MVA':'float','Rate_C_MVA':'float','Line_G_From_pu':'float',\
             'Line_B_From_pu':'float','Line_G_To_pu':'float','Line_B_To_pu':'float',\
             'In_Service':'int','Code':'int','Length':'float','Owner':'int',\
             'Fraction':'float'}
xfrmr1_dtype={'Fr_Bus_Num','To_Bus_Num',' Metered_on_Fr_End','ID','??',\
              'Winding1_on_Fr_End','AutoAdj','Magnetizing_G_pu',\
              'Magnetizing_B_pu','Xrmr_name','In_Service',\
              ' Owner1','Fraction_1','Owner_2','Fraction_2',\
              'Owner_3','Fraction_3','Owner_4','Fraction_4'}
xfrmr2_dtype={'Specified_R_pu':'float', 'Specified_X_pu':'float', 'Winding_MVA':'float'}
xfrmr3_dtype={'W1Ratio_pu':'float','W1NominalkV':'float','W1Angle_deg':'float',\
              'RateA_MVA':'float','Rate_B_MVA':'float','Rate_C_MVA':'float',\
              'CtrlMode':'float','CtrlBusNum':'float','R1_Max_deg':'float',\
              'R1_Min_deg':'float','V_max_MW':'float','V_min_MW':'float',\
              'Tap_postition':'float','Impedence_Tbl':'float','Load_Drop_R_pu':'float',\
              'Load_Drop_X_pu':'float','Unk':'float'}
xfrmr4_dtype={'Winding2Ratio_pu':'float', 'Winding2Nominal_kV':'float'}
area_dtype={'Area_Num':'int', 'Gen':'float', 'Ld':'float', \
            'float3':'float', 'Area_Name':'str'}
two_term_dc_dtype={}
vsc_dc1_dtype={"Name":'str','Int1':'int','float1':'float', \
               'float2':'float', 'float3':'float'}
vsc_dc2_dtype={'Bus_Num':'int','Terminal':'int','Int1':'int','float1':'float', \
               'pu':'float','MVA1':'float','float2':'float', 'float3':'float', \
               'float4':'float', 'MVA2':'float', 'float5':'float', 'float6':'float', \
               'float7':'float',"Bus_Num":'int',  'float8':'float'}
vsc_dc3_dtype=vsc_dc2_dtype
imped_correction_dtype={'Index':'int', 'float1':'float', 'float2':'float', \
                        'float3':'float', 'float4':'float', 'float5':'float', \
                        'float6':'float', 'float7':'float', 'float8':'float', \
                        'float9':'float', 'float10':'float',  'float11':'float',\
                        'float12':'float',   'float13':'float', 'float14':'float',  \
                        'float15':'float', 'float16':'float',  'float17':'float',\
                        'float18':'float',  'float19':'float', 'float20':'float',  \
                        'float21':'float', 'float22':'float'}  
multi_term_dc_dtype={'Fr_Bus_Num':'int','To_Bus_Num':'int','Amp1':'str',\
                     'Int1':'int','Bus3_Num':'int'}
multi_sctn_line_dtype={'Fr_Bus_Num':'int','To_Bus_Num':'int','Amp1':'str',\
                     'Int1':'int','Bus3_Num':'int'}
zone_dtype={'Zone_Num':'int','Zone_Name':'str'}
xfer_dtype={'unk':'float'}
owner_dtype={'Owner_Num':'int','Owner_Name':'str'}
facts_dtype={'Name':'float', 'Number':'float', 'int1':'float', 'int2':'float', \
            'X':'float', 'R':'float', 'pu':'float', 'col7':'float', \
            'col8':'float', 'col9':'float', 'col10':'float', \
            'col11':'float', 'col12':'float', 'col13':'float', \
            'col14':'float', 'col15':'float', 'col16':'float', \
            'col17':'float', 'col18':'float', 'col19':'float'}
sw_shunt_dtype={}
#gne_dtype={}


load_cols=['Bus_Num','I_P_RC','Code','Area','Zone',\
           'P','Q','float1','float1',\
           'float3','float4','Owner','In_Service']
fixed_shunt_cols=['Bus_Num', 'ID','In_Service',\
                  'float1', 'float2']
gen_cols=['Bus_Num', 'ID', 'Pgen', 'Qgen', \
          'Qmax', 'Qmin', 'VSched_pu',\
          'Remote_Bus_Num','Mbase', \
          'R_source_pu', 'X_source_pu',\
          'RTran_pu', 'XTran_pu','Gentap_pu', \
          'In_Service', 'RMPCT','Pmax',\
          'Pmin','Owner','Owner_Fraction']
branch_cols=['Fr_Bus_Num','To_Bus_Num','ID','Line_R_pu',\
             'Line_X_pu','Charging_pu','Rate_A_MVA',\
             'Rate_B_MVA','Rate_C_MVA','Line_G_From_pu',\
             'Line_B_From_pu','Line_G_To_pu','Line_B_To_pu',\
             'In_Service','Code','Length','Owner',\
             'Fraction']
xfrmr1_cols=['From_Bus_Num','To_Bus_Num','Fr_Bus_Num',\
             'l1c2','To_Bus_Num','ID','l1c4',\
             'l1c5','l1c6','R_pu','X_pu',\
             'l1c9','Name','In-Service',\
             'Owner','Fraction']
xfrmr2_cols=['l2c0', 'l2c1', 'l2c2']
xfrmr3_cols=['Fr_kV','To_kV','l3c2',\
              'Rate_A_MVA','Rate_B_MVA','Rate_C_MVA',\
              'G Fr pu','B Fr pu','Fr_kV2',\
              'To_kV2','l3c10','l3c11',\
              'l3c12','l3c13','B_To_pu',\
              'G_To_pu','l3c16']
xfrmr4_cols=['l4c0', 'l4c1']
area_cols=['Area_Num', 'Gen', 'Ld', \
            'float3', 'Area_Name']
two_term_dc_cols=[]
vsc_dc1_cols=["Name",'Int1','float1', \
               'float2', 'float3']
vsc_dc2_cols=['Bus_Num','Terminal','Int1','float1', \
               'pu','MVA1','float2', 'float3', \
               'float4', 'MVA2', 'float5', 'float6', \
               'float7',"Bus_Num",  'float8']
vsc_dc3_cols=vsc_dc2_cols
imped_correction_cols=['Index', 'float1', 'float2', \
                        'float3', 'float4', 'float5', \
                        'float6', 'float7', 'float8', \
                        'float9', 'float10',  'float11',\
                        'float12',   'float13', 'float14',  \
                        'float15', 'float16',  'float17',\
                        'float18',  'float19', 'float20',  \
                        'float21', 'float22']  
multi_term_dc_cols=['Fr_Bus_Num','To_Bus_Num','Amp1',\
                     'Int1','Bus3_Num']
multi_sctn_line_cols=['Fr_Bus_Num','To_Bus_Num','Amp1',\
                     'Int1','Bus3_Num']
zone_cols=['Zone_Num','Zone_Name']
xfer_cols=['unk']
owner_cols=['Owner_Num','Owner_Name']
facts_cols=['Name', 'Number', 'int1', 'int2', \
            'X', 'R', 'pu', 'col7', \
            'col8', 'col9', 'col10', \
            'col11', 'col12', 'col13', \
            'col14', 'col15', 'col16', \
            'col17', 'col18', 'col19']
sw_shunt_cols=[]
#gne_cols={}


########################################################################
#                   Main                      #
########################################################################

start=datetime.now()

print('')
print('Starting raw file comparison script')

datestr = str(datetime.now()).replace(' ','_').replace(':','').replace('.','')[:17]

if max_cols < 1:
    max_cols = max_col_cnt(os.path.join(tgt_dir,raw_file1))
    max_cols2 = max_col_cnt(os.path.join(tgt_dir,raw_file2))
    if max_cols2 > max_cols: 
        max_cols = max_cols2
    print('Max column count: ' + str(max_cols))

print('')
print('1. Parsing raw file 1: ' + raw_file1)
# load dataframes
print('    loading raw file')
df1 = raw_to_df(src_dir, tgt_dir, raw_file1, max_cols)
raw1_summary = parse_raw_header(df1[:3])
#print('        raw1 summary')
#print(raw1_summary)

df1['data_type']='na'

# Find sections within the dataframe
section_def1 = define_sections(df1)
#print('    raw file sections')
#print(section_def1)
# create section dataframes
print('    splitting raw file sections')
print
for i, sublist in enumerate(section_def1):
    #print("\n"+str(sublist[2])+": " )
    if 'BUS DATA' in sublist[2].upper():
        bus1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:9]
        df1[sublist[0]:sublist[1]]['data_type']='bus'
        bus1.columns = bus_cols #[s+'1' for s in bus_cols]
        for key in bus_dtype:
            bus1[key]=bus1[key].astype(bus_dtype[key])
    elif 'LOAD DATA' in sublist[2].upper():
        load1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:13]
        df1[sublist[0]:sublist[1]]['data_type']='load'
    elif 'FIXED SHUNT DATA' in sublist[2].upper():
        fixed_shunt1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:13]
        df1[sublist[0]:sublist[1]]['data_type']='fixed_shunt'
    elif 'GENERATOR DATA' in sublist[2].upper():
        gen1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:20]
        df1[sublist[0]:sublist[1]]['data_type']='gen'
        gen1.columns = gen_cols #[s+'1' for s in gen_cols]
        for key in gen_dtype:
            gen1[key]=gen1[key].astype(gen_dtype[key])
    elif 'BRANCH DATA' in sublist[2].upper():
        branch1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:18]
        df1[sublist[0]:sublist[1]]['data_type']='bbranch'
        branch1.columns = branch_cols #[s+'1' for s in branch_cols]
        for key in branch_dtype:
            branch1[key]=branch1[key].astype(branch_dtype[key])
    elif 'TRANSFORMER DAT' in sublist[2].upper():
        xfrmr1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:17]
        df1[sublist[0]:sublist[1]]['data_type']='xfrmr'
    elif 'AREA DATA' in sublist[2].upper():
        area1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:5]
        df1[sublist[0]:sublist[1]]['data_type']='area'
    elif 'TWO-TERMINAL DC DATA' in sublist[2].upper():
        two_term_dc1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:17]
        df1[sublist[0]:sublist[1]]['data_type']='two_term_dc'
    elif 'VSC DC LINE DATA' in sublist[2].upper():
        vsc_dc1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:15]
        df1[sublist[0]:sublist[1]]['data_type']='vsc_dc'
    elif 'IMPEDANCE CORRECTION DATA' in sublist[2].upper():
        imped_correction1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:24]
        df1[sublist[0]:sublist[1]]['data_type']='imped_correction'
    elif 'MULTI-TERMINAL DC DATA' in sublist[2].upper():
        multi_term_dc1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:28]
        df1[sublist[0]:sublist[1]]['data_type']='multi_term_dc'
    elif 'MULTI-SECTION LINE DATA' in sublist[2].upper():
        multi_sctn_line1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:5]
        df1[sublist[0]:sublist[1]]['data_type']='multi_sctn_line'
    elif 'ZONE DATA' in sublist[2].upper():
        zone1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:2]
        df1[sublist[0]:sublist[1]]['data_type']='zone'
    elif 'INTER-AREA TRANSFER DATA' in sublist[2].upper():
        xfer1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:28]
        df1[sublist[0]:sublist[1]]['data_type']='xfer'
    elif 'OWNER DATA' in sublist[2].upper():
        owner1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:2]
        df1[sublist[0]:sublist[1]]['data_type']='owner'
        owner1.columns = owner_cols #[s+'1' for s in branch_cols]
        for key in owner_dtype:
            owner1[key]=owner1[key].astype(owner_dtype[key])
    elif 'FACTS DEVICE DATA' in sublist[2].upper():
        facts1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:23]
        df1[sublist[0]:sublist[1]]['data_type']='facts'
    elif 'SWITCHED SHUNT DATA' in sublist[2].upper():
        sw_shunt1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:25]
        df1[sublist[0]:sublist[1]]['data_type']='switched_shunt'
    #elif 'GNE DATA DATA' in sublist[2].upper():
    #    gne1 = df1[sublist[0]:sublist[1]].copy().iloc[:,0:28]
    #    df1[sublist[0]:sublist[1]]['data_type']='gne'
print('run time: ' + str(datetime.now()-start))
#create some room in memory
df1=None


print('')
print('2. Parsing raw file 2: ' + raw_file2)
print()
# load dataframes
print('    loading raw file')
df2 = raw_to_df(src_dir, tgt_dir, raw_file2, max_cols)
raw2_summary = parse_raw_header(df2[:3])
#print('        raw2 summary')
#print(raw2_summary)

df2['data_type']='na'

# Find sections within the dataframe
section_def2 = define_sections(df2)
#print('    raw file sections')
#print(section_def2)
# create section dataframes
print('    splitting raw file sections')
for i, sublist in enumerate(section_def2):
    #print("\n"+str(sublist[2])+": " )
    if 'BUS DATA' in sublist[2].upper():
        bus2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:9]
        df2[sublist[0]:sublist[1]]['data_type']='bus'
        bus2.columns = bus_cols #[s+'1' for s in bus_cols]
        for key in bus_dtype:
            bus2[key]=bus2[key].astype(bus_dtype[key])
    elif 'LOAD DATA' in sublist[2].upper():
        load2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:13]
        df2[sublist[0]:sublist[1]]['data_type']='load'
    elif 'FIXED SHUNT DATA' in sublist[2].upper():
        fixed_shunt2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:13]
        df2[sublist[0]:sublist[1]]['data_type']='fixed_shunt'
    elif 'GENERATOR DATA' in sublist[2].upper():
        gen2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:20]
        df2[sublist[0]:sublist[1]]['data_type']='gen'
        gen2.columns = gen_cols #[s+'2' for s in gen_cols]
        for key in gen_dtype:
            gen2[key]=gen2[key].astype(gen_dtype[key])
    elif 'BRANCH DATA' in sublist[2].upper():
        branch2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:18]
        df2[sublist[0]:sublist[1]]['data_type']='branch'
        branch2.columns = branch_cols #[s+'1' for s in branch_cols]
        for key in branch_dtype:
            branch2[key]=branch2[key].astype(branch_dtype[key])
    elif 'TRANSFORMER DAT' in sublist[2].upper():
        xfrmr2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:17]
        df2[sublist[0]:sublist[1]]['data_type']='xfrmr'
    elif 'AREA DATA' in sublist[2].upper():
        area2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:5]
        df2[sublist[0]:sublist[1]]['data_type']='area'
    elif 'TWO-TERMINAL DC DATA' in sublist[2].upper():
        two_term_dc2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:17]
        df2[sublist[0]:sublist[1]]['data_type']='two_term_dc'
    elif 'VSC DC LINE DATA' in sublist[2].upper():
        vsc_dc2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:15]
        df2[sublist[0]:sublist[1]]['data_type']='vsc_dc'
    elif 'IMPEDANCE CORRECTION DATA' in sublist[2].upper():
        imped_correction2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:24]
        df2[sublist[0]:sublist[1]]['data_type']='imped_correction'        
    elif 'MULTI-TERMINAL DC DATA' in sublist[2].upper():
        multi_term_dc2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:28]
        df2[sublist[0]:sublist[1]]['data_type']='multi_term_dc'        
    elif 'MULTI-SECTION LINE DATA' in sublist[2].upper():
        multi_sctn_line2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:5]
        df2[sublist[0]:sublist[1]]['data_type']='multi_sctn_line'        
    elif 'ZONE DATA' in sublist[2].upper():
        zone2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:2]
        df2[sublist[0]:sublist[1]]['data_type']='zone'        
    elif 'INTER-AREA TRANSFER DATA' in sublist[2].upper():
        xfer2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:28]
        df2[sublist[0]:sublist[1]]['data_type']='xfer'        
    elif 'OWNER DATA' in sublist[2].upper():
        owner2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:2]
        df2[sublist[0]:sublist[1]]['data_type']='owner'
        owner2.columns = owner_cols #[s+'1' for s in branch_cols]
        for key in owner_dtype:
            owner2[key]=owner2[key].astype(owner_dtype[key])
    elif 'FACTS DEVICE DATA' in sublist[2].upper():
        facts2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:23]
        df2[sublist[0]:sublist[1]]['data_type']='facts'        
    elif 'SWITCHED SHUNT DATA' in sublist[2].upper():
        sw_shunt2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:25]
        df2[sublist[0]:sublist[1]]['data_type']='sw_shunt'        
    #elif 'GNE DATA DATA' in sublist[2].upper():
    #    gne2 = df2[sublist[0]:sublist[1]].copy().iloc[:,0:28]
    #    df2[sublist[0]:sublist[1]]['data_type']='gne'        

#create some room in memory
df2=None
print('run time: ' + str(datetime.now()-start))
#Find model differences    

#

print('')
print('3. Filter and apply Owner (if compare_area_list is not empty')
# Filter branch list by owner/area if requested.  
if isinstance(compare_owner_list, list) and len(compare_owner_list)>0:
    owner1=owner1[owner1['Owner_Num'].isin(compare_owner_list)]
    owner2=owner2[owner2['Owner_Num'].isin(compare_owner_list)]
owner_df = pd.merge(owner1, owner2, how='outer', on=['Owner_Num','Owner_Name'])

if compare_owner_list != []:
    owner_df=owner_df[owner_df['Owner_Num'].isin(compare_owner_list)].copy()

#print("gen1.describe")
#print(gen1.describe)

gen1=append_owner(gen1,owner1)
gen2=append_owner(gen2,owner_df)
#print("gen1.describe after appending owners")
#print(gen1.describe)
branch1 = append_owner(branch1,owner_df)
branch2 = append_owner(branch2,owner_df)

print('')
print('4. Add bus names')
gen1 = append_bus_info_to_gen(gen1,bus1)
gen2 = append_bus_info_to_gen(gen2,bus2)
branch1 = append_bus_info_to_branch(branch1,bus1)
branch2 = append_bus_info_to_branch(branch2,bus2)

#Find model differences    
print('')
print('5. Compare models')
print('    Finding generation differences')

#  ******  Gen compaare ******
print('    Comparison of gen1:gen2')
gen_diff = gen_df_compare(gen1, gen2)
gen_diff.to_csv(os.path.join(tgt_dir,'gen_diff_' + datestr + '.csv'))
print('run time: ' + str(datetime.now()-start))

#  ******  Branch compaare ******
print('    Comparison of branch1:branch2')
branch_diff = branch_df_compare(branch1, branch2)
branch_diff.to_csv(os.path.join(tgt_dir,'branch_diff_' + datestr + '.csv'))
print('run time: ' + str(datetime.now()-start))

print('')
print('Finished raw file comparison script')
print('total run time: ' + str(datetime.now()-start))

