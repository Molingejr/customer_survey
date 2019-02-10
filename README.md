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

### Twilio Credentials
Go to **appointment/reminder/sms** and replace the Credentials for twilio account
ACCOUNT_SID, AUTH_TOKEN, SENDER_TEL with your twilio credentials

### Note
The Tel field of the schedule appointment form will require that you put your country code to the tel.
e.g. +14212215453

### Server URL
The app make use of `http://127.0.0.1:8000/` where this is accessible only on your local machine and needs extra server 
to interface with the outside world.

If your testing this application over a wifi network per say, go to `survey/feedback/sms` and change the `SERVER_URL`
 to your server url which interface with the outside world. Also update the ALLOWED_HOSTS list to include your ip.
This will allow users to open the link to the survey form of our application through the sent link on their devices. 
Run the application with ` python manage.py runserver ip_address:8000
`
All these is not needed if you have deployed and serving the application through servers like NGINX

