import os

from invoke import Collection

from . import test

while not os.path.isdir('tasks'):
    os.chdir('..')

ns = Collection()
ns.add_collection(Collection.from_module(test))
