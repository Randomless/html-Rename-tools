import os
import random
import pickle
import logging

logging.basicConfig(level=logging.DEBUG,filename='logging.log')
logger = logging.getLogger(__name__)
 
logger.info('This is a log info for NAME.py')

save_data="./save_data.pkl"
f_namelist=[]

with open(save_data,"rb") as f:
    f_namelist=pickle.load(f)


for dirpath,_,filenames in os.walk('./'):
    for oldname,time,title in f_namelist:
        #if title:  
        newname=time+" "+title+".htm"
        if newname not in filenames: #防止重命名
            try:
                os.rename(oldname,newname)
            except Exception as e:
                print(e)
                logger.info(e)
                continue
                #print('rename dir fail\r\n')\
        elif newname in filenames:
            logger.info(newname," already exist")