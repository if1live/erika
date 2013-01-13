#-*- coding: utf-8 -*-

class BaseController(object):
    pass

def register_controller(model_cls, controller_cls):
    model_cls.C = controller_cls
    controller_cls.M = model_cls
