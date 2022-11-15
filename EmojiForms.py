import subprocess
import sys
from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
import base64

class EmojiForms(object):

    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install",'-r', package])

    def __init__(self,url,pre_csv=False):
        self.url = url
        self.pre_csv = pre_csv
        #self.install("requirments.txt")
        


    def get_emojis_and_unicode(self):
        base_url = self.url
        response = requests.get(base_url)
        soup = bs(response.content,'html.parser')
        rev_table = soup.findAll("td",attrs={"class","chars"})
        Skin_emojis_ls = []
        Skin_unicode_ls = []
        Skin_hex_ls = []
        for i in range(len(rev_table)):
            txt = rev_table[i].getText()
            #print(txt.encode('unicode_escape'))
            Skin_unicode_ls.append(txt.encode('unicode_escape'))
            Skin_emojis_ls.append(txt)
            Skin_hex_ls.append(txt.encode())
        Emojis = {
            'Emoji' : Skin_emojis_ls,
            'Unicode' : Skin_unicode_ls,
            "Hex" : Skin_hex_ls,
        }
        df = pd.DataFrame(Emojis)
        return df
    
    def Get_Make_Files(self,parent):
        parent = parent
        if not (os.path.exists(parent)):
            os.mkdir(parent)
        base_url = self.url
        response = requests.get(base_url)
        soup = bs(response.content,'html.parser')
        rev_table = soup.findAll("th",attrs={'class','cchars'})
        list_filename = []
        for i in rev_table:
            name = i.getText()
            if  name not in list_filename and name != "Browser":
                list_filename.append(name)
                path =os.path.join(parent,name)
                if not (os.path.exists(path)):
                    os.mkdir(path)
        return list_filename
    
    def Download_Emojis(self,parent):
        list_filename = self.Get_Make_Files(parent)
        response = requests.get(self.url)
        soup = bs(response.content,'html.parser')
        body = soup.find_all("tr")
        ls =[x[0] for x in os.walk("SkinData")]
        for i in body[3:-1]:
            #td =body[3].select("img")
            file_name = i.select("a")[0].getText()
            #print(file_name)
            imgs = i.select("img")
            directories = ls[1:len(imgs)+1]
            for id in range(len(imgs)):
                head,data = imgs[id]["src"].split(",")
                file_ext = head.split(';')[0].split('/')[1]
                filename = os.path.join(directories[id],file_name + '.' + file_ext)
                data = base64.b64decode(data)
                with open(filename, 'wb') as f:
                    f.write(data)