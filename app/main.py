from flask import Flask
import flask_restful as restful
from flask_restful import Api, Resource
from flask_cors import CORS

import json
app = Flask(__name__)
api = Api(app)
CORS(app)
 
# Opening JSON file
json_file_hotels = open('my_data.json')
 
# returns JSON object as
# a dictionary
hotels = json.load(json_file_hotels)



class HotelList(Resource):

   def get(self ):
      return hotels, 200

class Hotel(Resource):
  def get(self, cityId):
      listareturn = []
      for item in hotels:
        if item["address.postalCode"] == cityId:
           listareturn.append(item)
      return listareturn
    #return next(item for item in hotels if item["address.postalCode"] == cityId)


api.add_resource(HotelList, '/')
api.add_resource(Hotel, '/<int:cityId>')

if __name__ == '__main__':
    app.run()