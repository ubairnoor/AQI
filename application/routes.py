import dateparser
from application import app, db, utilities
from flask import render_template, request, Response, json
from pip._vendor import requests
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='65bdc6b66ccc47128ad5934cc48cc804')


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/courses")
@app.route("/courses/<term>")
def courses(term=" Spring 2019"):
    return render_template("courses.html", courseData=courseData, courses=True, term=term)


@app.route("/register")
def register():
    return render_template("index2.html", register=True)


@app.route("/login")
def login():
    return render_template("login.html", login=True)


@app.route("/search")
def search():
    return render_template("search-page.html")


@app.route("/worldmap")
def worldMap():
    return render_template("WorldMap.html")


@app.route("/asia")
def asia():
    return render_template("asia.html")


@app.route("/europe")
def europe():
    return render_template("europe.html")


@app.route("/africa")
def africa():
    return render_template("africa.html")


@app.route("/southAmerica")
def southAmerica():
    return render_template("southAmerica.html")


@app.route("/northAmerica")
def northAmerica():
    return render_template("northAmerica.html")


@app.route("/news")
def news(country):
    data = country
    print(data)

    def country_code(country):
        print(country)
        for data in utilities.countryCodes:
            if (data["country"] == country):
                return data["code"]

    code_output = country_code(country)
    print("code_output")
    print(code_output)
    url = "http://newsapi.org/v2/top-headlines?country=%s&category=health&apiKey=65bdc6b66ccc47128ad5934cc48cc804" % (
        code_output)

    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    news = json.loads(response.text)
    Title = news["articles"]
    print(Title)
    return render_template("news.html", data=Title)


@app.route('/result2', methods=['GET', 'POST'])
def result2():
    input = request.form.get('input')

    print(input)

    def Lat_Lon_Find(input):
        url = "https://us1.locationiq.com/v1/search.php?key=pk.b31969419cb75a4fa46f0419635ee6c3&q=%s&format=json" % (
            input)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print(url)
        Lat = json.loads(response.text)[0]['lat']
        Lon = json.loads(response.text)[0]['lon']
        return(Lat, Lon, input)
        # print(json.loads(response.text))
        # latLon(input)

    def aqi(result):
        # adding waqi api
        url_value = "https://api.waqi.info/feed/%s/?token=4a10769fcaf1c9b08c25a271fd1c92b1ab1b1db0" % (
            result[2])
        print(url_value)
        payload = {}
        headers = {}
        response = requests.request(
            "GET", url_value, headers=headers, data=payload)
        print(response)
        Status_two = json.loads(response.text)["status"]
        print(Status_two)

        if(Status_two == "ok"):
            waqi_output = json.loads(response.text)["data"]
            aqi = waqi_output["aqi"]
            print(aqi)
        elif(Status_two == "error"):
            # airpollution api
            url_value = "http://api.airpollutionapi.com/1.0/aqi?lat=%s&lon=%s&APPID=lkoc3osdik3gc8u9hg67u0i4ni" % (
                result[0], result[1])
            print(url_value)
            payload = {}
            headers = {}
            response = requests.request(
                "GET", url_value, headers=headers, data=payload)
            print(response)
            Status = json.loads(response.text)["status"]
            if(Status == "success"):
                Output = json.loads(response.text)["data"]
                print("if condition worked")
                alert = Output["value"]
                country = Output["country"]
                print()
                news(country)
                print(country)
                print(alert)

        else:
            print("Inside the block")

    # def output(result):

        #url_value = "http://api.airpollutionapi.com/1.0/aqi?lat=%s&lon=%s&APPID=lkoc3osdik3gc8u9hg67u0i4ni"%(Lat,Lon)
        #payload = {}
       # headers= {}
        #response = requests.request("GET",url_value, headers=headers, data = payload)
        #Status = json.loads(response.text)["data"]
        #alert = Status["value"]

        #country = Status["country"]
    result = Lat_Lon_Find(input)
    aqi(result)

    # output(result)
    return render_template("result_input.html")

# Getting Data from 2nd api
@app.route('/searchT', methods=['GET', 'POST'])
def searchT():
    if request.method == 'POST':
        city = request.form.get('city')
        print("City Found Inside Request Method---------=:- " + city)
        city = city.title()
        # Comparsion city and state

        def stateName(city):
            print("The Name of city Inside State Name fuction-------=:- " + city)
            flag = 'N'
            for data in courseData:
                if data["city"] == city:
                    flag = 'Y'
                    break
            # return data["state"]
            if flag == 'Y':
                return data["state", "country"]
            else:
                return 'No data Found'

        # return render_template("Result.html")
        # city = 'srinagar'
        state = stateName(city)
        url = "http://api.airvisual.com/v2/city?city=%s&state=%s&country=%scountry&key=ed06533f-c5d9-4b3e-8605-6d3c4c716970" % (
            city, state, country)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print(url)
        print(json.loads(response.text))
        airResponse = json.loads(response.text)["data"]

        qualityValue = airResponse["current"]["pollution"]["aqius"]
        # message_window=None
        # message=None
        # message_window=None
        # message_outdoor=None

        if(qualityValue < 50):
            quality = "Good"
            message = "Wear a mask outdoors"
        elif(qualityValue >= 51 and qualityValue < 99):
            quality = "Satisfactory"
            purifier = "	Run an air purifier"
            message = "Wear a mask outdoors"
            message_outdoor = "Avoid Outdoor Excercise"
            message_window = "Close your windows to avoid dirty outdoor air"
        elif(qualityValue > 100 and qualityValue <= 200):
            quality = "Unhealthy For Sensitive Groups"
            purifier = "	Run an air purifier"
            message = "Wear a mask outdoors"
            message_window = "Close your windows to avoid dirty outdoor air"
            message_outdoor = "Avoid Outdoor Games"
        elif(qualityValue > 200 and qualityValue <= 300):
            quality = "Unhealthy"
        elif(qualityValue > 301 and qualityValue <= 400):
            quality = "Very Poor"
        else:
            quality = "Severe"

        # for weather priction
        weather_icon = airResponse["current"]["weather"]["ic"]
        print(weather_icon)
        if(weather_icon == "06n"):
            output = "Clear Sky"
        elif(weather_icon == "01n"):
            output = "Clear Sky(night)"
        elif(weather_icon == "02d"):
            output = "few Clouds(day)"
        elif(weather_icon == "02n"):
            output = "few clouds"
        elif(weather_icon == "03d"):
            output = "scattered cloud"
        elif(weather_icon == "04d"):
            output = "Broekn cloud"
        elif(weather_icon == "09d"):
            output = "shoer rain"
        elif(weather_icon == "04n"):
            output = "Rainday time"
        else:
            output = "Rain Night time"

        # return render_template("enrollment.html", enrollment=True, data={"id":id, "title":title, "term":term ,"location":airResponse["city"], "pollution":airResponse["current"]["pollution"]["aqius"],"quality":quality})
        # return render_template("result.html", enrollment=True, data={"id":id, "title":title, "term":term ,"location":airResponse["city"], "pollution":airResponse["current"]["pollution"]["aqius"],"weather":airResponse["current"]["weather"]["tp"],"Humidity":airResponse["current"]["weather"]["hu"],"pressure":airResponse["current"]["weather"]["pr"],"windspeed":airResponse["current"]["weather"]["ws"],"quality":quality,"message":message,"message_window":message_window,"message_outdoor":message_outdoor})
        data = {}
        data['city'] = airResponse['city']
        data['state'] = airResponse['state']
        data['pollution'] = airResponse["current"]["pollution"]["aqius"]
        print(qualityValue)
        data['value'] = qualityValue
        data['message'] = message_window
        data['quality'] = quality
        data['purifier'] = purifier
        data['messageOutdoor'] = message_outdoor
        data['messageWindow'] = message_window
        # WEATHER VARIABLE
        data['temperature'] = airResponse["current"]["weather"]["tp"]
        data['pressure'] = airResponse["current"]["weather"]["pr"]
        data['humidity'] = airResponse["current"]["weather"]["hu"]
        data['windspeed'] = airResponse["current"]["weather"]["ws"]
        data['wind_direction'] = airResponse["current"]["weather"]["wd"]
        data['icon'] = output
        print(data)

        return render_template("Result.html", data=data)

        # return redirect(url_for('booking', date=date))
        # return render_template('main/index.html')


# @app.route('/booking')
# def booking():
#     date = request.args.get('date', None)
#     return render_template('main/booking.html', date=date)
@app.route("/australia")
def australia():
    return render_template("australia.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/enrollment")
def enrollment():
    id = request.args.get('courseID')
    title = request.args.get('title')
    term = request.args.get('term')
    state = request.args.get('state')
    city = request.args.get('city')
    url = "http://api.airvisual.com/v2/city?city=%s&state=%s&country=india&key=ed06533f-c5d9-4b3e-8605-6d3c4c716970" % (
        city, state)
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(url)
    print(json.loads(response.text))
    airResponse = json.loads(response.text)["data"]
    qualityValue = airResponse["current"]["pollution"]["aqius"]
    message_window = None
    message = None
    message_window = None
    message_outdoor = None

    if(qualityValue < 50):
        quality = "Good"
        message = "Wear a mask outdoors"

    elif(qualityValue >= 51 and qualityValue < 99):
        quality = "Satisfactory"
        message = "Wear a mask outdoors"
        message_outdoor = "Avoid Outdoor Excercise"
        message_window = "Close your windows to avoid dirty outdoor air"
    elif(qualityValue > 100 and qualityValue <= 200):
        quality = "Unhealthy For Sensitive Groups"
        message = "Wear a mask outdoors"
        message_window = "Close your windows to avoid dirty outdoor air"
        message_outdoor = "Avoid Outdoor Games"
    elif(qualityValue > 200 and qualityValue <= 300):
        quality = "Unhealthy"
    elif(qualityValue > 301 and qualityValue <= 400):
        quality = "Very Poor"
    else:
        quality = "Severe"
    # return render_template("enrollment.html", enrollment=True, data={"id":id, "title":title, "term":term ,"location":airResponse["city"], "pollution":airResponse["current"]["pollution"]["aqius"],"quality":quality})
    return render_template("index.html", enrollment=True, data={"id": id, "title": title, "term": term, "location": airResponse["city"], "pollution": airResponse["current"]["pollution"]["aqius"], "weather": airResponse["current"]["weather"]["tp"], "Humidity": airResponse["current"]["weather"]["hu"], "pressure": airResponse["current"]["weather"]["pr"], "windspeed": airResponse["current"]["weather"]["ws"], "quality": quality, "message": message, "message_window": message_window, "message_outdoor": message_outdoor})
#


class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=30)
    email = db.StringField(max_length=30)
    password = db.StringField(max_length=30)


@app.route("/user")
def user():
    User(user_id=1, first_name="ubair", last_name="noor",
         email="ubairnoor@gmail.com", password="1234567").save()
    users = User.objects.all()
    return render_template("user.html", users=users)


@app.route("/infoaqi")
def infoaqi():
    return render_template("infoaqi.html", infoaqi=infoaqi)
