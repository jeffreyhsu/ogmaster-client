# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="jeffrey"
__date__ ="$Dec 15, 2009 11:49:24 PM$"

import sqlalchemy as sqla
import pytz
import datetime

#class UTCDateTime(sqla.types.TypeDecorator):
#    impl = sqla.types.DateTime
#    def convert_bind_param(self, value, engine):
#        return value
#    def convert_result_value(self, value, engine):
#        return UTC.localize(value)

class PytzDateTime(sqla.types.TypeDecorator):

    impl = sqla.types.DateTime
    def convert_bind_param(self, value, engine):
        f = '%Y-%m-%d %H:%M:%S'
        value = value.astimezone(pytz.UTC)
        return datetime.datetime.now()
#        return "%s|%s" % (value.strftime('%Y-%m-%d %H:%M:%S'), self.timezone.zone)
    
    def convert_result_value(self, value, engine):
        return value
#        v = value.split('|')
#        datetime.datetime.strptime(v[0], '%Y-%m-%d %H:%M:%S')
#        tz = pytz.timezone(v[1])
#        return tz.localize(value)