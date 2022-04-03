import json

class MongoDB_Push:

    def __init__(self, cliente):
        self.cliente = cliente
    
    
    def mongodb_pushdata_db(self):
        cliente = self.cliente
        db = cliente['mongodbhotels']
        weather_col = db['weather_conditions2']
        hotels_col = db['hotels']
        costliving_col = db['cost_living']
        covid_col = db['covid_data']

        with open(r'\Users\Alberto\OneDrive\Escritorio\flutter_ebook\flask-jsonapi\data\current_conditions.json') as weather_file:
            weather_data = json.load(weather_file)

        with open(r'\Users\Alberto\OneDrive\Escritorio\flutter_ebook\flask-jsonapi\data\cost_living.json') as costliving_file:
            costliving_data = json.load(costliving_file)

        with open(r'\Users\Alberto\OneDrive\Escritorio\flutter_ebook\flask-jsonapi\data\covid_data.json') as covid_file:
            covid_data = json.load(covid_file)

        with open(r'\Users\Alberto\OneDrive\Escritorio\flutter_ebook\flask-jsonapi\data\hotels_and_transports.json') as hotels_file:
            hotels_data = json.load(hotels_file)


        weather_col.insert_many(weather_data)
        hotels_col.insert_many(hotels_data)
        costliving_col.insert_many(costliving_data)
        covid_col.insert_many(covid_data)






