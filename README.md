## HCS_TeamProject
UofG Human-Centred Security TeamProject

### Introduction
This is the code implementation of the survey website, which is a part of the University of Glasgow's MSC  Human-Centred Security Course.

### Environment Preparation
#### Install Anaconda Environment
```
conda create -n hcsTeamProject python=3.9
conda activate hcsTeamProject
```
#### Install required packages
```
pip install -r requirements.txt
```

### Database Preparation
The most important thing is that you should replace your database configuration(If you would like to build your own survey).   
After followed that, you can use the basic tools of Django to build your database by 
```
python manage.py migrate 
```
If you would like to change our design of database, you can overwrite our models and then run this command.
```
python manage.py makemigrations
```
We recommend the following software to manage the database：
* Navicat
* Datagrip

### Run
This project is based on Django, and you should start the service with the following command.
#### Notice
* Your pip requirements are all installed.

```
python manage.py runserver  
```

### SAMPLE
You can view the  project for this by visiting the following url: 
http://34.147.142.102/index/

* Invitation code: UofGHCS2024.
