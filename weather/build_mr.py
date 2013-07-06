__author__ = 'christopherfricke'
from bson.code import Code
import settings


class map_reduce():
    def __init__(self, key, key_type, fields):
        self.fields = []
        for field in fields:
            try:
                self.fields.append(settings.tabular_fields[field])
            except KeyError:
                pass


        self.key = key
        self.key_type = key_type
        self._query = {}

    @property
    def mapper(self):
        row = ','.join([field.mapper for field in self.fields if field.mapper])

        if self.key_type == 'date':
            more = """var key = new Date(this.date.getFullYear(), this.date.getMonth(), this.date.getDate());"""
            map_key = 'key'
        elif self.key_type == 'date_month':
            more = """var key = new Date(this.date.getFullYear(), this.date.getMonth());"""
            map_key = 'key'
        elif self.key_type == 'date_year':
            more = """var key = this.date.getFullYear();"""
            map_key = 'key'
        else:
            more = ''
            map_key = 'this.%s' % self.key


        return Code("""function() {
            %s
            var row = {%s};
            row.count = 1;
            emit(%s, row);
        }""" % (more, row, map_key))

    @property
    def reducer(self):
        out = Code("""
        function(key, values) {
            var result = {%s};
            result.count = 0;
            values.forEach(function(value){
                if (value.count){result.count += value.count;}
                %s
            });
            return result;
        }
        """ % ( ','.join([field.reducer_field for field in self.fields if field.reducer_field]),
                ''.join([field.reducer for field in self.fields if field.reducer])
        )

        )

        return out

    @property
    def finalize(self):
        return Code("""function(key, reduced_value){
            %s
            return reduced_value
            }""" % ''.join([field.finalize for field in self.fields if field.finalize]))

