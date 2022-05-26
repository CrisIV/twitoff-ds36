from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_or_update_user


def create_app():

    app = Flask(__name__)

    # Tell our app where to find our database
    # "registering" pur database with the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route("/")
    def home():
        # query the database for all the users
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)


    @app.route("/reset")
    def reset():
        # Drop our DB tables
        DB.drop_all()
        # Create tables according to the classes in models.py
        DB.create_all()
        return render_template('base.html', title='Reset DB')

    @app.route('/populate')
    def populate():
        add_or_update_user('nasa')
        add_or_update_user('austen')
        return render_template('base.html', title='Populate')

    @app.route('/update')
    def update():
        usernames = [user.username for user in User.query.all()]
        for username in usernames:
            add_or_update_user(username)
        return render_template('base.html', title='Update')

    return app
