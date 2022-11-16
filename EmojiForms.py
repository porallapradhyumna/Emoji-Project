"""
Created on Tue Nov 15 17:12:20 2022

@author: PorallaPradhyumna
"""

import subprocess
import sys
from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
import numpy as np
import base64
import re

class EmojiForms(object):

    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install",'-r', package])

    def __init__(self,pre_csv = False):
        #self.install("requirments.txt")
        self.pre_csv = pre_csv


    def get_emojis_and_unicode(self,url):
        """
        

        Parameters
        ----------
        url : Takes url of unicode.org site to get emojis.

        Returns
        -------
        df : Pandas Dataframe is Output Format.

        """
        base_url = url
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
    
    def Get_Make_Files(self,url,parent):
        """
        

        Parameters
        ----------
        url : Takes url of unicode.org site to get emojis.
        parent : The parent Directory where you want to save all type of emoji files.

        Returns
        -------
        list_filename : List of files created in Parent directory.

        """
        parent = parent
        if not (os.path.exists(parent)):
            os.mkdir(parent)
        base_url = url
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
    
    def Download_Emojis(self,url,parent):
        """
        
        Downlods all the emojis extracted from the url
        
        Parameters
        ----------
        url : Takes url of unicode.org site to get emojis.
        parent : The parent Directory where you want to save all type of emoji files.

        Returns
        -------
        None. 

        """
        list_filename = self.Get_Make_Files(url,parent)
        response = requests.get(url)
        soup = bs(response.content,'html.parser')
        body = soup.find_all("tr")
        ls =[x[0] for x in os.walk(parent)]
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

    def Extract_Emoji(self,Data_Frame):
        """
        

        Parameters
        ----------
        Data_Frame : Emojis are extracted from Pandas Data_Frame.

        Returns
        -------
        Dataframe with hex codes replaced with emojis.

        """
        Data_Frame = Data_Frame.replace(np.nan,"0")
        def find_emojis(text):
            data = text.split(" ")
            for content in data:
                if "\\x" in content:
                    
                    codes = re.findall(r'\\x[a-zA-Z0-9][a-zA-Z0-9]',content)
                    codes_str = ("").join(codes)
                    codes = codes_str.replace("\\x", "")
                    codes = bytes.fromhex(codes)
                    codes = codes.decode()
                    if(codes_str in content):
                        text = text.replace(codes_str,codes)        
            return text
        dit = {}
        for i in Data_Frame.columns:
            dit["data_"+i]= Data_Frame[i].apply(find_emojis)
        df =  pd.DataFrame(dit)
        return df
    
    def Count_Frequency_Emojis(self,Data_Frame):
        """
        

        Parameters
        ----------
        Data_Frame : Emojis are extracted from Pandas Data_Frame to Count them.

        Returns
        -------
        Data_frame of frequency of each emoji is used through out the file 

        """
        Data_Frame = Data_Frame.replace(np.nan,"0")
        def check_emojis(text):
            codes = re.findall(r'\\x[a-zA-Z0-9][a-zA-Z0-9]',text)
            codes = ("").join(codes)
            codes = codes.replace("\\x","")
            codes = bytes.fromhex(codes)
            codes = codes.decode()
            text = codes
            
            return text
        freq_dict ={}
        for i in Data_Frame.columns:
            freq_dict["row-"+i] = Data_Frame[i].apply(check_emojis)
        df =  pd.DataFrame(freq_dict)

        freq_dict = {}

        def count_emojis(text):
            #print(text)
            emoji_ls = [*text]
            #print(emoji_ls)
            for i in emoji_ls:
                if i not in freq_dict:
                    freq_dict[i] = 0
                freq_dict[i] = freq_dict[i] + 1
            return text
        for i in df.columns:
            #print(i)
            df[i].apply(count_emojis)
        count_emoji_df =  pd.DataFrame(freq_dict, index=[0])
        count_emoji_df = count_emoji_df.T

        return count_emoji_df