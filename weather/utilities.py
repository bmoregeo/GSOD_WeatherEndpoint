__author__ = 'christopherfricke'
import datetime
from pymongo import MongoClient
import localsettings
import settings
import build_mr

def connect(uri, database_name, collection_name, port=27017):
    client = MongoClient(uri, port)
    collection = client[database_name][collection_name]
    return collection


def build_date_query(start_date, end_date):
    if start_date or end_date:
        query = {}
        if start_date:
            query['$gte'] = start_date
        if end_date:
            query['$lte'] = end_date
    else:
        raise ValueError('Start and End Dates are not populated!')

    return query

def build_query(station_field, station_list, date_field, start_date, end_date):
    query = {}
    # Start / End Date
    try:
        date_query = build_date_query(start_date, end_date)
    except ValueError, e:
        print e
        date_query = None
    if date_query:
        query[date_field] = date_query

    # Station Listin
    if station_list:
        query[station_field] = {'$in': station_list}

    return query

def spatial_query(extent, start_date, end_date, fields):

    output = {}
    spatial_collection = connect(localsettings.uri,
                                           localsettings.database_name,
                                           localsettings.location_name,
                                           localsettings.port)
    # Define spatial extent
    if extent:
        q = {settings.geo_geo_field: {'$geoIntersects':{"$geometry" : extent}}}
    else:
        q = {}

    try:
        if start_date or end_date:
            q[settings.geo_start_field] = build_date_query(start_date, end_date)
            q[settings.geo_end_field] = build_date_query(start_date, end_date)
    except ValueError:
        pass

    # Define fields to pull
    query_fields = {}
    for field in fields:
        try:
            query_fields[settings.spatial_fields[field]] = 1
        except KeyError:
            pass

    # Execute query
    spatial_results = spatial_collection.find(q, query_fields)



    for result in spatial_results:
        try:
            output[result[settings.geo_station_field]] = {
                'geometry':result[settings.geo_geo_field],
                'properties':dict(((field.lower(), result[field]) for field in query_fields)),
                'type':'Feature'
            }
        except KeyError:
            output[result[settings.geo_station_field]] = {
                'properties':dict(((field.lower(), result[field]) for field in query_fields)),
                'type':'Record'
            }
    return output


def query(key, key_type, extent=None, start_date=None, end_date=None, station_ids=None, output_fields = None):
    output = {}
    tabular_collection = connect(localsettings.uri,
                                           localsettings.database_name,
                                           localsettings.collection_name,
                                           localsettings.port)


    if extent:
        output = spatial_query(extent, start_date, end_date, output_fields)
        #print 'Spatially Selected', len(output.keys())
        station_ids = output.keys()


    q = build_query(settings.station_field,
                              station_ids,
                              settings.date_field,
                              start_date,
                              end_date)


    m = build_mr.map_reduce(key,
                            key_type,
                            output_fields)

    #print m.mapper

    table_results = tabular_collection.inline_map_reduce(m.mapper,
                                                         m.reducer,
                                                         finalize = m.finalize,
                                                         query=q)
    for result in table_results:
        for field, value in result['value'].items():
            output[result['_id']]['properties'][field] = value

    return output.values()