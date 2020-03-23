from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models


GITHUB_SEARCH_URL = 'https://github.com/search?q={}'
GITHUB_MULTIPLE_PAGES_SEARCH_URL = 'https://github.com/search?'
GITHUB_REPO_URL ='https://github.com'

def homeView(request):
    return render(request, 'homeView.html')

def newSearch(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = GITHUB_SEARCH_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, features='html.parser')
    postListings = soup.find_all('li', {'class': 'repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source'})
    repoesQue = soup.find_all('div', {'class': 'd-flex flex-column flex-md-row flex-justify-between border-bottom pb-3 position-relative'})

    count = "";
    index = 0;
    for repo in repoesQue:
        count =repo.text
        break
    numberOfQues = count.split(' ')
    intNumberOfPages = int(int(numberOfQues[4].replace(',',''))/10)

    finalData = []
    for i in range(0,intNumberOfPages):
        UrlWithPages = GITHUB_MULTIPLE_PAGES_SEARCH_URL + str(i).format((quote_plus(search)))
        response = requests.get(final_url)
        data = response.text

        soup = BeautifulSoup(data, features='html.parser')
#

        postListings = soup.find_all('li', {'class': 'repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source'})
        repoesQue = soup.find_all('div', {'class': 'd-flex flex-column flex-md-row flex-justify-between border-bottom pb-3 position-relative'})

        for post in postListings:
            url = GITHUB_REPO_URL+post.find('a').get('href')
            username = post.find('a').get('href')[1:].split('/')[0]
            repositoryName = post.find('a').get('href')[1:].split('/')[1]
            description = post.find(class_ = 'mb-1').text
            tag = post.find_all('a',{'class':'topic-tag topic-tag-link f6 px-2 mx-0'})
            link = post.find_all()
            tagList=""
            for tags in tag:
                tagList+=tags.text+','

            starsQueyy = post.find_all('a',{'class':'muted-link'})
            watchers=""
            for fot in starsQueyy:
                watchers = fot.text

            languageQuery = post.find_all('span',{'itemprop':'programmingLanguage'})
            for lan in languageQuery:
                programmingLanguage = lan.text

            finalData.append((username,repositoryName,description,tagList,watchers,programmingLanguage,url))

        if i==10:
            break

    stuffForFronted = {
        'search': search,
        'finalData': finalData,
    }
    return render(request, 'myapp/newSearch.html', stuffForFronted)

def detailedSearchView(request):
    return render(request, 'myapp/detailedSearch.html')

def detailedSearch(request):
    search = request.POST.get('actualSearch')
    selectedProgrammingLanguage = request.POST.get('dropDown')
    final_url = GITHUB_SEARCH_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, features='html.parser')
    postListings = soup.find_all('li',{'class': 'repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source'})
    repoesQue = soup.find_all('div', {
        'class': 'd-flex flex-column flex-md-row flex-justify-between border-bottom pb-3 position-relative'})

    count = "";
    index = 0;
    for repo in repoesQue:
        count = repo.text
        break
    numberOfQues = count.split(' ')
    intNumberOfPages = int(int(numberOfQues[4].replace(',', '')) / 10)

    finalData = []
    for i in range(0, intNumberOfPages):
        UrlWithPages = GITHUB_MULTIPLE_PAGES_SEARCH_URL + str(i).format((quote_plus(search)))
        response = requests.get(final_url)
        data = response.text

        soup = BeautifulSoup(data, features='html.parser')
        #

        postListings = soup.find_all('li', {
            'class': 'repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source'})
        repoesQue = soup.find_all('div', {
            'class': 'd-flex flex-column flex-md-row flex-justify-between border-bottom pb-3 position-relative'})

        for post in postListings:
            url = GITHUB_REPO_URL + post.find('a').get('href')
            username = post.find('a').get('href')[1:].split('/')[0]
            repositoryName = post.find('a').get('href')[1:].split('/')[1]
            description = post.find(class_='mb-1').text
            tag = post.find_all('a', {'class': 'topic-tag topic-tag-link f6 px-2 mx-0'})
            link = post.find_all()
            tagList = ""
            for tags in tag:
                tagList += tags.text + ','

            starsQueyy = post.find_all('a', {'class': 'muted-link'})
            watchers = ""
            for fot in starsQueyy:
                watchers = fot.text

            languageQuery = post.find_all('span', {'itemprop': 'programmingLanguage'})
            for lan in languageQuery:
                programmingLanguage = lan.text
            if (programmingLanguage  ==selectedProgrammingLanguage):
                finalData.append((username, repositoryName, description, tagList, watchers, programmingLanguage, url))

        if i == 10:
            break

    stuffForFronted = {
        'search': search,
        'finalData': finalData,
    }
    return render(request, 'myapp/newSearch.html', stuffForFronted)

