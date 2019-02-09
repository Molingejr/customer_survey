# Customer Survey App
Customer fill out a form to rate his/her experience for the day

## Installation
Install Python 3.6 for your system

Create a python virtual environment
```
python3.6 -m venv <env_name>
```
Install Dependencies
```
source venv/bin/activate
pip install -r requirements
```
Run migrations
```
cd survey
python manage.py migrate
```
Create superuser for admin account
```
python manage.py createsuperuser
```

Run the Application
```
python manage.py runserver
```
