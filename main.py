from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse, abort
from datetime import datetime
from pymongo import MongoClient
from includes import keys, detect_plant
import requests
from bson import json_util
import json

app = Flask(__name__)
api = Api(app)

mongo_client = MongoClient(keys.mongo)
db = mongo_client.florax
users_collection = db.users
plants_collection = db.plants
disease_collection = db.diseases
logs_collection = db.logs

#Creating a new user
create_user_args = reqparse.RequestParser()
create_user_args.add_argument('username', required=True, type=str, help='Username is required.')
create_user_args.add_argument('email', required=True, type=str, help='Email is required.')
create_user_args.add_argument('password', required=True, type=str, help="Password is required.")

#Loging a user 
login_user_args = reqparse.RequestParser()
login_user_args.add_argument('email', required=True, type=str, help='Email is required.')
login_user_args.add_argument('password', required=True, type=str, help="Password is required.")

#getting username
getting_username_args = reqparse.RequestParser()
getting_username_args.add_argument('email', required=True, type=str, help='Email is required.')

#Getting information about Plant
get_plants = reqparse.RequestParser()
get_plants.add_argument('name', required=True, type=str, help='Name is required.')
get_plants.add_argument('botanical_name', type=str, help='Botanical Name of the plant.')


#Getting Disease about Plant
get_disease = reqparse.RequestParser()
get_disease.add_argument('name', required=True, type=str, help='Name is required.')

#Creating a new plant
create_plant_args = reqparse.RequestParser()
create_plant_args.add_argument('name', required=True, type=str, help='Name of the plant is required.')
create_plant_args.add_argument('display_name', required=True, type=str, help='Display name of the plant is required.')
create_plant_args.add_argument('botanical_name', required=True, type=str, help='Botanical Name of the plant is required.')
create_plant_args.add_argument('image', required=True, type=str, help='Image link of the plant is required.')
create_plant_args.add_argument('water_per_day', required=True, type=str, help='Water Per Day for plant is required.')
create_plant_args.add_argument('sunlight_per_day', required=True, type=str, help='Sunlight / Day for the plant is required.')
create_plant_args.add_argument('temp', required=True, type=str, help='Average temperature of the plant is required.')
create_plant_args.add_argument('humidity', required=True, type=str, help='Humiditity of the plant is required.')
create_plant_args.add_argument('fertilizer', required=True, type=str, help='Name of the plant is required.')
create_plant_args.add_argument('description', required=True, type=str, help='Description of the plant is required.')
create_plant_args.add_argument('pests', required=True, type=str, help='pests of the plant is required.')
create_plant_args.add_argument('growing_conditions', required=True, type=str, help='Growing conditions the plant is required.')
create_plant_args.add_argument('health_benefits', required=True, type=str, help='Health Benefits of the plant is required.')
create_plant_args.add_argument('culinary_uses', required=True, type=str, help='Culinary Uses of the plant is required.')
create_plant_args.add_argument('common_diseases', required=True, type=str, help='Common Diseases of the plant is required.')
create_plant_args.add_argument('display_img', required=True, type=str, help='First Pest of the plant is required.')

#Pests
create_plant_args.add_argument('pest_1', required=True, type=str, help='First Pest of the plant is required.')
create_plant_args.add_argument('pest_1_img', required=True, type=str, help='First Pest of the plant is required.')
create_plant_args.add_argument('pest_2', required=True, type=str, help='Second Pest of the plant is required.')
create_plant_args.add_argument('pest_2_img', required=True, type=str, help='Second Pest of the plant is required.')
create_plant_args.add_argument('pest_3', required=True, type=str, help='Third Pest of the plant is required.')
create_plant_args.add_argument('pest_3_img', required=True, type=str, help='Third Pest of the plant is required.')
create_plant_args.add_argument('pest_4', required=True, type=str, help='Fourth Pest of the plant is required.')
create_plant_args.add_argument('pest_4_img', required=True, type=str, help='Fourth Pest of the plant is required.')

#culinary
create_plant_args.add_argument('culinary_1', required=True, type=str, help='First Culinary of the plant is required.')
create_plant_args.add_argument('culinary_1_img', required=True, type=str, help='First Culinary of the plant is required.')
create_plant_args.add_argument('culinary_2', required=True, type=str, help='Second Culinary of the plant is required.')
create_plant_args.add_argument('culinary_2_img', required=True, type=str, help='Second Culinary of the plant is required.')
create_plant_args.add_argument('culinary_3', required=True, type=str, help='Third Culinary of the plant is required.')
create_plant_args.add_argument('culinary_3_img', required=True, type=str, help='Third Culinary of the plant is required.')

#disease
create_plant_args.add_argument('disease_1', required=True, type=str, help='First Pest of the plant is required.')
create_plant_args.add_argument('disease_1_img', required=True, type=str, help='First Pest of the plant is required.')
create_plant_args.add_argument('disease_2', required=True, type=str, help='Second Pest of the plant is required.')
create_plant_args.add_argument('disease_2_img', required=True, type=str, help='Second Pest of the plant is required.')
create_plant_args.add_argument('disease_3', required=True, type=str, help='Third Pest of the plant is required.')
create_plant_args.add_argument('disease_3_img', required=True, type=str, help='Third Pest of the plant is required.')

#Create Disease pages
create_disease_args = reqparse.RequestParser()
create_disease_args.add_argument('name', required=True, type=str, help="Name of the plant is required.")
create_disease_args.add_argument('display_name', required=True, type=str, help="Display name of the plant is required.")
create_disease_args.add_argument('image', required=True, type=str, help='Image URL is required.')
create_disease_args.add_argument('description', required=True, type=str, help="Description of the plant is required.")
create_disease_args.add_argument('symptoms', required=True, type=str, help="Symptoms of the plant is required.")
create_disease_args.add_argument('cure', required=True, type=str, help="Cure of the plant is required.")


#Updating Plant information
update_plant_args = reqparse.RequestParser()
update_plant_args.add_argument('name', type=str, required=True, help='Plant name is required.')
update_plant_args.add_argument('display_name', type=str, help='Display name of the plant is required.')
update_plant_args.add_argument('botanical_name', type=str, help='Botanical Name of the plant is required.')
update_plant_args.add_argument('image', type=str, help='Image link of the plant is required.')
update_plant_args.add_argument('origin_short', type=str, help='Origin of the plant in one or two words.')
update_plant_args.add_argument('culinary_uses_short', type=str,help='Culinary uses of the plant in one or two words.')
update_plant_args.add_argument('growing_conditions_short', type=str, help='Growing Conditions of the plant in one or two words.')
update_plant_args.add_argument('pests_short', type=str, help='Pests of the plant.')
update_plant_args.add_argument('health_benefits_short', type=str, help='Health benefits of the plants.')
update_plant_args.add_argument('description', type=str, help='Description of the plants in 2 or 3 lines.')
update_plant_args.add_argument('appearance', type=str, help='Appearance of the plants in 2 or 3 lines.')
update_plant_args.add_argument('growing_conditons', type=str, help='Growing Conditions of the plants in 2 or 3 lines.')

#Getting Weather info
get_weather_args = reqparse.RequestParser()
get_weather_args.add_argument('city',required=True, type=str, help="City is required.")

#Create logs
update_logs_args = reqparse.RequestParser()
update_logs_args.add_argument('datetime', required=True, type=str, help="DateTime is required.")
update_logs_args.add_argument('animal',required=True, type=str, help="Name of the Animal is required.")

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return json_util.default(o)
        return json.JSONEncoder.default(self, o)

class Create_User(Resource):
    def put(self):
        args = create_user_args.parse_args()
        user = users_collection.find_one({'username': args.username})
        
        if user: abort(409, message="User already exists.")
        else:
            args['date_created'] = datetime.utcnow()
            users_collection.insert_one(args)

            return {"message":"User Created Successfully", 'valid':'true'}

class Get_Username(Resource):
    def put(self):
        args = getting_username_args.parse_args()
        return {'username' : 'Praanesh'}

class Login_User(Resource):      
    def put(self):
        args = login_user_args.parse_args()
        user = users_collection.find_one({'email': args.email})
        if not user:
            return {'message':'User not found', 'valid':'false'}
        if user['password'] != args.password:
            return {'message':'Invalid Credentials', 'valid':'false'}
        else:
            return {"valid":"true"}
class Get_Disease(Resource):
    def put(self):
        args = get_disease.parse_args()
        disease = disease_collection.find_one({'name':args.name})
        if disease:
            try: del disease['_id']
            except Exception as e: print(e)
            data = {}
            for i in disease:
                data[i] = disease[i]
            return data
        else: abort(409)

class Get_Plants(Resource):
    def put(self):
 
        args = get_plants.parse_args()
        # args = {'water_per_day' : '50 ml', 'sunlight_per_day': '7 hrs', 'temp':'22 °C', 'humidity': '70%', 'fertilizer':'300 kg', 'description':'Monstera is a tropical plant native to Central and South America, prized for its large, perforated leaves and unique appearance. It is a popular houseplant and is believed to bring good luck and prosperity' }
        #return args
        plant = plants_collection.find_one({'name': args.name})
        # args = {'display_name': 'banana', 'botanical_name': 'Musa acuminata', 'image': 'https://image/lnk', 'origin_short': 'Southeast Asia', 'appearance_short': 'Large leaves', 'culinary_uses_short': 'Fresh, Cooking', 'growing_conditions_short': None, 'pests_short': 'Aphids, Thrips', 'health_benefits_short': 'Nutrient-rich', 'description': 'The banana tree is a large, herbaceous plant that \nbelongs to Musaceae family. It is characterized by its \ntall, slender trunk, which is made up of tightly packed \nleaf sheaths and can grow up to 30 feet (9 meters) in \nheight.', 'appearance': 'Banana plants have a stout pseudostem and large, \nsmooth, shiny leaves with a distinct midrib. The fruit is \na long, curved, and slightly tapered berry with a thin, \neasily peeled skin that turns yellow when ripe.', 'growing_conditons': None}
        # return args
        if plant:
            del plant['_id']
            data = {}
            for i in plant:
                data[i] = plant[i]
            
            # print(data)

            return data
        else: 
            abort(404, message = 'Plant not found')

class Create_Plant(Resource):
    def put(self):
        args= create_plant_args.parse_args()
        plant = plants_collection.find_one({'name':args.name})
        if plant:abort(409, message="Plant already exists")
        else:
            plants_collection.insert_one(args)
            return {'message':"Plant Created Successfully"}

class Update_Plant(Resource):
    def put(self):
        args = update_plant_args.parse_args()
        plants_collection.update_one({'name':args['name']}, {'$set':args})
        return {'message':'Updated Successfully.'}

class Get_Weather(Resource):
    def put(self):
        args = get_weather_args.parse_args()
        url = "http://api.openweathermap.org/data/2.5/weather?appid=" + keys.openweathermap + "&q=" + args.city
        response = requests.get(url).json()
        return response

class Detect_Plant(Resource):
    def post(self):
        image_file = request.files['image']
        plant_predicted = detect_plant.detect_plant(image_file)
        print('________________________')
        print(plant_predicted)
        print('________________________')

        plant = plants_collection.find_one({'ml_keyword':plant_predicted['plant_name']})
        try:
            del plant['_id']
        except Exception as e: print(e)

        return plant

class Create_Disease(Resource):
    def put(self):
        args = create_disease_args.parse_args()

        disease = disease_collection.find_one({'name':args.name})
        if disease:
            abort(409, message="Plant already exists")
        else:
            disease_collection.insert_one(args)
            return  {'message':"Disease Created Successfully"}

class Detect_Disease(Resource):
    def post(self):
        image_file = request.files['image']
        plant_predicted = detect_plant.detect_diesease(image_file)
        print('________________________')
        print(plant_predicted)
        print('________________________')
        return plant_predicted

class Get_Logs(Resource):
    def get(self):
        res = []
        logs = list(logs_collection.find())
        for i in logs:
            del i["_id"]
            res.append(i)
        return json.loads(json.dumps(res, indent=2, cls=JSONEncoder))

class Update_Logs(Resource):
    def put(self):
        args = update_logs_args.parse_args()
        args['datetime'] = datetime.fromisoformat(args['datetime'])
        print(args)
        try:
            logs_collection.insert_one(args)

            return {"message": "Log created successfully."}
        except Exception as e:
            return {"exception" : e}
            
class Test(Resource):
    def get(self):
        return "FloraX"
        
api.add_resource(Test,'/')
api.add_resource(Create_User, '/user/register')
api.add_resource(Login_User, '/user/login')
api.add_resource(Get_Username, '/user/info')
api.add_resource(Get_Plants, '/plant')
api.add_resource(Create_Plant, '/plant/create')
api.add_resource(Update_Plant, '/plant/update')
api.add_resource(Detect_Plant, '/plant/detect')
api.add_resource(Get_Disease, '/disease')
api.add_resource(Detect_Disease, '/disease/detect') 
api.add_resource(Create_Disease, '/disease/create')
api.add_resource(Get_Weather, '/weather')
api.add_resource(Get_Logs, '/logs')
api.add_resource(Update_Logs, '/logs/update')