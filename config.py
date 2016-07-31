WTF_CSRF_ENABLED = True
SECRET_KEY = '_s1=ut&^%2d)1^$p-$s4-sh1^*-@x8a446p@5e9gc^s@68rjs1'

import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
