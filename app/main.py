from flask import Flask
import flask_restful as restful
from flask_restful import Api, Resource
from flask_cors import CORS
import pymongo
from flask_pymongo import PyMongo
import json
import json
from bson import json_util

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/mongodbhotels'
mongo = PyMongo(app)
api = Api(app)
CORS(app)


client = pymongo.MongoClient("mongodb+srv://lasheralberto:economiaUm94@cluster0.ov3vg.mongodb.net/mongodbhotels?retryWrites=true&w=majority")

# Opening JSON file
#json_file_hotels = open(r'\Users\Alberto\OneDrive\Escritorio\flutter_ebook\flask-jsonapi\my_data.json')
# returns JSON object as
# a dictionary
#hotels = json.load(json_file_hotels)

class HotelList(Resource):

   def get(self):
      hotels = list(client['mongodbhotels']['TravelAPI'].find())
      json_response = json.dumps(hotels, default=json_util.default)
      return json.loads(json_response), 200

class Hotel(Resource):
  def get(self, cityId):
    
      filter={
      'address.postalCode': cityId
      }
      docs_list  = list(client['mongodbhotels']['TravelAPI'].find(filter = filter))
      json_response = json.dumps(docs_list, default=json_util.default)
      return json.loads(json_response)

api.add_resource(HotelList, '/')
api.add_resource(Hotel, '/<int:cityId>')

if __name__ == '__main__':
    app.run()