import importlib
import os

__all__ = []

for f in os.listdir(os.path.dirname(__file__)):
    if f == os.path.basename(__file__):
        continue

    module_name = f.split('.')[0]
    importlib.import_module('ptydash.cards.' + module_name)
    __all__.append(module_name)
