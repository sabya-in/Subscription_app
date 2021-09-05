import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document):
    phone_no    =   db.IntField( unique=True )
    first_name  =   db.StringField( max_length=50 )
    last_name   =   db.StringField( max_length=50 )
    email       =   db.StringField( max_length=30, unique=True )
    details     =   db.StringField( max_length=600 )
    password    =   db.StringField( )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        return 'complete'
        

class Job(db.Document):
    jobID       =   db.StringField( max_length=10, unique=True )
    title       =   db.StringField( max_length=100 )
    description =   db.StringField( max_length=255 )
    ctc         =   db.IntField()
    job_poster  =   db.StringField( max_length=25 )