"""Utility function for loading settings"""
import configparser
import os


def load_settings():
    cfg = configparser.ConfigParser()
    cfg.read('settings.ini')
    cfg = cfg['DEFAULT']
    for nm in list(cfg.keys()):
        if os.environ.get(nm):
            cfg[nm] = os.environ[nm]
    return cfg
