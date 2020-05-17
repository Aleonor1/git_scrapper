import requests
import threading
from bs4 import BeautifulSoup
from requests.compat import quote_plus


GITHUB_SEARCH_URL = 'https://github.com/search?q={}'
GITHUB_MULTIPLE_PAGES_SEARCH_URL = 'https://github.com/search?q={}'
GITHUB_REPO_URL ='https://github.com'
finalData=[]
def newSearch(search):
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

    return onTime(intNumberOfPages,search)


def onTime(intNumberOfPages,search):
    number = int(intNumberOfPages / 5)
    if (intNumberOfPages > 5):
        thread1 = threading.Thread(target=function, args=[0, number,finalData,intNumberOfPages,search], )
        thread2 = threading.Thread(target=function, args=[number, (number * 2) + 1,finalData,intNumberOfPages,search], )
        thread3 = threading.Thread(target=function, args=[(number * 2) + 1, (number * 3) + 1,finalData,intNumberOfPages,search], )
        thread4 = threading.Thread(target=function, args=[(number * 3) + 1, (number * 4) + 1,finalData,intNumberOfPages,search], )
        thread5 = threading.Thread(target=function, args=[(number * 4) + 1, intNumberOfPages,finalData,intNumberOfPages,search], )

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()

        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
    return set(finalData)


def function(fromNr, toNr, finalData, intNumberOfPages, search):
    j=0
    for i in range(fromNr, toNr):
        UrlWithPages = GITHUB_REPO_URL + '/search?q=' + search + '&p=' + str(i) + '& type = Repositories'
        response = requests.get(UrlWithPages)
        data = response.text
        soup = BeautifulSoup(data, features='html.parser')
        postListings = soup.find_all('li', {
            'class': 'repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source'})
        repoesQue = soup.find_all('div', {
            'class': 'd-flex flex-column flex-md-row flex-justify-between border-bottom pb-3 position-relative'})

        for post in postListings:
            url = GITHUB_REPO_URL + post.find('a').get('href')
            username = post.find('a').get('href')[1:].split('/')[0]
            repositoryName = post.find('a').get('href')[1:].split('/')[1]
            tag = post.find_all('a', {'class': 'topic-tag topic-tag-link f6 px-2 mx-0'})
            link = post.find_all()
            tagList = ""
            if (len(tag) != 0):
                for tags in tag:
                    tagList += tags.text
            else:
                tagList = 'N/A'
            if (search in tagList):
                finalData.append((username, repositoryName, url))
        j+=1
        if j==10:
            break




