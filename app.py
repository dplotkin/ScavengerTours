from flask import Flask, render_template, session, url_for, request, redirect
from flask import render_template
import db

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = "tom_waits_is_grits"

@app.route("/")
def index():
    user = "Login"
    if "user" in session:
        user = session["user"]
        return redirect(url_for("home"))
    return render_template('index.html', title="Scavenger Tours", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    correct = 1
    if "user" in session:
        return redirect(url_for("index"))
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        correct = 0
        if db.verify(username, password):
            session["user"] = username
            return redirect(url_for("index"))
        else:
            correct = 0
    return render_template("signin.html", title="Login", correct=correct)

@app.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("index"))

@app.route("/getUser")
def getUser():
    if "user" in session:
        return session["user"]
    else:
        return ""

def geturl():
    return request.url

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST" and request.form["username"] and request.form["password"]:
        db.addUser(request.form["username"], request.form["password"])
        return redirect(url_for("login"))
    return render_template("signup.html", title="Register")

@app.route("/home")
def home():
    if "user" in session:
        currentStage = "None"
        currentCity = "None"
        points = db.getUser(session["user"])[0][3]
        currentTour = db.getUser(session["user"])[0][4]
        if currentTour != "None":
            currentCity = db.getTour(currentTour)[0][7]
            currentStage = db.getUser(session["user"])[0][5]
        print geturl()
        return render_template('homepage.html', title="Welcome", currentTour = currentTour, user = getUser(), points = points, currentCity = currentCity, currentStage = currentStage)
    else:
        return redirect(url_for("index"))

@app.route("/tours")
def tours():
    if "user" in session:
        listOfCities = db.getCityList()
        points = db.getUser(session["user"])[0][3]
        return render_template('manyCities.html', title="Choose a City", listOfCities=listOfCities, points = points)
    else:
        return redirect(url_for("index"))

@app.route("/error")
def error():
    return render_template('error.html')

@app.route("/<city>")
def city(city):
    if city not in db.getCityList():
        return redirect(url_for("error"))
    if "user" in session:
        points = db.getUser(session["user"])[0][3]
        tours = db.getTourList(city)
        count = len(tours)
        images = []
        for tour in tours:
            img = db.getTour(tour)[0][8]
            images.append(img)
        return render_template('city.html', city = city, tours = tours, images = images, points = points, count = count, title = city)
    else:
        return redirect(url_for("index"))

@app.route("/<city>/<tour>", methods=["GET","POST"])
def touroverview(city, tour):
    if "user" in session:
        description = db.getTour(tour)[0][1]
        points = db.getUser(session["user"])[0][3]
        image = db.getTour(tour)[0][8]
        if request.method == "POST":
            db.addCurrentTourtoUser(getUser(),tour)
            stage = str(db.getUser(getUser())[0][5])
            #return redirect(url_for("home"))
            return redirect("/"+city+"/"+tour+"/"+tour+"/"+stage)
        return render_template('touroverview.html', city=city, tour=tour, description = description, image = image, points = points, title = tour)
    else:
        return redirect(url_for("index"))

@app.route("/google")
def google():
    return render_template('google.html')

@app.route("/map")
def map():
    return render_template('map.html')

@app.route("/create", methods=["GET","POST"])
def create():
    city = ""
    points = db.getUser(session["user"])[0][3]
    cities = db.getCityList()
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        image = request.form["image"]
        city = request.form["selectedCity"]
        clues = []
        hints = []
        ratings = []
        reviews = []
        coordinates = []
        db.addTour(title, description, clues, hints, ratings, reviews, coordinates, city, image)
        return redirect("/"+title+"/create2/1")
    return render_template('create.html', cities = cities, points = points, title = "Create",city = city)

@app.route("/<tour>/create2/<num>", methods=["GET","POST"])
def create2(tour, num):
    number = num
    city = db.getTour(tour)[0][7]
    if request.method == "POST":
        if request.form.has_key("newness"):
            clue = request.form["clue"]
            hint = request.form["hint"]
            coords = request.form["coords"]
            newco = coords.split(',')
            lat = float(newco[0])
            lng = float(newco[1])
            newco = [lat,lng]
            print clue
            db.addTourStop(tour, clue, hint, newco)
            return redirect("/"+tour+"/create2/"+str(int(number) + 1))
        else:
            return redirect(url_for("home"))
    return render_template('create2.html', tour = tour, number = number, city = city)

@app.route("/<city>/<tour>/<tour1>/<stage>", methods=["GET","POST"])
def running(city, tour, tour1, stage):
    newstage = db.getUser(getUser())[0][5]
    points = db.getUser(session["user"])[0][3]
    print newstage
    stages = len(db.getTour(tour)[0][2]) - 1
    if newstage == "Begin":
        newstage = 0
    if int(newstage) == stages + 1:
        newstage = "End"
    if newstage == "End":
        return redirect("complete")
    newstage = int(newstage)
    clue = db.getTour(tour)[0][2][newstage]
    hint = db.getTour(tour)[0][3][newstage]
    latitude = db.getTour(tour)[0][5][newstage][0]
    print latitude
    longitude = db.getTour(tour)[0][5][newstage][1]
    # hint = db.getTour(tour)[0][3][newstage]
    print db.getUser(getUser())[0][5]
    if request.method == "POST":
        db.goToNextStage(getUser(),tour)
        print db.getUser(getUser())[0][5]
        sstage = str(db.getUser(getUser())[0][5])
        return  redirect("/"+city+"/"+tour+"/"+tour1+"/"+sstage)
    return render_template('runningtour.html', city=city, tour=tour, stage=newstage, clue = clue, stages = stages, latitude = latitude, longitude = longitude, points = points, title = tour, hint = hint)


@app.route("/complete")
def complete():
    if "user" in session:
        db.addPoints(getUser())
        points = db.getUser(session["user"])[0][3]
        db.addCurrentTourtoUser(getUser(),"None")
        return render_template("complete.html", points=points)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.debug=True
    app.run()
