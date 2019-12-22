import ast
import math
import operator
from pymongo import MongoClient

comp_dict={}

f=open('sof_final_data_ir.txt',"r", encoding="utf8")
for each_line in f:
    each_line=each_line.strip()
    lin_list=each_line.split("$#@")
    i=0
    while(i<len(lin_list)-1):
        if(i==0):
            i=i+1
        elif(i==1):
            key_list=ast.literal_eval(lin_list[i])
            i=i+1
        else:
            if((int(''.join(lin_list[i+1].split(","))))==0):
                lin_list[i+1]='1'    
            tf_idf_computed_value=(int(''.join(lin_list[i+1].split(","))))*(1+math.log10(int(''.join(lin_list[i+2].split(",")))))*(math.log10(89545/int(''.join(lin_list[i+2].split(",")))))
            for ke in key_list:
                if ('.' not in ke):
                    if ke.lower() not in comp_dict.keys():
                        comp_dict[ke.lower()]={}
                        if('.' not in lin_list[i]):
                            comp_dict[ke.lower()][lin_list[i]]=tf_idf_computed_value
                    else:
                        if('.' not in lin_list[i]):
                            if lin_list[i] not in comp_dict[ke].keys(): 
                                comp_dict[ke][lin_list[i]]=tf_idf_computed_value
                            else:
                                comp_dict[ke][lin_list[i]]=comp_dict[ke][lin_list[i]]+tf_idf_computed_value
            i=i+3

f.close()

client=MongoClient()
db=client["irproject"]
collection=db["sofusers"]

for ke in comp_dict.keys():
    comp_dict[ke]=dict(sorted(comp_dict[ke].items(),key=operator.itemgetter(1)))
    collection.insert_one({"technology":ke,"users":comp_dict[ke]})

keys=[]
for ke in comp_dict.keys():
    keys.append(ke)

collection.insert_one({"keys_terms":"keys","k":keys})

