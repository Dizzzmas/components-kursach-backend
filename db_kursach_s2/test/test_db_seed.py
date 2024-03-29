from db_kursach_s2.commands import drop_all_tables
import flask_migrate
from db_kursach_s2.db.fixtures import seed_db
from db_kursach_s2.db import db


def test_db_init_seed(app):
    """Try initializing and seeding development database."""
    drop_all_tables(app=app)
    db.create_all(app=app)
    seed_db()
    drop_all_tables(app=app)


def test_db_migrate_seed():
    """Run migrations and seed."""
    flask_migrate.upgrade()
    seed_db()
