from pymongo import Connection

connection = Connection('mongo2.stuycs.org')
db = connection.admin
db = db.authenticate('ml7','ml7')
db = connection['BelarussianMafia']
tours = db['tours']
users = db['users']

def drop():
    db.tours.drop()

def addTour(title, clues, hints, ratings, reviews, coordinates, city, image):
    db.tours.insert({'title':title, 'clues':clues, 'hints':hints, 'ratings':ratings, 'reviews': reviews, 'coordinates': coordinates, 'city':city, 'image':image})

def addUser(username, accesskey):
    db.users.insert({'username':username, 'accesskey':accesskey, 'tours':[], 'points':0})

def getTour(title):
    return db.users.find({'title':title})

def getUser(username):
    return db.users.find({'username':username})

addUser("swyetzner","38472")
print getUser('swyetzner')


            
                             
    
