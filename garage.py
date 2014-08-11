from flask import Flask
from flask.ext import restful

import sensors


app = Flask(__name__)
api = restful.Api(app)


class Garage(restful.Resource):
    def get(self):
        gd = sensors.GarageDoorSensor()
        return {'state': gd.get_state()}


api.add_resource(Garage, '/')

if __name__ == '__main__':
    app.run('0.0.0.0')
