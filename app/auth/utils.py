from flask import current_app
from app.auth.methods.Authentificator import Authentificator
import importlib


def get_auth_instance():
    auth_methods_module = importlib.import_module("app.auth.methods."+current_app.config["AUTH_METHOD"])
    auth_method = getattr(auth_methods_module, current_app.config["AUTH_METHOD"])

    auth_method = Authentificator(auth_method)
    return auth_method.get_instance()