import os
import importlib

import horse.config
import horse.jockey


def run(**kwargs):
    config_path = os.getenv('HORSE_CONFIG_MODULE', None)
    config_module = importlib.import_module(config_path)
    horse.config.__dict__.update(config_module.__dict__)
    jockey = horse.jockey.Jockey()
    jockey.start()
