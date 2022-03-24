from backend import Traveller

#Traveller.get_cities_for_db(
 #  '3ccd09de80msh288908a563dc4f2p1129c0jsn2c47d1d1d79c'
#)
from flask import Flask
import flask_restful as restful
from flask_restful import Api, Resource


import json
app = Flask(__name__)
api = Api(app)
 
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


api.add_resource(HotelList, '/hotels')
api.add_resource(Hotel, '/hotels/<int:cityId>')

if __name__ == '__main__':
    app.run(debug=True)