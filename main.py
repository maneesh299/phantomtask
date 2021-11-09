from flask import Flask
from flask_restful import Resource, Api

# use grequests for asynchronous calls

import grequests

app = Flask(__name__)
api = Api(app)


class phantom(Resource):

    # api is using get method

    def get(self, name):

# urls of both calls in an array and pass the cityname as parameter to url

        urls = ['https://api.openweathermap.org/data/2.5/weather?q=%s'
                % name + '&appid=f998c8a8ccb71a9b6fc4c87ae409970f',
                'https://api.roadgoat.com/api/v2/destinations/auto_complete?q=%s'
                 % name]
        header = \
            {'Authorization': 'Basic YWM4ZWM4MTgyM2RiNzBlMGEzNTQ5OWViMzY3MjYzYmI6YzRkNjNlNTlmMmVkOWI4MTgyYmFiZTQ1ODU2MDczOGI='}

       # get api calls as asynchronous using grequests

        rs = (grequests.get(u, headers=header) for u in urls)
        responses = grequests.map(rs)

       # if any apis return failure return error message

        for response in responses:
            if response.status_code != 200:
                return {'response': 'either api is down or bad input'}
        a = responses[0].json()
        b = responses[1].json()

# pull only the weather entity from the first api call

        weather = a['weather']
        images = b['included'][0]['attributes']['image']

# pull only image entity from json in the response of second api call. This can be improved for error handling by checking if the images are empty
# aggregate responses as json

        return {'weather': weather, 'image': images}


# pass the cityname as input from the url

api.add_resource(phantom, '/cityName/<string:name>')

# debug true only for dev purpose and run the web server

if __name__ == '__main__':
    app.run(debug=True)
