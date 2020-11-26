import dateparser
from application import app,db
from flask import render_template, request,Response,json
from pip._vendor import requests

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html",index=True)
@app.route("/courses")
@app.route("/courses/<term>")
def courses(term=" Spring 2019"):
    return render_template("courses.html", courseData=courseData, courses= True, term=term)

@app.route("/register")
def register():
    return render_template("index2.html", register= True)
@app.route("/login")
def login():
    return render_template("login.html", login= True)
@app.route("/search")
def  search():
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

#Getting Data from 2nd api
@app.route('/searchT', methods = ['GET', 'POST'])
def searchT():
    
    if request.method == 'POST':
        print("Inside Method")
        city = request.form.get('city')
        print("City Found Inside Request Method---------=:- "+city)
        
        #Comparsion city and state
        def stateName(city):
            print("The Name of city Inside State Name fuction-------=:- "+city)
            flag ='N'
            for data in courseData:
                if data["city"]== city:
                    flag = 'Y'
                    break
            #return data["state"]    
            if flag =='Y':
                return data["state"]
            else:
                return 'No data Found'
        
        # return render_template("Result.html")
        # city = 'srinagar'
        state = stateName(city)
        url = "http://api.airvisual.com/v2/city?city=%s&state=%s&country=india&key=ed06533f-c5d9-4b3e-8605-6d3c4c716970" %(city,state)
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data = payload)
        print(url)
        print(json.loads(response.text))
        airResponse = json.loads(response.text)["data"]
 
        qualityValue=airResponse["current"]["pollution"]["aqius"]
        # message_window=None
        # message=None
        # message_window=None
        # message_outdoor=None
        

        if(qualityValue<50):
            quality="Good"
            message="Wear a mask outdoors"
        elif(qualityValue>=51 and qualityValue<99):
            quality="Satisfactory"
            purifier="	Run an air purifier"   
            message="Wear a mask outdoors"
            message_outdoor="Avoid Outdoor Excercise" 
            message_window="Close your windows to avoid dirty outdoor air"
        elif(qualityValue>100 and qualityValue<=200):
            quality="Unhealthy For Sensitive Groups"
            purifier="	Run an air purifier"   
            message="Wear a mask outdoors"
            message_window="Close your windows to avoid dirty outdoor air"
            message_outdoor="Avoid Outdoor Games"
        elif(qualityValue>200 and qualityValue<=300):
            quality="Unhealthy"
        elif(qualityValue>301 and qualityValue<=400):
            quality="Very Poor"
        else:
            quality="Severe"

        #for weather priction
        weather_icon =  airResponse["current"]["weather"]["ic"]
        print(weather_icon)
        if(weather_icon =="06n"):
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


        #return render_template("enrollment.html", enrollment=True, data={"id":id, "title":title, "term":term ,"location":airResponse["city"], "pollution":airResponse["current"]["pollution"]["aqius"],"quality":quality})
        # return render_template("result.html", enrollment=True, data={"id":id, "title":title, "term":term ,"location":airResponse["city"], "pollution":airResponse["current"]["pollution"]["aqius"],"weather":airResponse["current"]["weather"]["tp"],"Humidity":airResponse["current"]["weather"]["hu"],"pressure":airResponse["current"]["weather"]["pr"],"windspeed":airResponse["current"]["weather"]["ws"],"quality":quality,"message":message,"message_window":message_window,"message_outdoor":message_outdoor})
        data = {}
        data['city']=airResponse['city']
        data['state']=airResponse['state']
        data['pollution']=airResponse["current"]["pollution"]["aqius"]
        print(qualityValue)
        data['value']=qualityValue
        data['message']=message_window
        data['quality']= quality 
        data['purifier']=purifier
        data['messageOutdoor'] =message_outdoor
        data['messageWindow']=message_window
        #WEATHER VARIABLE
        data['temperature']=airResponse["current"]["weather"]["tp"]
        data['pressure']=airResponse["current"]["weather"]["pr"]
        data['humidity'] = airResponse["current"]["weather"]["hu"]
        data['windspeed']=airResponse["current"]["weather"]["ws"]
        data['wind_direction']=airResponse["current"]["weather"]["wd"]
        data['icon']= output



        print(data)    
        
        return render_template("Result.html",data=data)

        
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
    url = "http://api.airvisual.com/v2/city?city=%s&state=%s&country=india&key=ed06533f-c5d9-4b3e-8605-6d3c4c716970" %(city,state)
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    print(url)
    print(json.loads(response.text))
    airResponse = json.loads(response.text)["data"]
 
    qualityValue=airResponse["current"]["pollution"]["aqius"]
    message_window=None
    message=None
    message_window=None
    message_outdoor=None
    

    if(qualityValue<50):
        quality="Good"
        message="Wear a mask outdoors" 
       
    elif(qualityValue>=51 and qualityValue<99):
        quality="Satisfactory"
        message="Wear a mask outdoors"
        message_outdoor="Avoid Outdoor Excercise" 
        message_window="Close your windows to avoid dirty outdoor air"
    elif(qualityValue>100 and qualityValue<=200):
        quality="Unhealthy For Sensitive Groups"
        message="Wear a mask outdoors"
        message_window="Close your windows to avoid dirty outdoor air"
        message_outdoor="Avoid Outdoor Games"
    elif(qualityValue>200 and qualityValue<=300):
        quality="Unhealthy"
    elif(qualityValue>301 and qualityValue<=400):
        quality="Very Poor"
    else:
        quality="Severe"
    #return render_template("enrollment.html", enrollment=True, data={"id":id, "title":title, "term":term ,"location":airResponse["city"], "pollution":airResponse["current"]["pollution"]["aqius"],"quality":quality})
    return render_template("index.html", enrollment=True, data={"id":id, "title":title, "term":term ,"location":airResponse["city"], "pollution":airResponse["current"]["pollution"]["aqius"],"weather":airResponse["current"]["weather"]["tp"],"Humidity":airResponse["current"]["weather"]["hu"],"pressure":airResponse["current"]["weather"]["pr"],"windspeed":airResponse["current"]["weather"]["ws"],"quality":quality,"message":message,"message_window":message_window,"message_outdoor":message_outdoor})
#                             
class  User(db.Document):
    user_id = db.IntField(unique = True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=30)
    email = db.StringField(max_length=30)
    password = db.StringField(max_length =30)
@app.route("/user")
def user():
    User(user_id=1, first_name="ubair",last_name="noor",email="ubairnoor@gmail.com", password="1234567").save()
    users = User.objects.all()
    return render_template("user.html", users=users)

@app.route("/infoaqi")
def infoaqi():
        return render_template("infoaqi.html", infoaqi=infoaqi)


# @app.route("/getdata")
# def api():
   
#course data

courseData = [ {"country":"india","state":"Jammu and kashmir","city":"Jammu"},
{"country":"india","state":"Jammu and kashmir","city":"Srinagar"},
{"country":"india","state":"Andhra Pradesh","city":"Amaravati"},
{"country":"india","state":"Andhra Pradesh","city":"Rajamahendravaram"},
{"country":"india","state":"Andhra Pradesh","city":"Tirupati"},
{"country":"india","state":"Andhra Pradesh","city":"Visakhapatnam"},
{"country":"india","state":"Bihar","city":"Gaya"},
{"country":"india","state":"Bihar","city":"Hajipur"},
{"country":"india","state":"Bihar","city":"Khagaul"},
{"country":"india","state":"Bihar","city":"Muzaffarpur"},
{"country":"india","state":"Bihar","city":"Patna"},
{"country":"india","state":"Delhi","city":"Alipur"},
{"country":"india","state":"Delhi","city":"Bawana"},
{"country":"india","state":"Delhi","city":"Defence Colony"},
{"country":"india","state":"Delhi","city":"Delhi"},
{"country":"india","state":"Delhi","city":"Deoli"},
{"country":"india","state":"Delhi","city":"Karol Bagh"},
{"country":"india","state":"Delhi","city":"New Delhi"},
{"country":"india","state":"Delhi","city":"Pitampura"},
{"country":"india","state":"Delhi","city":"Shahdara"},
{"country":"india","state":"Gujarat","city":"Adalaj"},
{"country":"india","state":"Gujarat","city":"Ahmedabad"},
{"country":"india","state":"Gujarat","city":"Ghandinagar"},
{"country":"india","state":"Gujarat","city":"Naroda"},
{"country":"india","state":"Gujarat","city":"Sarkhej"},
{"country":"india","state":"Gujarat","city":"Vapi"},
{"country":"india","state":"Haryana","city":"Ambala"},
{"country":"india","state":"Haryana","city":"Bahadurgarh"},
{"country":"india","state":"Haryana","city":"Bhiwani"},
{"country":"india","state":"Haryana","city":"Dharuhera"},
{"country":"india","state":"Haryana","city":"Faridabad"},
{"country":"india","state":"Haryana","city":"Fatehabad"},
{"country":"india","state":"Haryana","city":"Firozpur Jhirka"},
{"country":"india","state":"Haryana","city":"Gharaunda"},
{"country":"india","state":"Haryana","city":"Gurugram"},
{"country":"india","state":"Haryana","city":"Hisar"},
{"country":"india","state":"Haryana","city":"Jind"},
{"country":"india","state":"Haryana","city":"Kaithal"},
{"country":"india","state":"Haryana","city":"Narnaul"},
{"country":"india","state":"Haryana","city":"Palwal"},
{"country":"india","state":"Haryana","city":"Panchkula"},
{"country":"india","state":"Haryana","city":"Rohtak"},
{"country":"india","state":"Haryana","city":"Sirsa"},
{"country":"india","state":"Haryana","city":"Sonipat"},
{"country":"india","state":"Haryana","city":"Thanesar"},
{"country":"india","state":"Haryana","city":"Yamunanagar"},
{"country":"india","state":"Karnataka","city":"Bagalkot"},
{"country":"india","state":"Karnataka","city":"Bengaluru"},
{"country":"india","state":"Karnataka","city":"Bijapur"},
{"country":"india","state":"Karnataka","city":"Chik Ballapur"},
{"country":"india","state":"Karnataka","city":"Chikmagalur"},
{"country":"india","state":"Karnataka","city":"Closepet"},
{"country":"india","state":"Karnataka","city":"Gulbarga"},
{"country":"india","state":"Karnataka","city":"Hoskote"},
{"country":"india","state":"Karnataka","city":"Hubli"},
{"country":"india","state":"Karnataka","city":"Mysore"},
{"country":"india","state":"Kerala","city":"Cochin"},
{"country":"india","state":"Kerala","city":"Elur"},
{"country":"india","state":"Kerala","city":"Kannur"},
{"country":"india","state":"Kerala","city":"Kollam"},
{"country":"india","state":"Kerala","city":"Kozhikode"},
{"country":"india","state":"Kerala","city":"Thiruvananthapuram"},
{"country":"india","state":"Madhya Pradesh","city":"Bhopal"},
{"country":"india","state":"Madhya Pradesh","city":"Damoh"},
{"country":"india","state":"Madhya Pradesh","city":"Dewas"},
{"country":"india","state":"Madhya Pradesh","city":"Gwalior"},
{"country":"india","state":"Madhya Pradesh","city":"Indore"},
{"country":"india","state":"Madhya Pradesh","city":"Jabalpur"},
{"country":"india","state":"Madhya Pradesh","city":"Maihar"},
{"country":"india","state":"Madhya Pradesh","city":"Mandideep"},
{"country":"india","state":"Madhya Pradesh","city":"Murwara"},
{"country":"india","state":"Madhya Pradesh","city":"Pithampur"},
{"country":"india","state":"Madhya Pradesh","city":"Ratlam"},
{"country":"india","state":"Madhya Pradesh","city":"Satna"},
{"country":"india","state":"Madhya Pradesh","city":"Saugor"},
{"country":"india","state":"Madhya Pradesh","city":"Singrauli"},
{"country":"india","state":"Madhya Pradesh","city":"Ujjain"},
{"country":"india","state":"Maharashtra","city":"Airoli"},
{"country":"india","state":"Maharashtra","city":"Alandi"},
{"country":"india","state":"Maharashtra","city":"Artist Village"},
{"country":"india","state":"Maharashtra","city":"Aurangabad"},
{"country":"india","state":"Maharashtra","city":"Borivli"},
{"country":"india","state":"Maharashtra","city":"Chandrapur"},
{"country":"india","state":"Maharashtra","city":"Kalyan"},
{"country":"india","state":"Maharashtra","city":"Lohogaon"},
{"country":"india","state":"Maharashtra","city":"Mumbai"},
{"country":"india","state":"Maharashtra","city":"Nagpur"},
{"country":"india","state":"Maharashtra","city":"Nashik"},
{"country":"india","state":"Maharashtra","city":"Pimpri"},
{"country":"india","state":"Maharashtra","city":"Powai"},
{"country":"india","state":"Maharashtra","city":"Pune"},
{"country":"india","state":"Maharashtra","city":"Shivaji Nagar"},
{"country":"india","state":"Maharashtra","city":"Solapur"},
{"country":"india","state":"Maharashtra","city":"Thane"},
{"country":"india","state":"Maharashtra","city":"Uran"},
{"country":"india","state":"Maharashtra","city":"Virar"},
{"country":"india","state":"Odisha","city":"Brajrajnagar"},
{"country":"india","state":"Odisha","city":"Talcher"},
{"country":"india","state":"Punjab","city":"Amritsar"},
{"country":"india","state":"Punjab","city":"Bathinda"},
{"country":"india","state":"Punjab","city":"Jalandhar"},
{"country":"india","state":"Punjab","city":"Khanna"},
{"country":"india","state":"Punjab","city":"Ludhiana"},
{"country":"india","state":"Punjab","city":"Mandi Gobindgarh"},
{"country":"india","state":"Punjab","city":"Patiala"},
{"country":"india","state":"Punjab","city":"Ropar"},
{"country":"india","state":"Rajasthan","city":"Ajmer"},
{"country":"india","state":"Rajasthan","city":"Alwar"},
{"country":"india","state":"Rajasthan","city":"Bhiwadi"},
{"country":"india","state":"Rajasthan","city":"Jaipur"},
{"country":"india","state":"Rajasthan","city":"Jodhpur"},
{"country":"india","state":"Rajasthan","city":"Kota"},
{"country":"india","state":"Rajasthan","city":"Pali"},
{"country":"india","state":"Rajasthan","city":"Udaipur"},
{"country":"india","state":"Tamil Nadu","city":"Chennai"},
{"country":"india","state":"Tamil Nadu","city":"Chinnasekkadu"},
{"country":"india","state":"Telangana","city":"Hyderabad"},
{"country":"india","state":"Uttar Pradesh","city":"Agra"},
{"country":"india","state":"Uttar Pradesh","city":"Baraut"},
{"country":"india","state":"Uttar Pradesh","city":"Bulandshahr"},
{"country":"india","state":"Uttar Pradesh","city":"Dadri"},
{"country":"india","state":"Uttar Pradesh","city":"Dasna"},
{"country":"india","state":"Uttar Pradesh","city":"Daurala"},
{"country":"india","state":"Uttar Pradesh","city":"Ghaziabad"},
{"country":"india","state":"Uttar Pradesh","city":"Greater Noida"},
{"country":"india","state":"Uttar Pradesh","city":"Hapur"},
{"country":"india","state":"Uttar Pradesh","city":"Jaunpur"},
{"country":"india","state":"Uttar Pradesh","city":"Kadaura"},
{"country":"india","state":"Uttar Pradesh","city":"Kanpur"},
{"country":"india","state":"Uttar Pradesh","city":"Kirakat"},
{"country":"india","state":"Uttar Pradesh","city":"Kurara"},
{"country":"india","state":"Uttar Pradesh","city":"Loni"},
{"country":"india","state":"Uttar Pradesh","city":"Lucknow"},
{"country":"india","state":"Uttar Pradesh","city":"Meerut"},
{"country":"india","state":"Uttar Pradesh","city":"Moradabad"},
{"country":"india","state":"Uttar Pradesh","city":"Muzaffarnagar"},
{"country":"india","state":"Uttar Pradesh","city":"Noida"},
{"country":"india","state":"Uttar Pradesh","city":"Sector"},
{"country":"india","state":"Uttar Pradesh","city":"Varanasi"},
{"country":"india","state":"West Bengal","city":"Asansol"},
{"country":"india","state":"West Bengal","city":"Bara Bazar"},
{"country":"india","state":"West Bengal","city":"Barjora"},
{"country":"india","state":"West Bengal","city":"Howrah"},
{"country":"india","state":"West Bengal","city":"Kolkata"},
{"country":"india","state":"West Bengal","city":"Medinipur"},
{"country":"india","state":"West Bengal","city":"Siliguri"},
{"country":"india","state":"West Bengal","city":"Solap"}]