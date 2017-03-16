# DjangoLab #
This isn't something big, but just a little playground for myself.

## class_mgt ##
### What is it? ###
My school assignment in NTUST, a little web-based system built with Django to manage and organize the events and activities in class.

### Preparation ###
As I am using Ubuntu 15.10 to develop this, you may need to find equivalents of the following packages in your favourite OS.

1. Install required packages
```
sudo apt-get install python3-dev build-essential
```
2. Get pip installed
```
curl https://bootstrap.pypa.io/get-pip.py | sudo python3
```
3. Git clone the repo and prepare your development environment
```
git clone https://github.com/easontse/djangolab.git
cd djangolab
python3 -m virtualenv venv
```
4. Install required pip packages with `requirement.txt` in `class_mgt`
```
pip install -r class_mgt/requirement.txt
```
5. Make a model migrations to the class_mgt project
```
cd class_mgt
python3 manage.py makemigrations
python3 manage.py migrate
```
6. Finally, run the build-in web server to test:
```
python3 manage.py runserver 0.0.0.0:8000
```
