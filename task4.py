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
def scrap_movie_details(movie_url):
    if os.path.exists("movie_details.json"):
        with open("movie_details.json","r") as file:
	        read=file.read()
	        data=json.loads(read)
        return(data)
    page=requests.get(movie_url)
    soup=BeautifulSoup(page.text,'html.parser')
    title_div=soup.find("div",class_="col mob col-center-right col-full-xs mop-main-column").h1.get_text()
    sub_div=soup.find("div",class_="col mob col-center-right col-full-xs mop-main-column").p.get_text()
    sub_div.split(",")
    year,genre,time= sub_div.split(",")
    director_name=soup.find("a",href="/celebrity/josh_cooley").get_text()
    bio=soup.find("div", class_="movie_synopsis clamp clamp-6 js-clamp").get_text().strip()
    image = soup.find_all('img', class_='posterImage js-lazyLoad')
    for e in image:
        link = e.get('data-src')

    f=soup.find("ul",class_='content-meta info')
    all=f.find_all("li",class_="meta-row clearfix")
    movie_language=all[2].find("div",class_="meta-value").get_text().strip()
    gener=all[1].find("div",class_="meta-value").text.split()

    p=dict(name=title_div,director=director_name,language=movie_language,poster_img_url=link,bio=bio,runtime=time,gener=gener,)
    with open("movie_details.json","w")as file:
	    data=json.dump(p,file,indent=4)
    
    return p
    
url="https://www.rottentomatoes.com/m/toy_story_4"
scrap_movie_details(url)



















