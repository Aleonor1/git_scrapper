from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models
from .models import RegisterForm
from django.core.mail import send_mail
from git_scrapper import settings
from gitsuggest import GitSuggest
from django.db.models import Count


GITHUB_SEARCH_URL = 'https://github.com/search?q={}'
GITHUB_MULTIPLE_PAGES_SEARCH_URL = 'https://github.com/search?'
GITHUB_REPO_URL ='https://github.com/'


def homeView(request):
    return render(request, 'homeView.html')

def recommand(request):
    finalData = []

    if 'search' in request.POST:
        githubUser=request.POST.get('search')
        gs = GitSuggest(username=githubUser)
        for data in gs.get_suggested_repositories():
            repo=data.full_name
            final_url = GITHUB_REPO_URL + repo
            response = requests.get(final_url)
            data = response.text

            soup = BeautifulSoup(data, features='html.parser')

            stars = soup.find(class_='social-count js-social-count').text
            description = soup.find(class_='text-gray-dark mr-2').text
            tag = soup.find_all('a',{'class':'topic-tag topic-tag-link'})

            tagList = ""
            if (len(tag) != 0):
                for tags in tag:
                    tagList += tags.text + ','
            else:
                tagList = 'N/A'

            user = repo.split('/')[0]
            projectName = repo.split('/')[0]


            finalData.append((projectName,user,description,stars,tagList))

        stuffForFronted = {
            'search': githubUser,
            'finalData': set(finalData),
            'totalData': set(finalData).__sizeof__(),
        }
        return render(request, 'myapp/recommandation.html', stuffForFronted)
    else:
        return render(request, 'myapp/recommand.html')


def sendMail(message):
    subject = 'GitScrapper New Topic'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['aleonornyikita@gmail.com', ]
    send_mail(subject, message, email_from, recipient_list)


def newSearch(request):
    searchText = request.POST.get('search')
    search = searchText
    current_user = request.user
    if models.Search.objects.filter(search=request.POST.get('search')).exists():
        t = models.Search.objects.get(search=searchText)
        t.count += 1
        t.save()
    else:
        models.Search.objects.create(search=search, user=current_user)

    print(models.Search.objects.order_by('count')[:5])

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
#    intNumberOfPages = int(int(numberOfQues[4].replace(',',''))/10)
    intNumberOfPages = 10
    container = soup.find("div", attrs={'class': 'd-md-flex flex-items-start flex-auto'})
    if (container!= None):
        definitie = container.find("p").text
    else:
        definitie = None
    finalData = []
    for i in range(0,intNumberOfPages):
        UrlWithPages = GITHUB_REPO_URL + '/search?q=' + search + '&p=' + str(i) + '& type = Repositories'
        response = requests.get(UrlWithPages)
        data = response.text
        soup = BeautifulSoup(data, features='html.parser')
        postListings = soup.find_all('li', {'class': 'repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source'})
        repoesQue = soup.find_all('div', {'class': 'd-flex flex-column flex-md-row flex-justify-between border-bottom pb-3 position-relative'})

        for post in postListings:
            url = GITHUB_REPO_URL+post.find('a').get('href')
            username = post.find('a').get('href')[1:].split('/')[0]
            repositoryName = post.find('a').get('href')[1:].split('/')[1]
            description = post.find(class_ = 'mb-1').text
            tag = post.find_all('a',{'class':'topic-tag topic-tag-link f6 px-2 mx-0'})
            tagList=""
            if (len(tag)!=0):
                for tags in tag:
                    tagList+=tags.text+','
            else:
                tagList ='N/A'
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
        'finalData': set(finalData),
        'def': definitie,
    }
    return render(request, 'myapp/newSearch.html', stuffForFronted)

def detailedSearchView(request):
    if 'actualSearch' in request.GET:
        return detailedSearch(request)
    else:
        return render(request, 'myapp/detailedSearch.html')

def subscribed(request):
    sendMail("new repo")
    return render(request, 'myapp/subscribed.html')

def notificationView(request):
    return render(request, 'notification.html')

def detailedSearch(request):
    search = request.GET.get('actualSearch')
    selectedProgrammingLanguage = request.GET.get('tools')
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
    #intNumberOfPages = int(int(numberOfQues[4].replace(',', '')) / 10)
    intNumberOfPages = 10
    container = soup.find("div", attrs={'class': 'd-md-flex flex-items-start flex-auto'})
    if (container != None):
        definitie = container.find("p").text
    else:
        definitie = None
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
            if (len(tag) != 0):
                for tags in tag:
                    tagList += tags.text + ','
            else:
                tagList = 'N/A'

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
        'def': definitie,
    }
    return render(request, 'myapp/newSearch.html', stuffForFronted)

def login(request):
    return render(request, 'login.html', name="login")

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return render(response, 'homeView.html')
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form":form})

def homepage(request):
    return render(request, 'home.html')


def sentvalue(request):
    value1 = request.GET['nameradio']
    print(request)
    return render(request, 'value.html', {'value2': value1, })
