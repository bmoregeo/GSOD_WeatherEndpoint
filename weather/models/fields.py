__author__ = 'christopherfricke'

class mr_field():
    prefix = ''

    def __init__(self, value_field, count_field = None):
        self.value_field = value_field
        self.count_field = count_field

    @property
    def fields(self):
        try:
            out =  {
                'value_field': '_'.join([self.prefix, self.value_field]),
                'count_field':'_'.join([self.prefix, self.count_field]),
                'in_count_field':self.count_field,
                'in_value_field': self.value_field
            }
        except TypeError:
            out =  {
                'value_field': '_'.join([self.prefix, self.value_field]),
                'count_field':None,
                'in_count_field':None,
                'in_value_field': self.value_field
            }
        finally:
            return out
    @property
    def mapper(self):
        return ''

    @property
    def reducer_fields(self):
        return ''

    @property
    def reducer(self):
        return ''

    @property
    def finalize(self):
        return ''


class mr_field_max(mr_field):
    prefix = 'max'
    default_value = '-9999.9'

    @property
    def mapper(self):
        return '%(value_field)s:this.%(in_value_field)s' % self.fields

    @property
    def reducer_field(self):
        return ':'.join([self.fields['value_field'], self.default_value])

    @property
    def reducer(self):
        return """
        if ( value.%(value_field)s > result.%(value_field)s ){result.%(value_field)s = value.%(value_field)s;}
        """ % self.fields
    @property
    def finalize(self):
        return """if (reduced_value.%(value_field)s === -9999.9){reduced_value.%(value_field)s = null;}""" % self.fields

class mr_field_min(mr_field):
    prefix = 'min'
    default_value = '9999.9'

    @property
    def mapper(self):
        return 'max_%(value_field)s:this.%(value_field)s' % self.fields

    @property
    def reducer_field(self):
        return ':'.join([self.fields['value_field'], self.default_value])

    @property
    def reducer(self):
        return """
        if ( value.%(value_field)s < result.%(value_field)s ){result.%(value_field)s = value.%(value_field)s;}
        """ % self.fields
    @property
    def finalize(self):
        return """if (reduced_value.%(value_field)s === 9999.9){reduced_value.%(value_field)s = null;}""" % self.fields

class mr_field_sum(mr_field):
    prefix = 'sum'
    default_value = '0'

    @property
    def reducer_field(self):
        try:
            return ','.join([':'.join([self.fields['value_field'], self.default_value]),
                        ':'.join([self.fields['count_field'], self.default_value])])
        except TypeError:
            return ':'.join([self.fields['value_field'], self.default_value])
    @property
    def mapper(self):
        if self.count_field:
            out = """%(value_field)s:this.%(in_value_field)s * this.%(in_count_field)s,
%(count_field)s:this.%(in_count_field)s""" % self.fields
        else:
            out = 'sum_%(value_field)s:this.%(value_field)s' % self.fields
        return out

    @property
    def reducer(self):
        if self.count_field:
            out = """if (value.%(value_field)s && value.%(count_field)s){
                result.%(value_field)s += value.%(value_field)s;
                result.%(count_field)s += value.%(count_field)s;
            }""" % self.fields
        else:
            out = """if (value.%(value_field)s && value.%(count_field)s){
                result.%(value_field)s += value.%(value_field)s;
            }""" % self.fields

        return out

    @property
    def finalize(self):
        pass


class mr_field_avg(mr_field_sum):
    prefix = 'avg'
    default_value = '0'

    @property
    def finalize(self):
        out = """
                if (reduced_value.%(value_field)s && reduced_value.%(count_field)s){
                    reduced_value.%(value_field)s = (reduced_value.%(value_field)s/reduced_value.%(count_field)s);
                }
                else {
                    reduced_value.%(value_field)s = null;
                }
                delete reduced_value.%(count_field)s;

                """ % self.fields
        return out


