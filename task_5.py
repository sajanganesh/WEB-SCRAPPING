

































































from bs4 import BeautifulSoup
import requests
import os.path
import re
import json
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
            movie_rank= i.find("td", class_="bold").text
            movie_ran=movie_rank[:0]+ movie_rank[:-1]
            movie_ranks.append(movie_ran)
            # print(movie_ranks)
            movie_name = i.find("a", class_="unstyled articleLink").text.strip()  
            movie_nam= movie_name[:0] +  movie_name[:-6] 
            movie_names.append(movie_nam)

            name=movie_name
            movie_name=re.split('(\d+)',name)
            year_of_realease.append(movie_name[-2])
            # print(year_of_realease)

            # names=movie_name[0]
            # namename=names.replace("(","")
            # movie_names.append(namename)
            # print(movie_names)

            movie_review= i.find("td",class_="right hidden-xs").get_text()
            no_of_Reviews.append(movie_review)
            # print(no_of_Reviews)

            movie_rating = i.find("span",class_="tMeterScore").get_text()
            movie_ratin=movie_rating[:0] + movie_rating[-5:]
            movie_ratings.append(movie_ratin)
            # print(movie_rating)

            url=i.find("a",class_="unstyled articleLink")['href']
            movie_url="https://www.rottentomatoes.com"+url
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
    with open("year.json","w") as f:
        json.dump(Top_Movies,f,indent=4)
    return Top_Movies     

scrapped=(scrap_top_list())



def scrap_movie_details(movie_url):
    final=[]
    # time_sleep=random.randint(1,3)
    for i in movie_url:
        id=i[33:]
        if os.path.exists(id+".json"):
                with open(id+".json","r") as file:
	                read=file.read()
	                data=json.loads(read)
                final.append(data)
        else:
            # time.sleep
            deatails_dic={}
            page=requests.get(i)
            soup=BeautifulSoup(page.text,'html.parser')
            title_div=soup.find("score-board",class_="scoreboard").h1.get_text()
            # print(title_div)
            # sub_div=soup.find("div",class_="col mob col-center-right col-full-xs mop-main-column").p.get_text()
            # sub_div.split(",")
            # year,genre,time= sub_div.split(",")
            # director_name=soup.find("a",href="/celebrity/josh_cooley").get_text()
            # bio=soup.find("div", class_="movie_synopsis clamp clamp-6 js-clamp").get_text().strip()
            # image = soup.find_all('img', class_='posterImage js-lazyLoad')
            # for e in image:
                # link = e.get('data-src')

            f=soup.find("ul",class_='content-meta info')
            all=f.find_all("li",class_="meta-row clearfix")
            for s in all:
                deatails_dic[" ".join((s.find("div",class_="meta-label subtle").text).split())]=" ".join(((s.find("div",class_="meta-value")).text).split())
            # movie_language=all[2].find("div",class_="meta-value").get_text().strip()
            # gener=all.find_all("div",class_="meta-value").text.split()
            # "div",class="meta-label subtle"

            # p=dict(name=title_div,director=director_name,language=movie_language,poster_img_url=link,bio=bio,runtime=time,gener=gener,)
        with open(id+".json","w")as file:
	        json.dump(deatails_dic,file,indent=4)
        final.append(deatails_dic)
                # 
    return final
    # 
# url="https://www.rottentomatoes.com/m/toy_story_4"
# print(scrap_movie_details(url))

def get_movie_detail_list(movie_list):
    # print(movie_list[0])
    movie_detail_list=[]
    i=0
    while i<len(movie_list):
        list=movie_list[i]['url']
        movie_detail_list.append(list)
        # print(movie_detail_list)
        i=i+1
    return movie_detail_list
get_movie_detail_list(scrapped)
# print(type(scrapped))

url=get_movie_detail_list(scrapped)
pprint.pprint(scrap_movie_details(url[:10]))
























































