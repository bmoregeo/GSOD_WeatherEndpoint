__author__ = 'christopherfricke'
import localsettings
import settings

import utilities
import pprint
import build_mr
from bson import json_util

import json

pp = pprint.PrettyPrinter(indent=4)




if __name__ == '__main__':


    query_features = utilities.query(key,
                                     key_type,
                                     extent,
                                     start_date,
                                     end_date)

    features = {'type':'FeatureCollection',
                'features':query_features}

    with open ('/Users/christopherfricke/Sites/stations.json', 'w') as stations:
        stations.write(json.dumps(features, default=json_util.default))

