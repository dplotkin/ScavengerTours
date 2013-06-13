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

def addTour(title, description, clues, hints, ratings, coordinates, reviews, city, image):
    db.tours.insert({'title':title, 'description':description, 'clues':clues, 'hints':hints, 'ratings':ratings, 'coordinates': coordinates, 'reviews': reviews, 'city':city, 'image':image})

def addUser(username, accesskey):
    db.users.insert({'username':username, 'accesskey':accesskey, 'tours':[], 'points':0, 'currenttour':"None", 'currenttourstatus':"None"})

def getTour(title):
    return [[x['title'], x['description'], x['clues'], x['hints'], x['ratings'], x['coordinates'], x['reviews'],  x['city'], x['image']] for x in db.tours.find({'title':title})]

def getUser(username):
    return [[x['username'], x['accesskey'], x['tours'], x['points'], x['currenttour'], x['currenttourstatus']] for x in db.users.find({'username':username})]

def getUserList():
    return [[x['username'], x['accesskey']] for x in db.users.find()]

def getCityList():
    cities = []
    for x in db.tours.find():
        if x['city'] not in cities:
            cities.append(str(x['city']))
            print str(x['city'])
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

def addTourStop(title, clue, hint, coordinates):
    for tour in db.tours.find():
        if tour["title"] == title:
            tmpc = []
            tmph = []
            tmpco = []
            for c in tour["clues"]:
                tmpc.append(c)
            for h in tour["hints"]:
                tmph.append(h)
            for co in tour["coordinates"]:
                tmpco.append(co)
            tmpc.append(clue)
            tmph.append(hint)
            tmpco.append(coordinates)
            db.tours.update({"title":title},{"title":title, "description":tour["description"], "clues":tmpc, "hints":tmph, "ratings":tour["ratings"], "coordinates":tmpco, "reviews":tour["reviews"], "city": tour["city"], "image": tour["image"]})

def goToNextStage(username, title):
    for user in db.users.find():
        if user["username"] == username:
            print user["currenttourstatus"]
            if user["currenttourstatus"] == "Begin":
                db.users.update({"username":username},{"username":username, "accesskey":user["accesskey"], "tours":user["tours"], "points":user["points"], "currenttour":user["currenttour"], "currenttourstatus":"1"})
            else:
                if user["currenttourstatus"] != len(getTour(title)[0][2]):
                    db.users.update({"username":username},{"username":username, "accesskey":user["accesskey"], "tours":user["tours"], "points":user["points"], "currenttour":user["currenttour"], "currenttourstatus":str(int(user["currenttourstatus"])+1)})
                else:
                     db.users.update({"username":username},{"username":username, "accesskey":user["accesskey"], "tours":user["tours"], "points":user["points"], "currenttour":user["currenttour"], "currenttourstatus":"End"})

def addPoints(username):
    for user in db.users.find():
        if user["username"] == username:
            db.users.update({"username":username},{"username":username, "accesskey":user["accesskey"], "tours":user["tours"], "points":user["points"]+15, "currenttour":user["currenttour"], "currenttourstatus":user["currenttourstatus"]})

def __init__():
    drop()
    addUser("swyetzner","38472")
    # addUser("sbabski","62398")
    # print getUserList()
    addTour("New York Hipster Tour", "a hipster tour", ["Go here","Go there","Go back here"], ["stop being stupid","yes", "no"], [5,4,3,2,1], [[40.7927018,-73.9740501],[40.7927018,-73.9740501],[40.7927018,-73.9740501]], "this was bad",  "New York", "http://www.newyorkpersonalinjuryattorneyblog.com/wp-content/uploads/2010/06/NewYork.jpg")
    addTour("New York Not Hipster Tour", "a not hipster tour", ["Go here","Go there","Go back here"], ["stop being stupid","yes","no"], [5,4,3,2,1],[[40.7927018,-73.9740501],[40.7927018,-73.9740501],[40.7927018,-73.9740501]], "this was bad",  "New York", "http://www.sfexaminer.com/files/blog_images/New%20York%20skyline_0.jpg")
    addTour("New York Normal Tour", "a not hipster tour", ["Go here","Go there","Go back here"], ["stop being stupid","yes","no"], [5,4,3,2,1],[[40.7927018,-73.9740501],[40.7927018,-73.9740501],[40.7927018,-73.9740501]], "this was bad",  "New York", "http://www.drug-rehab.org/wp-content/uploads/2011/03/New-York-2.jpg")
    addTour("Washington Hipster Tour", "a hipster tour", ["Go here","Go there","Go back here"], ["stop being stupid","yes","no"], [5,4,3,2,1], [[40.7927018,-73.9740501],[40.7927018,-73.9740501],[40.7927018,-73.9740501]], "this was bad", "District of Columbia", "http://static.giantbomb.com/uploads/original/0/2251/969527-washington_dc.jpg")
    addCurrentTourtoUser("swyetzner","New York Hipster Tour")
    print getUser("swyetzner")
    print getTour("New York Hipster Tour")
    # print getTourList("New York City")
    print getCityList()                           
