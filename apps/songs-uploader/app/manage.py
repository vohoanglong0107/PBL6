from flask_migrate import Migrate

from .app import app
from .db import db

# to let alembic recognize models
from .models import Song


migrate = Migrate(app, db)
