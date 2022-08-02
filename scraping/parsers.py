import requests


from  bs4 import BeautifulSoup as bs
from random import randint
__all__ = ('hh','ishkop','uzjobble')



headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]

def hh(url,city=None,language=None):

    jobs = []

    if url:

        r = requests.get(url, headers=headers[randint(0, 2)])
        if r.status_code==200:
            soup=bs(r.content,'html.parser')
            main_div=soup.find('div','sticky-sidebar-and-content--NmOyAQ7IxIOkgRiBRSEg')

            if main_div:
#
                vacations=main_div.find_all('div',"vacancy-serp-item__layout")




                for vacation in vacations:
                    if vacation.find('span', 'bloko-header-section-3'):

                        salary=vacation.find('span', 'bloko-header-section-3').get_text()
                    else:
                        salary='Kelishilgan holatda'
                    title_and_format=vacation.find('a','bloko-link')

                    title =title_and_format.get_text()


                    description= vacation.find('div','g-user-content').get_text()

                    jobs.append({
                        'url':title_and_format.get('href'),
                        'title': title,
                        'company':'Malumot asosiy saytda',
                        'salary': salary,
                        'description':description,
                        'city_id': city,
                        'language_id': language
})

        return jobs






def uzjobble(url,city=None,language=None):
    jobs = {}

    if url:
        r = requests.get(url, headers=headers[randint(0, 2)])

        if r.status_code==200:
            soup=bs(r.content,'html.parser')





            vacations=soup.find_all('article','yKsady')



            for vacation in vacations:


                title = vacation.find('span','_33bQdO').get_text()

                description = vacation.find('div','_9jGwm1').get_text()

                jobs={
                    'url':vacation.find_next('a').get('href'),
                    'title': title,
                    'company':'Companiya nomi',
                    'salary': "Kelishilgan holatda",
                    'description':description,
                    'city_id': city,
                    'language_id': language
}


    return jobs


def ishkop(url,city=None,language=None):
    total_url='https://ishkop.uz/viewjob?'
    add_url='&src=js&sid=EXxoW7VH2ghBPm73bpBQQqVjMoz7MolU'
    jobs = []

    if url:
        r = requests.get(url, headers=headers[randint(0, 2)])
        if r.status_code==200:
            soup=bs(r.content,'html.parser')
            main_div=soup.find('div','jobs')
            if main_div:

                 vacations=main_div.find_all('article','job no-logo')

                 for vacation in vacations:

                     title_and_url=vacation.find('h2','title').find_next('a')
                     href=title_and_url.get('href')
                     url_v = href[7:]
                     if vacation.find('div','company-job-data').find_next('div','company'):
                         com=vacation.find('div','company-job-data').find_next('div','company').get_text()
                     else:
                         com="Kompaniya haqida ma'lumot yoq"
                     title = title_and_url.get_text()
                     if vacation.find('div','company-job-data').find_next('div','salary'):
                         salary=vacation.find('div','company-job-data').find_next('div','salary').get_text()
                     else:
                         salary='Kelishilgan holatda'
                     description = vacation.find('div','desc').get_text()

                     jobs.append({
                        'url':total_url+url_v+add_url,
                        'title':title ,
                        'company':com,
                        'salary':salary,
                        'description':description,
                        'city_id': city,
                        'language_id': language
                     })

    return jobs

