from flask import Flask
from flask.ext.jsonpify import jsonify
import weather.utilities
from flask import request
import datetime
app = Flask(__name__)
from weather import settings

key_type_lookup = {
    'station':'text',
    'date':'date',
    }

@app.route('/weather', methods=['GET'])
def request_weather():
    try:
        key = request.args['key']
    except TypeError:
        key = 'station'
    except KeyError:
        key = 'station'

    try:
        key_type = key_type_lookup[key]
    except KeyError:
        key_type = 'text'


    try:
        start_date = datetime.datetime.strptime(request.args['start_date'], '%Y-%m-%d')
    except TypeError:
        start_date = None
    except KeyError:
        start_date = None
    try:
        end_date = datetime.datetime.strptime(request.args['end_date'], '%Y-%m-%d')
    except TypeError:
        end_date = None
    except KeyError:
        end_date = None



    query_fields = [request.args[field] for field in request.args if field.startswith('fields')]
    try:
        extent = {
            "type" : request.args['extent[type]'],
            "coordinates": [
                [
                    [
                        float(request.args['extent[coordinates][%s][X]' % x]),
                        float(request.args['extent[coordinates][%s][Y]' % x])
                    ]
                    for x in range(0,5)
                ]
            ]
        }
    except KeyError, e:
        raise KeyError(e)

    query_features = weather.utilities.query(key,
                                     key_type,
                                     extent,
                                     start_date,
                                     end_date,
                                     output_fields=query_fields)

    if settings.geo_geo_field in query_fields:
        return jsonify(type='FeatureCollection',features=query_features)
    else:
        return jsonify(type='RecordCollection',records=query_features)


if __name__ == '__main__':
    app.debug = True
    app.run()
