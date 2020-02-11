import re

import arrow
import decimal
import datetime
from schema import And, Use, Or, Optional, SchemaError, Schema
from tornado.escape import utf8, to_unicode

schema_unicode_empty = Use(to_unicode, error='请传入合法的字符串')
schema_unicode_upper = And(Use(to_unicode), len, Use(str.upper), error='请传入不为空的字符串')
schema_int = Use(int, error='请传入合法的整数')
schema_date_arrow = Use(arrow.get, error='请传入合法的日期, 如:2017-05-20')
