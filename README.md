# Backend clone of social media app by using FastAPI
This API has 4 routes
## 1) Post route
This routes is respnsible for creating post, deleting post, updating post and Chencking post
## 2) Users route
This route is about creating users and searching user by id
## 3) Auth route
This route is about login system
## 4) Vote route
This route is about likes or vote system and this route contain code for upvote or back vote there is not logic about down vote

## How to run locally
First clone this repo by using following command
```bash
git clone https://github.com/V2003-k/fast-api.git
```
tehn
```bash
cd fast-api
```
Then install fastapi 
```bash
pip install "fastapi[standard]"
```
Then run the application using following command
```bash
fastapi dev app/main.py
```
Then you can use following link to use the API
```bash
http://127.0.0.1:8000/docs 
```
## After run this API you need a database in postres
Create a database in postgres then create a file name .env and write the following things in your file
```bash
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = passward_that_you_set
DATABASE_NAME = name_of_database
DATABASE_USERNAME = User_name
SECRET_KEY = 09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7 
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60(base)
```
## Note: SECRET_KEY in this example is just a psudo key. You need to get a key for yourself and you can get the SECRET_KEY from fastapi documentation