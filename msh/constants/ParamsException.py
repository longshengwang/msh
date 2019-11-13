# -*- coding:utf8 -*-
class ParamsException(Exception):
    def __init__(self, value):
        self.msg = value