from cgitb import lookup
from flask import Flask, jsonify
import flask_restful as restful
from flask_restful import Api, Resource
from flask_cors import CORS
import pymongo
from flask_pymongo import PyMongo
import json
from bson import json_util
import dns
from mongo_db import MongoDB_Push


app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://lasheralberto:economiaUm94@cluster0.ov3vg.mongodb.net/test?authSource=admin&replicaSet=atlas-d1rt3z-shard-0&readPreference=primary&appname=MongoDB+Compass&ssl=true"
#"mongodb+srv://lasheralberto:economiaUm94@cluster0.ov3vg.mongodb.net/mongodbhotels?retryWrites=true&w=majority"

mongo = PyMongo(app)
api = Api(app)
CORS(app)
client = pymongo.MongoClient(app.config['MONGO_URI'], connect= True)
db = client.mongodbhotels

db_push = MongoDB_Push( cliente= client )
db_push.mongodb_pushdata_db( )


class HotelList(Resource):

   def get(self):

      hotels = db.weather_conditions.find()
      json_response = json.dumps(list(hotels), default=json_util.default)
      return json.loads(json_response), 200


class Hotel(Resource):
      
  def get(self, cityname):

      result = db.weather_conditions.find(
        {
        'id': cityname.capitalize()
        }
        )

      json_response = json.dumps(list(result), default=json_util.default)
      return json.loads(json_response)


api.add_resource(HotelList, '/')
api.add_resource(Hotel, '/<string:cityname>')


if __name__ == '__main__':
    app.run(debug=True)