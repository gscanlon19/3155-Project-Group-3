from database import db

class Post(db.Model):
	id = db.Column("id", db.Integer, primary_key = True)
	text = db.Column("text", db.String(100))

	def __init__(self, text):
		self.text