# Web Scrapping Application using Django


## About
A Web Scrapping App made in Python and the Django framework. It is able to scrape different webpages.


## Requirements
The requirements can be found in [requirements.txt](https://github.com/Zero722/gbd/blob/django/DjangoProject/requirements.txt)


## Installation
The first thing to do is to clone the repository:
```
$ git clone -b django --single-branch https://github.com/Zero722/gbd.git
$ cd DjangoProject
```
Create a virtual environment and activate it:
```
$ virtualenv venv
$ venv\scripts\activate
```
Install dependencies:
```
(venv)$ pip install -r requirements.txt
```
Once pip has finished downloading the dependencies:
```
(venv)$ cd mysite
(venv)$ py manage.py runserver 
```
And navigate to ```http://127.0.0.1:8000/projects/```


## Endpoints
- Home: http://127.0.0.1:8000/projects/
- Upload config or URLs (One at a time):  http://127.0.0.1:8000/projects/upload/
- Upload config and URLs (Both at a time):  http://127.0.0.1:8000/projects/upload_both/
- List config:  http://127.0.0.1:8000/projects/list_config/
- View config of <scheme_name>: http://127.0.0.1:8000/projects/view_config/<scheme_name>
- Edit config of <scheme_name>: http://127.0.0.1:8000/projects/config/edit/<scheme_name>/


## Features
- Takes the URLs in CSV format, scrapes the webpages hit by the URls and converts it into a csv format for the users to download 
- Takes the configuration file in json format to indicate which data of the webpages needs to be scraped
- xPath of the configuration can be directly edited
- View configuration according to scheme name


## Technology Used
- HTML
- CSS
- JavaScript
- Python






