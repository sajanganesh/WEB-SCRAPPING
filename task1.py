from bs4 import BeautifulSoup
import requests
import os.path
import json
import re
import pprint
def scrap_top_list():
    if os.path.exists("movies.json"):
        with open("movies.json","r") as file:
	        read=file.read()
	        data=json.loads(read)
        return(data)
    url="https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/"
    sample=requests.get(url)
    soup=BeautifulSoup(sample.text,"html.parser")
    main_div=soup.find_all("table",class_="table")
    movie_ranks=[]
    movie_names=[]
    no_of_Reviews=[]
    movie_urls=[]
    movie_ratings=[]
    year_of_realease=[]
    for tr in main_div:
        for i in tr.find_all('tr')[1:]:
            movie_rank = i.find("td", class_="bold").text
            movie_ranks.append(movie_rank)
            # print(movie_ranks)
            movie_name = i.find("a", class_="unstyled articleLink").text.strip() 
            # print(movie_name) 
            name=movie_name
            movie_name=re.split('(\d+)',name)
            year_of_realease.append(movie_name[-2])
            # print(year_of_realease)

            names=movie_name[0]
            namename=names.replace("(","")
            movie_names.append(namename)
            # print(movie_names)
            
            movie_review= i.find("td",class_="right hidden-xs").get_text()
            no_of_Reviews.append(movie_review)
            # print(no_of_Reviews)

            movie_rating = i.find("span",class_="tMeterScore").get_text()
            movie_ratings.append(movie_rating)
            # print(movie_rating)

            url=i.find("a",class_="unstyled articleLink")['href']
            movie_url="https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/"+url
            movie_urls.append(movie_url)
            # print(movie_url)
    
    Top_Movies=[]
    details={'position':'','Rating':'','Name':'','year':"",'url':'','movie_Reviews':''}
    for i in range(0,len(movie_ranks)):
        details['position']=str(movie_ranks[i])
        details['Rating']=str(movie_ratings[i])
        details['Name']=str(movie_names[i])
        details['year']=str(year_of_realease[i])
        details['url']=movie_urls[i]
        details['movie_Reviews']=str(no_of_Reviews[i])
        Top_Movies.append(details.copy())
    with open("movies.json","w")as file:
	    data=json.dump(Top_Movies,file,indent=4)
    return Top_Movies     
   
   
pprint.pprint(scrap_top_list())




