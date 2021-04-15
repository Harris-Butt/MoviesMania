from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
# Create your views here.


def index(request):
    if request.is_ajax():
        loaded_movies = get_more_movies('https://www.movies2.com.pk',request.session.get("current_page"))
        #                                                                                                                                                                                                                                                                                                                                                                                                                                                             request.session.get('movies_data').update(loaded_movies)
        context = {
            'images_titles_and_links': loaded_movies,
        }
        request.session["current_page"] = (request.session.get("current_page")+1)
        return render(request, 'temo.html', context)
    if  'movies_data' in request.session:
        request.session["current_page"] = 1
        context = {
            'images_titles_and_links': request.session.get("movies_data"),
        }
        return render(request, 'index.html', context)
    print('movie_data' in request.session)
    images_titles_and_links = {}
    session = setup_connection()
    html_content = session.get(f"https://www.movies2.com.pk/").text
    soup = BeautifulSoup(html_content, 'html.parser')
    current_page = get_current_page_number(soup)
    request.session['current_page']= int(current_page)
    print(current_page)
    post_boxs = soup.find_all('div', attrs={'class': 'boxtitle'})
    for post_box in post_boxs:
        children = post_box.find('a',attrs={'class':'thumnail-imagee'})
        image = post_box.find('img')
        images_titles_and_links[children["title"]]=[image["src"],children["href"]]

    #request.session["movies_data"] = images_titles_and_links

    context = {
        'images_titles_and_links': images_titles_and_links,
        #'images_titles_and_links': request.session.get("movies_data"),

    }
    context["hidden"] = "hidden"
    if is_navigation_tag(soup) and is_nextpage(soup):

        context["hidden"] = ""


    return render(request, 'base.html', context)


def page1(request):
    if request.is_ajax():
        name = request.session.get('movie_name')
        movie_name = name.replace(" ", "+")
        loaded_movies = get_more_movies('https://www.movies2.com.pk/',request.session.get("current_page"),movie_name)
        context = {
            'images_titles_and_links': loaded_movies,
        }
        request.session["current_page"] = (request.session.get("current_page") + 1)
        return render(request, 'temo.html', context)
    images_titles_and_links = {}
    name = request.POST.get("movie_name")
    if name is None:
        name = request.session.get('movie_name')
    else:
        request.session['movie_name'] = name
    movie_name = name.replace(" ", "+")
    session = setup_connection()
    html_content = session.get(f"https://www.movies2.com.pk/?s={movie_name}").text
    soup = BeautifulSoup(html_content,'html.parser')
    if is_navigation_tag(soup):
        current_page = get_current_page_number(soup)
        request.session['current_page'] = int(current_page)
    print(soup.title.string)
    post_boxs = soup.find_all('div',attrs={'class':'boxtitle'})
    for post_box in post_boxs:
        children = post_box.find('a',attrs={'class':'thumnail-imagee'})
        print(children["href"])
        print(children["title"])
        image = post_box.find('img')
        print(image["src"])
        images_titles_and_links[children["title"]] = [image["src"], children["href"]]
    context = {
        'images_titles_and_links': images_titles_and_links,
    }
    context["hidden"] = "hidden"
    if is_navigation_tag(soup) and is_nextpage(soup):
        context["hidden"] = ""

    return render(request,'page1.html',context)


def is_navigation_tag(soup):
    nav_tag = soup.find('div',attrs={'class':'wp-pagenavi'})
    if nav_tag:
        return True
    return False
def is_nextpage(soup):
    next_page = soup.find('a', {'class': 'page larger'})
    if next_page:
        return True
    return False

def get_navigation_tag(soup):
    return soup.find('div',attrs={'class':'wp-pagenavi'})

def check_last_button(soup,tag):
    last = soup.tag.find('div', attrs={'class':'nextpostslink'})
    if last:
        return True
    return False

def setup_connection():
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    return session

def get_current_page_number(soup):
    navigation_tag = get_navigation_tag(soup)
    current_page = navigation_tag.find('span',attrs={'class','current'}).text
    return current_page

def get_more_movies(url,current_page,movie_name=None,category=None):
    images_titles_and_links = {}
    session = setup_connection()
    if movie_name is not None:
         site = str(url)+'/'+'page'+'/'+str(current_page)+'/?s='+str(movie_name)
    elif category is not None:
        site = str(url)+'/'+'category'+'/'+str(category)+'/'+'page'+'/'+str(current_page)
    else:
        site = str(url)+'/'+'page'+'/'+str(current_page)
    html_content  = session.get(site).text
    soup = BeautifulSoup(html_content, 'html.parser')
    if is_nextpage(soup):
        if movie_name is not None:
            html_content = session.get(f"{url}/page/{str(current_page + 1)}/?s={movie_name}").text

        elif category is not None:
            html_content = session.get(f"{url}/category/{category}/page/{str(current_page + 1)}").text
        else:
            html_content = session.get(f"{url}/page/{str(current_page + 1)}").text
        soup = BeautifulSoup(html_content, 'html.parser')
        post_boxs = soup.find_all('div', attrs={'class': 'boxtitle'})
        for post_box in post_boxs:
            children = post_box.find('a', attrs={'class': 'thumnail-imagee'})
            print(children["href"])
            print(children["title"])
            image = post_box.find('img')
            print(image["src"])
            images_titles_and_links[children["title"]] = [image["src"], children["href"]]
    return images_titles_and_links

def page2 (request):
    movie_links = []
    link = request.POST.get('link')
    name = request.POST.get('movie_name')
    if link is None:
        link = request.session.get('link')
        name = request.session.get('movie_name')
    else:
        request.session['link'] = link
        request.session['movie_name'] = name
    session = setup_connection()
    html_content = session.get(link).text
    soup = BeautifulSoup(html_content, 'html.parser')
    iframes = soup.find_all('iframe',attrs={'loading':'lazy'})
    for iframe in iframes:
        movie_links.append(iframe["src"])
    context = {
        'movie_links': movie_links,
        'movie_name':name
    }
    print(len(movie_links))
    return render(request, 'page2.html', context)

def by_category(request):
    if request.is_ajax():
        movie_category = request.session.get('movie_category')
        loaded_movies = get_more_movies('https://www.movies2.com.pk/',request.session.get("current_page"),category=movie_category)
        context = {
            'images_titles_and_links': loaded_movies,
        }
        request.session["current_page"] = (request.session.get("current_page") + 1)
        return render(request, 'temo.html', context)
    images_titles_and_links = {}
    movie_category = request.POST['category']
    if movie_category is None:
        movie_category = request.session.get['movie_category']
    else:
        request.session['movie_category'] = movie_category
    session = setup_connection()
    html_content = session.get(f"https://www.movies1.com.pk/category/{movie_category}").text
    soup = BeautifulSoup(html_content, 'html.parser')
    if is_navigation_tag(soup):
        current_page = get_current_page_number(soup)
        request.session['current_page'] = int(current_page)
    print(soup.title.string)
    post_boxs = soup.find_all('div',attrs={'class':'boxtitle'})
    for post_box in post_boxs:
        children = post_box.find('a',attrs={'class':'thumnail-imagee'})
        print(children["href"])
        print(children["title"])
        image = post_box.find('img')
        print(image["src"])
        images_titles_and_links[children["title"]] = [image["src"], children["href"]]
    context = {
        'images_titles_and_links': images_titles_and_links,
    }
    context["hidden"] = "hidden"
    if is_navigation_tag(soup) and is_nextpage(soup):
        context["hidden"] = ""

    return render(request,'category.html',context)