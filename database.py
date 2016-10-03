from google.appengine.ext import db

class User(db.Model):
	full_name = db.StringProperty(required=True)
	user_name = db.StringProperty(required=True)
	password = db.StringProperty(required=True)
	win = db.IntegerProperty(required=True)
	lose = db.IntegerProperty(required=True)
	draw = db.IntegerProperty(required=True)

