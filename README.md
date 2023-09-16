# Amazon Seller central
### How to run the project
#### run these commands in the terminal
##### Option 1 - With Virtual Environment
```
cd amazon-seller-central
python -m pip install virtualenv
python -m virtualenv env
env\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
##### Option 2 - Without Virtual Environment
```
cd amazon-seller-central
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```