__author__ = 'christopherfricke'
from models import fields


spatial_fields = {
    'STATION':'STATION',
    'STATION NAME':'STATION NAME',
    'BEGIN':'BEGIN',
    'END':'END',
    'geo':'geo'
}

tabular_fields = {
    'slp_avg':fields.mr_field_avg("sea_level_pressure","slp_count"),
    'stp_avg':fields.mr_field_avg("station_pressure","stp_count"),
    'wind_avg':fields.mr_field_avg("windspeed","wdsp_count"),
    'stp_max':fields.mr_field_max("station_pressure"),
    'dew_avg':fields.mr_field_avg("dewpoint","dewpoint_count"),
    'temp_max':fields.mr_field_max("max_temperature"),
    'temp_min':fields.mr_field_min("min_temperature"),
    'temp_avg':fields.mr_field_avg("avg_temperature","temp_count"),
    'gust_max':fields.mr_field_max("gust"),
    'visib_max':fields.mr_field_max("visibility"),
    'dew_max':fields.mr_field_max("dewpoint"),
    'wind_max':fields.mr_field_max("max_windspeed"),
    'dew_min':fields.mr_field_min("dewpoint"),
    'visib_min':fields.mr_field_min("visibility"),
    'precip_sum':fields.mr_field_sum("total_precipitation"),
    'snow_max':fields.mr_field_sum("snow_depth"),
    }


station_field = 'station'
date_field = 'date'

geo_geo_field = 'geo'
geo_station_field = 'STATION'
geo_start_field = 'BEGIN'
geo_end_field = 'END'
