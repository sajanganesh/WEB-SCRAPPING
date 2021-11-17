from bs4 import BeautifulSoup
import requests
import os.path
import json
import pprint
def scrap_top_list():
    if os.path.exists("pickle_data.json"):
        with open("pickle_data.json","r") as file:
	        read=file.read()
	        data=json.loads(read)
        return(data)
    url="https://paytmmall.com/shop/search?q=pickles&from=organic&child_site_id=6&site_id=2&category=101471"
    sample=requests.get(url)
    soup=BeautifulSoup(sample.text,"html.parser")
    main_div=soup.find("div",class_="_3RA-")
    main=main_div.find_all("div",class_="_1fje")
    pickle_name=[]
    pickle_price=[]
    pickle_url=[]
    pickle_img=[]
    count=0
    position_c=[]
    for div in main:
        all=div.find_all("div",class_="_2i1r")
        for i in all:
            pickle=i.find("div",class_="_2PhD").text
            pickle_name.append(pickle)
            pickle_p=i.find("div",class_="_1kMS").text
            pickle_price.append(pickle_p)
            link=i.find("a",class_="_8vVO")['href']
            pickle_u="https://paytmmall.com"+link
            pickle_url.append(pickle_u)
            image=i.find("div",class_="_3nWP")
            for i in image:
                pickle_img.append(i['src'])
            count=count+1
            position_c.append(count)
    Top_list=[]
    details={'position':'','Name':'','price':'','url':'','image':''}
    for i in range(0,len(pickle_name)):
        details['position']=str(position_c[i])
        details['Name']=str(pickle_name[i])
        details['price']=str(pickle_price[i])
        details['url']=pickle_url[i]
        details['image']=pickle_img[i]
        Top_list.append(details.copy())
    pprint.pprint(Top_list)   
    with open("pickle_data.json","w")as file:
	    data=json.dump(Top_list,file,indent=4)
    pprint.pprint(Top_list)
scrap_top_list()
