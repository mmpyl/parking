#!/usr/bin/env python3
from lib.database import db
from app.models.postgres_models import UserModel
print('Creating tables...')
UserModel.create_table()
print('Done.')