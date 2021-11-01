from bs4 import BeautifulSoup
import requests
import os.path
import json
import re
import pprint
def scrap_top_list():
    url="https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/"
    sample=requests.get(url)
    soup=BeautifulSoup(sample.text,"html.parser")
    main_div=soup.find_all("table",class_="table")
    movie_ranks=[]
    movie_names=[]
    no_of_Reviews=[]
    movie_urls=[]
    new_list=[]
    k=[]
    movie_ratings=[]
    year_of_realease=[]
    for tr in main_div:
        for i in tr.find_all('tr')[1:]:
            movie_rank = i.find("td", class_="bold").text
            movie_ranks.append(movie_rank)
            # print(movie_ranks)
            movie_name = i.find("a", class_="unstyled articleLink").text.strip()  
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
    return Top_Movies     
   
   
scrapped=(scrap_top_list())

def group_by_year(movies_data):
    if os.path.exists("year.json"):
        with open("years.json","r") as f:
	        read1=f.read()
	        data1=json.loads(read1)
        return(data1)
    years=[]
    for i in movies_data:
        year=i["year"]
        if year not in years:
            years.append(year)
    movie_dict={i:[]for i in years}
    for i in movies_data:
        year=i['year']
        for x in movie_dict:
            if str(x)==str(year):
                movie_dict[x].append(i)
    with open("years.json","w") as f:
        json.dump(movie_dict,f,indent=4)
    return movie_dict
print(group_by_year(scrapped))






























