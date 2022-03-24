#from pandas.io import parsers
#for locations api
from requests.models import Response
import requests
import pandas as pd 
import json
import datetime
from datetime import datetime, timezone



class Traveller:
    
    def __init__(self, rapid_key) -> None:
        self.rapid_key = rapid_key


    def get_all_cities(self):

        url = "https://cost-of-living-and-prices.p.rapidapi.com/cities"

        headers = {
            'x-rapidapi-host': "cost-of-living-and-prices.p.rapidapi.com",
            'x-rapidapi-key': self.rapid_key
            }

        response = requests.get(url, headers= headers).json()
        dfc = pd.DataFrame.from_dict(response, orient='columns')
        df_cities = pd.json_normalize(dfc['cities'])[['city_name', 'country_name']]
        cities_list = list(df_cities.loc[df_cities['country_name']=='Spain']['city_name'])
        return cities_list

    def query_api_locations(self,p_city):

        url = "https://hotels4.p.rapidapi.com/locations/v2/search"

        querystring = {"query": p_city}

        headers = {
            'x-rapidapi-host': "hotels4.p.rapidapi.com",
            'x-rapidapi-key': self.rapid_key
            }
        response = requests.get(url, headers= headers, params= querystring).json()
        try:
            df = pd.DataFrame.from_dict(response, orient='columns')
            return df
        except:
            print('Limite de API hotels')
        
        

    def get_location_df(self, p_city):

        query_locations=self.query_api_locations(p_city)
        dfcity=pd.DataFrame(columns=['geoId', 'destinationId', 'landmarkCityDestinationId', 'type',
                'redirectPage', 'latitude', 'longitude', 'searchDetail', 'caption',
                'name'])
        for i in range(0,4):
            a = query_locations.to_json()
            a=json.loads(a)
            city_group = pd.json_normalize(a['suggestions'])[f'{i}.entities'].to_json()
            city_group= json.loads(city_group)
            dfcity_group = pd.json_normalize(city_group['0'])
            dfcity= pd.concat([dfcity, dfcity_group])
            cityId = dfcity.loc[dfcity['name']==p_city]['destinationId']
        return cityId

            

    def get_properties_list(self, p_destinationId, p_adults):

        url = "https://hotels4.p.rapidapi.com/properties/list"


        querystring = {"destinationId":p_destinationId,"pageNumber":"1","pageSize":'50',"checkIn":"2020-01-08","checkOut":"2020-01-15","adults1":p_adults,"sortOrder":"PRICE","locale":"en_US","currency":"USD"}

        headers = {
            'x-rapidapi-host': "hotels4.p.rapidapi.com",
            'x-rapidapi-key': self.rapid_key
            }

        #response = requests.request("GET", url, headers=headers, params=querystring)
        #print(response.text)

        response = requests.get(url, headers= headers, params= querystring).json()

        df = pd.DataFrame.from_dict(response, orient='columns')

        return df


    def get_transport_photelid(self, p_hotelid):

        url = "https://hotels4.p.rapidapi.com/properties/get-details"

        querystring = {"id":p_hotelid,"checkIn":"2020-01-08","checkOut":"2020-01-15","adults1":"1","currency":"USD","locale":"en_US"}

        headers = {
            'x-rapidapi-host': "hotels4.p.rapidapi.com",
            'x-rapidapi-key': self.rapid_key
            }

        response = requests.request("GET", url, headers=headers, params=querystring).json()

        
        return response


    def get_hotel_list(self, p_city, p_adults):

        cityId = self.get_location_df(p_city)

        if cityId is None:

            pass

        else:

            hotel_list = self.get_properties_list(cityId, p_adults)
            hotel_list = hotel_list.to_json()
            hotel_list=json.loads(hotel_list)
            hotel_list=pd.json_normalize(hotel_list['data'])['body.searchResults.results'].to_json()
            hotel_list = json.loads(hotel_list)
            hotel_list = pd.json_normalize(hotel_list['0'])[['id','name','starRating','neighbourhood','supplierHotelId','ratePlan.price.exactCurrent','guestReviews.rating','address.postalCode','address.locality','address.countryName']]
            now = datetime.now(tz = timezone.utc)
            hotel_list['date_update'] = datetime.now()

            transportesdf_allHotelsId = pd.DataFrame(columns= ['name', 'distance', 'distanceInTime', 'type_transports','hotelId', 'cityname'])


            for hotelId in hotel_list['id']:
                try:
                    #transportation_options_df = pd.json_normalize(pd.DataFrame.from_dict(json.loads(pd.json_normalize(pd.json_normalize(get_transport_hotelid(hotelId)['transportation'])['transportLocations']).to_json()), orient='index')['0'])
                    df_transports = pd.json_normalize(pd.DataFrame.from_dict(json.loads(pd.json_normalize(pd.json_normalize(self.get_transport_photelid(hotelId)['transportation'])['transportLocations']).to_json()), orient='index')['0'])
                except:
                    pass

                df_transports_air = df_transports.loc[df_transports['category']=='airport']
                df_transports_train = df_transports.loc[df_transports['category']=='train-station']
                df_transports_metro = df_transports.loc[df_transports['category']=='metro']

                try:
                    df_transports_air = pd.json_normalize(pd.DataFrame.from_dict(json.loads(pd.json_normalize(df_transports_air['locations']).to_json()), orient='index')['0'])
                except:
                    pass

                try:
                    df_transports_train = pd.json_normalize(pd.DataFrame.from_dict(json.loads(pd.json_normalize(df_transports_train['locations']).to_json()), orient='index')['0'])
                except:
                    pass

                try:
                    df_transports_metro = pd.json_normalize(pd.DataFrame.from_dict(json.loads(pd.json_normalize(df_transports_metro['locations']).to_json()), orient='index')['0'])
                except:
                    pass

                df_transports_air['type_transport'] = 'airport'
                df_transports_train['type_transports'] = 'train'
                df_transports_metro['type_transports'] = 'metro'

                df_transports_air['hotelId'] = hotelId
                df_transports_train['hotelId'] = hotelId
                df_transports_metro['hotelId'] = hotelId
                df_transports_air['cityname'] = p_city
                df_transports_train['cityname'] = p_city
                df_transports_metro['cityname'] = p_city


                transportesdf_allHotelsId = pd.concat([df_transports_air, df_transports_train, df_transports_metro])

        
            return  hotel_list, transportesdf_allHotelsId

    def cost_of_living_pcity(self, p_city):

        url = "https://cost-of-living-and-prices.p.rapidapi.com/prices"

        querystring = {"city_name":p_city,"country_name":"Spain"}

        headers = {
            'x-rapidapi-host': "cost-of-living-and-prices.p.rapidapi.com",
            'x-rapidapi-key': self.rapid_key
            }

        response = requests.get(url, headers= headers, params= querystring).json()

        df = pd.DataFrame.from_dict(response, orient='columns')
        df_cost_of_living = pd.json_normalize(df['prices'])
        df_cost_of_living['Ciudad'] = p_city
        df_cost_of_living['País'] = querystring['country_name']
        df_cost_of_living['update_date']=datetime.now()
        
        return df_cost_of_living



    def get_cities_for_db(self):

        #cities_list= get_all_cities()
        cities_list=['Seville']

        df=pd.DataFrame(columns=['id','name','starRating','neighbourhood','supplierHotelId','ratePlan.price.exactCurrent','guestReviews.rating','address.postalCode','address.locality','address.countryName'])  
        df_city = pd.DataFrame(columns=['good_id', 'item_name', 'category_id', 'category_name', 'min', 'avg', 'max', 'measure', 'currency_code', 'Ciudad', 'País'])
        df_transportes = pd.DataFrame(columns= ['name', 'distance', 'distanceInTime', 'type_transports','hotelId', 'cityname'])

        for city in cities_list:
            try:
                print(city)
                hotels, transportes_to_hotel = self.get_hotel_list(city,1)
                hotels_list = hotels
                transport_listhotels = transportes_to_hotel
                df = pd.concat([hotels_list, df])

                cost_cities = self.cost_of_living_pcity(city)
                df_city = pd.concat([cost_cities, df_city])
                df_transportes = pd.concat([transport_listhotels, df_transportes])

            except: 
                pass
        
        df.to_excel('hotels_list.xlsx', index=False)
        df_city.to_excel('costliving_list.xlsx', index=False)
        df_transportes.to_excel('transportes_hotelsAll.xlsx')

    #hacerlo en un futuro por ciudad del pais desglosado
    def get_covid_data_country(self):
        url = "https://covid-19-statistics.p.rapidapi.com/reports"

        querystring = {'iso': 'ESP',
                        "date":"2020-04-16"}

        headers = {
            'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
            'x-rapidapi-key': self.rapid_key
            }

        response = requests.get(url, headers= headers, params= querystring).json()
        df = pd.json_normalize(response['data'])
        return df 
