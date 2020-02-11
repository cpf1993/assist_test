# -*- coding: utf-8 -*-

from django.conf import settings


class SupplierMgrRouter(object):
    """
    A router to control all database operations on models in the
    supplier application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read supplier_mgr models go to supplier_mgr.
        """
        # if model._meta.app_label == 'supplier':
        #     return 'supplier_mgr'
        #     # return 'default'
        # return None

        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write supplier_mgr models go to supplier_mgr.
        """
        # if model._meta.app_label == 'supplier':
        #     return 'supplier_mgr'
        #     # return 'default'
        # return None
        if model._meta.app_label in settings.DATABASE_APPS_MAPPING:
            return settings.DATABASE_APPS_MAPPING[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the supplier_mgr app is involved.
        """
        # if obj1._meta.app_label == 'supplier' or \
        #    obj2._meta.app_label == 'supplier':
        #    return True
        # return None
        db1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
        db2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
        if db1 and db2:
            return db1 == db2
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the supplier app only appears in the 'supplier_mgr'
        database.
        """
        # print app_label, db, model, hints
        # if app_label == 'supplier':
        #     return db == 'supplier_mgr'
        #     # return db == 'default'
        # return False
        if db in settings.DATABASE_APPS_MAPPING.values():
            return settings.DATABASE_APPS_MAPPING.get(app_label) == db
        elif app_label in settings.DATABASE_APPS_MAPPING:
            return False
