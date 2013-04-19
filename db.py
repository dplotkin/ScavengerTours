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

def addTour(title, clues, hints, ratings, reviews, coordinates, city, image):
    db.tours.insert({'title':title, 'clues':clues, 'hints':hints, 'ratings':ratings, 'reviews': reviews, 'coordinates': coordinates, 'city':city, 'image':image})

def addUser(username, accesskey):
    db.users.insert({'username':username, 'accesskey':accesskey, 'tours':[], 'points':0, 'currenttour':'None', 'currenttourstatus':'None'})

def getTour(title):
    return db.users.find({'title':title})

def getUser(username):
    return db.users.find({'username':username})

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

drop()
# addUser("swyetzner","38472")
# addUser("sbabski","62398")
# print getUserList()
addTour("New York Hipster Tour", ["Go here","Go there","Go back here"], ["stop being stupid","yes"], [5,4,3,2,1], 1231245.343, "this was bad",  "New York City", "img1")
addTour("New York Not Hipster Tour", ["Go here","Go there","Go back here"], ["stop being stupid","yes"], [5,4,3,2,1], 1231245.343, "this was bad",  "New York City", "img1")
addTour("Washington Hipster Tour", ["Go here","Go there","Go back here"], ["stop being stupid","yes"], [5,4,3,2,1], 1231245.343, "this was bad",  "Washington D.C.", "img1")
print getTourList("New York City")
print getCityList()

            
                             
    
