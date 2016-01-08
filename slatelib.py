#!/usr/bin/python
from datetime import datetime as dt
import json
from urllib2 import urlopen as http

class slate:
    def get(self, query, url, **kwargs):
        if ':' in query:
            raise TypeError('Query must be single key only!')
        else:
            q = url + 'get/' + query
            try:
                return str(http(q).read()).strip('\n')
            except Exception as (e):
                raise IOError('Unable to reach SlateKV URL. Err:'  + str(e))

    def post(self, query, url, **kwargs):
        if len(query.split(':')) != 2:
            raise TypeError('Object must be key:value! Not enough or too many key:value pairs submitted')
        else:
            q = url + 'post/' + query
            try:
                return str(http(q).read()).strip('\n')
            except Exception as (e):
                raise IOError('Unable to reach SlateKV URL. Err:'  + str(e))

    def change(self, query, url, **kwargs):
        if len(query.split(':')) != 2:
            raise TypeError('Object must be key:value! Not enough or too many key:value pairs submitted')
        else:
            q = url + 'change/' + query
            try:
                return str(http(q).read()).strip('\n')
            except Exception as (e):
                raise IOError('Unable to reach SlateKV URL. Err:'  + str(e))
