from pymongo import Connection

connection = Connection('mongo2.stuycs.org')
db = connection.admin
db = db.authenticate('ml7','ml7')
db = connection['BelarussianMafia']
tours = db['tours']
users = db['users']

def drop():
    db.tours.drop()
    db.users.drop()

def addTour(title, description, clues, hints, ratings, reviews, coordinates, city, image):
    db.tours.insert({'title':title, 'description':description, 'clues':clues, 'hints':hints, 'ratings':ratings, 'reviews': reviews, 'coordinates': coordinates, 'city':city, 'image':image})

def addUser(username, accesskey):
    db.users.insert({'username':username, 'accesskey':accesskey, 'tours':[], 'points':0, 'currenttour':"None", 'currenttourstatus':"None"})

def getTour(title):
    return [[x['title'], x['description'], x['clues'], x['hints'], x['ratings'], x['reviews'], x['coordinates'], x['city'], x['image']] for x in db.tours.find({'title':title})]

def getUser(username):
    return [[x['username'], x['accesskey'], x['tours'], x['points'], x['currenttour'], x['currenttourstatus']] for x in db.users.find({'username':username})]

def getUserList():
    return [[x['username'], x['accesskey']] for x in db.users.find()]

def getCityList():
    cities = []
    for x in db.tours.find():
        if x['city'] not in cities:
            cities.append(x['city'])
    return cities

def getTourList(city):
    return [x['title'] for x in db.tours.find({'city':city})]

def verify(username, accesskey):
    if db.users.find({"username":username,"accesskey":accesskey}).count() != 0:
        return True
    else:
        return False

def addCurrentTourtoUser(username, title):
    for user in db.users.find():
        if user["username"] == username:
            db.users.update({"username":username},{"username":username, "accesskey":user["accesskey"], "tours":user["tours"], "points":user["points"], "currenttour":title, "currenttourstatus":"Begin"})

drop()
addUser("swyetzner","38472")
# addUser("sbabski","62398")
# print getUserList()
addTour("New York Hipster Tour", "a hipster tour", ["Go here","Go there","Go back here"], ["stop being stupid","yes"], [5,4,3,2,1], 1231245.343, "this was bad",  "New York City", "http://www.newyorkpersonalinjuryattorneyblog.com/wp-content/uploads/2010/06/NewYork.jpg")
addTour("New York Not Hipster Tour", "a not hipster tour", ["Go here","Go there","Go back here"], ["stop being stupid","yes"], [5,4,3,2,1], 1231245.343, "this was bad",  "New York City", "img1")
addTour("Washington Hipster Tour", "a hipster tour", ["Go here","Go there","Go back here"], ["stop being stupid","yes"], [5,4,3,2,1], 1231245.343, "this was bad",  "Washington D.C.", "img1")
addCurrentTourtoUser("swyetzner","New York Hipster Tour")
print getUser("swyetzner")
# print getTour("New York Hipster Tour")
# print getTourList("New York City")
# print getCityList()

            
                             
    
