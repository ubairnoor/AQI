import dateparser
from application import app,db
from flask import render_template, request,Response,json
from pip._vendor import requests
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='65bdc6b66ccc47128ad5934cc48cc804')

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
@app.route("/news")
def news(country):
    data=country
    print(data)
    def country_code(country):
      print(country)
      for data in CC:
            if (data["country"] == country):
                return data["code"]
    
    code_output = country_code(country)
    print("code_output")
    print(code_output)
    url="http://newsapi.org/v2/top-headlines?country=%s&category=health&apiKey=65bdc6b66ccc47128ad5934cc48cc804"%(code_output)
    
    payload = {}
    headers = {}
    response = requests.request("GET",url, headers=headers,data=payload)
    news = json.loads(response.text)
    Title = news["articles"]
    print(Title)
    return render_template("news.html",data=Title)

@app.route('/result2', methods = ['GET','POST'])
def result2():
    input = request.form.get('input')
   
    print(input)   
    def Lat_Lon_Find(input):
        url = "https://us1.locationiq.com/v1/search.php?key=pk.b31969419cb75a4fa46f0419635ee6c3&q=%s&format=json"%(input)
        payload = {}
        headers= {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print(url)
        Lat = json.loads(response.text)[0]['lat']
        Lon = json.loads(response.text)[0]['lon']
        return(Lat,Lon,input)
        #print(json.loads(response.text))
        #latLon(input)   
    def aqi(result):
        #adding waqi api
        url_value = "https://api.waqi.info/feed/%s/?token=4a10769fcaf1c9b08c25a271fd1c92b1ab1b1db0"%(result[2])
        print(url_value)
        payload = {}
        headers= {}
        response = requests.request("GET",url_value, headers=headers, data = payload)
        print(response) 
        Status_two = json.loads(response.text)["status"]
        print(Status_two)   
        
        if(Status_two == "ok"):
            waqi_output = json.loads(response.text)["data"]
            aqi=waqi_output["aqi"]
            print(aqi)  
        elif(Status_two == "error"):  
            #airpollution api
            url_value = "http://api.airpollutionapi.com/1.0/aqi?lat=%s&lon=%s&APPID=lkoc3osdik3gc8u9hg67u0i4ni"%(result[0],result[1])
            print(url_value)
            payload = {}
            headers= {}
            response = requests.request("GET",url_value, headers=headers, data = payload)
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
            
            
      
        
    #def output(result):
        
        #url_value = "http://api.airpollutionapi.com/1.0/aqi?lat=%s&lon=%s&APPID=lkoc3osdik3gc8u9hg67u0i4ni"%(Lat,Lon)
        #payload = {}
       # headers= {}
        #response = requests.request("GET",url_value, headers=headers, data = payload)
        #Status = json.loads(response.text)["data"]
        #alert = Status["value"]
        
        #country = Status["country"]
    result = Lat_Lon_Find(input)
    aqi(result)
    
    #output(result)
    return render_template("result_input.html")

@app.route("/faq")
def faq():
    return render_template()


#Getting Data from 2nd api
@app.route('/searchT', methods = ['GET', 'POST'])
def searchT():
    if request.method == 'POST':      
        city = request.form.get('city')
        print("City Found Inside Request Method---------=:- "+ city)
        city = city.title()
        #Comparsion city and state
        def stateName(city):
            print("The Name of city Inside State Name fuction-------=:- "+ city)
            flag ='N'
            for data in courseData:
                if data["city"]== city:
                    flag = 'Y'
                    break
            #return data["state"]    
            if flag =='Y':
                return data["state","country"]
            else:
                return 'No data Found'
        
        # return render_template("Result.html")
        # city = 'srinagar'
        state = stateName(city)        
        url = "http://api.airvisual.com/v2/city?city=%s&state=%s&country=%scountry&key=ed06533f-c5d9-4b3e-8605-6d3c4c716970" %(city,state,country)   
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
        data['icon']=output
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
CC = [{"country":"Afghanistan","code":"AF"},
{"country":"Albania","code":"AL"},
{"country":"Algeria","code":"DZ"},
{"country":"American Samoa","code":"AS"},
{"country":"Andorra","code":"AD"},
{"country":"Angola","code":"AO"},
{"country":"Anguilla","code":"AI"},
{"country":"Antarctica","code":"AQ"},
{"country":"Antigua and Barbuda","code":"AG"},
{"country":"Argentina","code":"AR"},
{"country":"Armenia","code":"AM"},
{"country":"Aruba","code":"AW"},
{"country":"Australia","code":"AU"},
{"country":"Austria","code":"AT"},
{"country":"Azerbaijan","code":"AZ"},
{"country":"Bahamas","	code":"BS"},
{"country":"Bahrain","code":"BH"},
{"country":"Bangladesh","code":"BD"},
{"country":"Barbados","code":"BB"},
{"country":"Belarus","code":"BY"},
{"country":"Belgium","code":"BE"},
{"country":"Belize","code":"BZ"},
{"country":"Benin","code":"BJ"},
{"country":"Bermuda","code":"BM"},
{"country":"Bhutan","code":"BT"},
{"country":"Bolivia","code":"BO"},
{"country":"Bonaire, Sint Eustatius and Saba","code":"BQ"},
{"country":"Bosnia and Herzegovina","code":"BA"},
{"country":"Botswana","code":"BW"},
{"country":"Bouvet Island","code":"BV"},
{"country":"Brazil","code":"BR"},
{"country":"British Indian Ocean Territory (the)","code":"IO"},
{"country":"Brunei Darussalam","code":"BN"},
{"country":"Bulgaria","code":"BG"},
{"country":"Burkina Faso","code":"BF"},
{"country":"Burundi","code":"BI"},
{"country":"Cabo Verde","code":"CV"},
{"country":"Cambodia","code":"KH"},
{"country":"Cameroon","code":"CM"},
{"country":"Canada","code":"CA"},
{"country":"Cayman Islands (the)","code":"KY"},
{"country":"Central African Republic (the)","code":"CF"},
{"country":"Chad","code":"TD"},
{"country":"Chile","code":"CL"},
{"country":"China","code":"CN"},
{"country":"Christmas Island","code":"CX"},
{"country":"Cocos (Keeling) Islands (the)","code":"CC"},
{"country":"Colombia","code":"CO"},
{"country":"Comoros (the)","code":"KM"},
{"country":"Congo (the Democratic Republic of the)","code":"CD"},
{"country":"Congo (the)","code":"CG"},
{"country":"Cook Islands (the)","code":"CK"},
{"country":"Costa Rica","code":"CR"},
{"country":"Croatia","code":"HR"},
{"country":"Cuba","code":"CU"},
{"country":"Curaçao","code":"CW"},
{"country":"Cyprus","code":"CY"},
{"country":"Czechia","code":"CZ"},
{"country":"Côte d'Ivoire","code":"CI"},
{"country":"Denmark","code":"DK"},
{"country":"Djibouti","code":"DJ"},
{"country":"Dominica","code":"DM"},
{"country":"Dominican Republic (the)","code":"DO"},
{"country":"Ecuador","code":"EC"},
{"country":"Egypt","code":"EG"},
{"country":"El Salvador","code":"SV"},
{"country":"Equatorial Guinea","code":"GQ"},
{"country":"Eritrea","code":"ER"},
{"country":"Estonia","code":"EE"},
{"country":"Eswatini","code":"SZ"},
{"country":"Ethiopia","code":"ET"},
{"country":"Falkland Islands (the) [Malvinas]","code":"FK"},
{"country":"Faroe Islands (the)","code":"FO"},
{"country":"Fiji","code":"FJ"},
{"country":"Finland","code":"FI"},
{"country":"France","code":"FR"},
{"country":"French Guiana","code":"GF"},
{"country":"French Polynesia","code":"PF"},
{"country":"French Southern Territories (the)","code":"TF"},
{"country":"Gabon","code":"GA"},
{"country":"Gambia (the)","code":"GM"},
{"country":"Georgia","code":"GE"},
{"country":"Germany","code":"DE"},
{"country":"Ghana","code":"GH"},
{"country":"Gibraltar","code":"GI"},
{"country":"Greece","code":"GR"},
{"country":"Greenland","code":"GL"},
{"country":"Grenada","code":"GD"},
{"country":"Guadeloupe","code":"GP"},
{"country":"Guam","code":"GU"},
{"country":"Guatemala","code":"GT"},
{"country":"Guernsey","code":"GG"},
{"country":"Guinea","code":"GN"},
{"country":"Guinea-Bissau","code":"GW"},
{"country":"Guyana","code":"GY"},
{"country":"Haiti","code":"HT"},
{"country":"Heard Island and McDonald Islands","code":"HM"},
{"country":"Holy See (the)","code":"VA"},
{"country":"Honduras","code":"HN"},
{"country":"Hong Kong","code":"HK"},
{"country":"Hungary","code":"HU"},
{"country":"Iceland","code":"IS"},
{"country":"India","code":"IN"},
{"country":"Indonesia","code":"ID"},
{"country":"Iran (Islamic Republic of)","code":"IR"},
{"country":"Iraq","code":"IQ"},
{"country":"Ireland","code":"IE"},
{"country":"Isle of Man","code":"IM"},
{"country":"Israel","code":"IL"},
{"country":"Italy","code":"IT"},
{"country":"Jamaica","code":"JM"},
{"country":"Japan","code":"JP"},
{"country":"Jersey","code":"JE"},
{"country":"Jordan","code":"JO"},
{"country":"Kazakhstan","code":"KZ"},
{"country":"Kenya","code":"KE"},
{"country":"Kiribati","code":"KI"},
{"country":"Korea","code":"KP"},
{"country":"Korea (the Republic of)","code":"KR"},
{"country":"Kuwait","code":"KW"},
{"country":"Kyrgyzstan","code":"KG"},
{"country":"Lao People's Democratic Republic (the)","code":"LA"},
{"country":"Latvia","code":"LV"},
{"country":"Lebanon","code":"LB"},
{"country":"Lesotho","code":"LS"},
{"country":"Liberia","code":"LR"},
{"country":"Libya","code":"LY"},
{"country":"Liechtenstein","code":"LI"},
{"country":"Lithuania","code":"LT"},
{"country":"Luxembourg","code":"LU"},
{"country":"Macao","code":"MO"},
{"country":"Madagascar","code":"MG"},
{"country":"Malawi","code":"MW"},
{"country":"Malaysia","code":"MY"},
{"country":"Maldives","code":"MV"},
{"country":"Mali","code":"ML"},
{"country":"Malta","code":"MT"},
{"country":"Marshall Islands (the)","code":"MH"},
{"country":"Martinique","code":"MQ"},
{"country":"Mauritania","code":"MR"},
{"country":"Mauritius","code":"MU"},
{"country":"Mayotte","code":"YT"},
{"country":"Mexico","code":"MX"},
{"country":"Micronesia (Federated States of)","code":"FM"},
{"country":"Moldova (the Republic of)","code":"MD"},
{"country":"Monaco","code":"MC"},
{"country":"Mongolia","code":"MN"},
{"country":"Montenegro","code":"ME"},
{"country":"Montserrat","code":"MS"},
{"country":"Morocco","code":"MA"},
{"country":"Mozambique","code":"MZ"},
{"country":"Myanmar","code":"MM"},
{"country":"Namibia","code":"NA"},
{"country":"Nauru","code":"NR"},
{"country":"Nepal","code":"NP"},
{"country":"Netherlands (the)","code":"NL"},
{"country":"New Caledonia","code":"NC"},
{"country":"New Zealand","code":"NZ"},
{"country":"Nicaragua","code":"NI"},
{"country":"Niger (the)","code":"NE"},
{"country":"Nigeria","code":"NG"},
{"country":"Niue","code":"NU"},
{"country":"Norfolk Island","code":"NF"},
{"country":"Northern Mariana Islands (the)","code":"MP"},
{"country":"Norway","code":"NO"},
{"country":"Oman","code":"OM"},
{"country":"Pakistan","code":"pk"},
{"country":"Palau","code":"PW"},
{"country":"Palestine, State of","code":"PS"},
{"country":"Panama","code":"PA"},
{"country":"Papua New Guinea","code":"PG"},
{"country":"Paraguay","code":"PY"},
{"country":"Peru","code":"PE"},
{"country":"Philippines (the)","code":"PH"},
{"country":"Pitcairn","code":"PN"},
{"country":"Poland","code":"PL"},
{"country":"Portugal","code":"PT"},
{"country":"Puerto Rico","code":"PR"},
{"country":"Qatar","code":"QA"},
{"country":"Republic of North Macedonia","code":"MK"},
{"country":"Romania","code":"RO"},
{"country":"Russian Federation (the)","code":"RU"},
{"country":"Rwanda","code":"RW"},
{"country":"Réunion","code":"RE"},
{"country":"Saint Barthélemy","code":"BL"},
{"country":"Saint Helena, Ascension and Tristan da Cunha","code":"SH"},
{"country":"Saint Kitts and Nevis","code":"KN"},
{"country":"Saint Lucia","code":"LC"},
{"country":"Saint Martin (French part)","code":"MF"},
{"country":"Saint Pierre and Miquelon","code":"PM"},
{"country":"Saint Vincent and the Grenadines","code":"VC"},
{"country":"Samoa","code":"WS"},
{"country":"San Marino","code":"SM"},
{"country":"Sao Tome and Principe","code":"ST"},
{"country":"Saudi Arabia","code":"SA"},
{"country":"Senegal","code":"SN"},
{"country":"Serbia","code":"RS"},
{"country":"Seychelles","code":"SC"},
{"country":"Sierra Leone","code":"SL"},
{"country":"Singapore","code":"SG"},
{"country":"Sint Maarten (Dutch part)","code":"SX"},
{"country":"Slovakia","code":"SK"},
{"country":"Slovenia","code":"SI"},
{"country":"Solomon Islands","code":"SB"},
{"country":"Somalia","code":"SO"},
{"country":"South Africa","code":"ZA"},
{"country":"South Georgia and the South Sandwich Islands","code":"GS"},
{"country":"South Sudan","code":"SS"},
{"country":"Spain","code":"ES"},
{"country":"Sri Lanka","code":"LK"},
{"country":"Sudan (the)","code":"SD"},
{"country":"Suriname","code":"SR"},
{"country":"Svalbard and Jan Mayen","code":"SJ"},
{"country":"Sweden","code":"SE"},
{"country":"Switzerland","code":"CH"},
{"country":"Syrian Arab Republic","code":"SY"},
{"country":"Taiwan (Province of China)","code":"TW"},
{"country":"Tajikistan","code":"TJ"},
{"country":"Tanzania, United Republic of","code":"TZ"},
{"country":"Thailand","code":"TH"},
{"country":"Timor-Leste","code":"TL"},
{"country":"Togo","code":"TG"},
{"country":"Tokelau","code":"TK"},
{"country":"Tonga","code":"TO"},
{"country":"Trinidad and Tobago","code":"TT"},
{"country":"Tunisia","code":"TN"},
{"country":"Turkey","code":"TR"},
{"country":"Turkmenistan","code":"TM"},
{"country":"Turks and Caicos Islands (the)","code":"TC"},
{"country":"Tuvalu","code":"TV"},
{"country":"Uganda","code":"UG"},
{"country":"Ukraine","code":"UA"},
{"country":"United Arab Emirates (the)","code":"AE"},
{"country":"United Kingdom of Great Britain and Northern Ireland (the)","code":"GB"},
{"country":"United States Minor Outlying Islands (the)","code":"UM"},
{"country":"United States of America (the)","code":"US"},
{"country":"Uruguay","code":"UY"},
{"country":"Uzbekistan","code":"UZ"},
{"country":"Vanuatu","code":"VU"},
{"country":"Venezuela (Bolivarian Republic of)","code":"VE"},
{"country":"Viet Nam","code":"VN"},
{"country":"Virgin Islands (British)","code":"VG"},
{"country":"Virgin Islands (U.S.)","code":"VI"},
{"country":"Wallis and Futuna","code":"WF"},
{"country":"Western Sahara","code":"EH"},
{"country":"Yemen","code":"YE"},
{"country":"Zambia","code":"ZM"},
{"country":"Zimbabwe","code":"ZW"},

{"country":"Åland Islands","code":"AX"}
]


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
{"country":"india","state":"West Bengal","city":"Solap"},
{"country":"China","state":"Anhui","city":"Anqing"},
{"country":"China","state":"Anhui","city":"Bengbu"},
{"country":"China","state":"Anhui","city":"Bozhou"},
{"country":"China","state":"Anhui","city":"Chaohu"},
{"country":"China","state":"Anhui","city":"Chizhou"},
{"country":"China","state":"Anhui","city":"Datong"},
{"country":"China","state":"Anhui","city":"Fuyang"},
{"country":"China","state":"Anhui","city":"Gushu"},
{"country":"China","state":"Anhui","city":"Hefei"},
{"country":"China","state":"Anhui","city":"Huaibei"},
{"country":"China","state":"Anhui","city":"Huainan"},
{"country":"China","state":"Anhui","city":"Huaiyuan Chengguanzhen"},
{"country":"China","state":"Anhui","city":"Huangshan"},
{"country":"China","state":"Anhui","city":"Jieshou"},
{"country":"China","state":"Anhui","city":"Jiujiang"},
{"country":"China","state":"Anhui","city":"Luan"},
{"country":"China","state":"Anhui","city":"Lucheng"},
{"country":"China","state":"Anhui","city":"Maanshan"},
{"country":"China","state":"Anhui","city":"Mengcheng Chengguanzhen"},
{"country":"China","state":"Anhui","city":"Mingguang"},
{"country":"China","state":"Beijing","city":"Beijing"},
{"country":"China","state":"Chongqing","city":"Beibei"},
{"country":"China","state":"Chongqing","city":"Chongqing"},
{"country":"China","state":"Chongqing","city":"Fuling"},
{"country":"China","state":"Chongqing","city":"Hechuan"},
{"country":"China","state":"Chongqing","city":"Jijiang"},
{"country":"China","state":"Chongqing","city":"Wanxian"},
{"country":"China","state":"Chongqing","city":"Yongchuan"},
{"country":"China","state":"Chongqing","city":"Yudong"},
{"country":"China","state":"Fujian","city":"Fuzhou"},
{"country":"China","state":"Fujian","city":"Longyan"},
{"country":"China","state":"Fujian","city":"Nanping"},
{"country":"China","state":"Fujian","city":"Ningde"},
{"country":"China","state":"Fujian","city":"Putian"},
{"country":"China","state":"Gansu","city":"Baiyin"},
{"country":"China","state":"Gansu","city":"Dingxi"},
{"country":"China","state":"Gansu","city":"Gannan"},
{"country":"China","state":"Gansu","city":"Jiayuguan"},
{"country":"China","state":"Guangdong","city":"Chaozhou"},
{"country":"China","state":"Guangdong","city":"Dongguan"},
{"country":"China","state":"Guangdong","city":"Foshan"},
{"country":"China","state":"Guangdong","city":"Guangzhou"},
{"country":"China","state":"Guangdong","city":"Heyuan"},
{"country":"China","state":"Guangdong","city":"Huizhou"},
{"country":"China","state":"Guangdong","city":"Jiangmen"},
{"country":"China","state":"Hainan","city":"Haikou"},
{"country":"China","state":"Hainan","city":"Sanya"},
{"country":"China","state":"Hebei","city":"Baoding Shi"},
{"country":"China","state":"Hebei","city":"Cangzhou Shi"},
{"country":"China","state":"Hebei","city":"Chengde"},
{"country":"China","state":"Hebei","city":"Handan"},
{"country":"China","state":"Henan","city":"Anyang"},
{"country":"China","state":"Henan","city":"Dingcheng"},
{"country":"China","state":"Henan","city":"Hebi"},
{"country":"China","state":"Henan","city":"Jiaozuo"},
{"country":"China","state":"Henan","city":"Jinchang"},
{"country":"China","state":"Henan","city":"Kaifeng"},
{"country":"China","state":"Henan","city":"Shangqiu"},
{"country":"China","state":"Shaanxi","city":"Ankang"},
{"country":"China","state":"Shaanxi","city":"Shangluo"},
{"country":"China","state":"Shaanxi","city":"Tongchuan"},
{"country":"China","state":"Shaanxi","city":"Weinan"},
{"country":"China","state":"Tibet","city":"Changdu"},
{"country":"China","state":"Tibet","city":"Lasa"},
{"country":"China","state":"Tibet","city":"Nagqu"},
{"country":"China","state":"Tibet","city":"Ngari"},
{"country":"China","state":"Tibet","city":"Nyingchi"},
{"country":"China","state":"Xinjiang","city":"Aksu"},
{"country":"China","state":"Xinjiang","city":"Altay"},
{"country":"China","state":"Xinjiang","city":"Bayinguoleng Mengguzizhizhou"},
{"country":"China","state":"Xinjiang","city":"Bortala"},
{"country":"China","state":"Xinjiang","city":"Changji"},
{"country":"China","state":"Xinjiang","city":"Ili"},
{"country":"China","state":"Xinjiang","city":"Karamay"},
{"country":"China","state":"Xinjiang","city":"Kashgar"},
{"country":"China","state":"Xinjiang","city":"Wujiaqu"}]