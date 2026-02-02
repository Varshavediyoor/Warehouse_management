# whm_project/db_router.py
import threading
from django.conf import settings

_company = threading.local()

def set_company(code):
    """
    Set the current company code for the request thread.
    """
    if code in settings.DATABASES:
        _company.value = code
    else:
        _company.value = "default"

def get_company():
    """
    Get the current company code; default if not set.
    """
    return getattr(_company, "value", "default")


class CompanyDBRouter:
    """
    Routes database operations based on the current company.
    Ensures that sessions always use the default DB.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "sessions":
            return "default"
        db = get_company()
        print(f"[DBRouter] Reading {model} from database: {db}")
        return db

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "sessions":
            return "default"
        db = get_company()
        print(f"[DBRouter] Writing {model} to database: {db}")
        return db

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "sessions":
            return db == "default"
        return True