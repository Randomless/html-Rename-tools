import os
import re
from bs4 import BeautifulSoup as bs
from lxml import html
from html.parser import HTMLParser
import random
import pickle

cwd=os.getcwd()
print(cwd)
save_data="./save_data.pkl"

def Addchangedname(f_name,f_namelist):
    # 中文或外文有字符无法用utf-8编码时，使用ISO-8859-1
    with open(f_name,encoding='ISO-8859-1') as f:
        # bsObj = BeautifulSoup(f)
        # dateText=bsObj.find("EntryWriteDate")
        # print(dateText.get_text())
        f_text=f.read()  # IOstream to string
        tree = html.fromstring(f_text)
        name = tree.xpath("//span[@class='EntryWriteDate']") # 提取class
        title= tree.xpath("//title")       # 按名称提取属性
        if name:
            name1 = html.tostring(name[0]) # html变量转换为string
            title1 = html.tostring(title[0],encoding='ISO-8859-1') # title中有外文无法解析 故encoding
            name2 = HTMLParser().unescape(name1.decode())
            title2 = HTMLParser().unescape(title1.decode())
            title3 =title2[18:-9] # 按字符strip掉字符串变量前后的<title>...<title/>
            mat = re.search(r"(\d{4}/\d{1,2}/\d{1,2}\s\d{1,2}:\d{1,2})",name2) 
            #正则表达式提取时间 返回一个Match类型的对象
            time=mat.group() #match对象group
            year,month,day= time.split(sep="/")
            day1,second=day.split(sep=":")  # split(sep=)掉非法目录字符
            time1=year+month+day1+" "+second #重新生成所需的文件名string
            a=(f_name,time1,title3)
            f_namelist.append(a)
            #os.rename(f_name,newname)
        else:
            print(f," file have no class called EntryWriteDate")
        

f_namelist=[]

for dirpath,_,filenames in os.walk('./'):
    count=0
    for f in filenames:
        f_name = os.path.join(dirpath,f)
        #f_head,f_tial=os.path.split(f)
        if f_name.endswith(".htm"):
            Addchangedname(f,f_namelist)
            count+=1
print('htm files Count:',count)
print(f_namelist)
print(len(f_namelist))

with open(save_data,"wb") as f: # wb dump 存   rb load 读
    pickle.dump(f_namelist,f)

