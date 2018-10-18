import os
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import Role


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.cli.command()
def deploy():
    """Run deployment tasks."""
    print('deploy')
    # migrate database to latest revision
    upgrade()

    # create or update user roles
    Role.insert_roles()


