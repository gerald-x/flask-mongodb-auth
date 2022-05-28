from main import db, ma
from marshmallow import fields


class User(db.Document):
    email = db.EmailField(required=True)
    first_name = db.StringField(max_length=50, required=True)
    last_name = db.StringField(max_length=50, required=True)
    password = db.StringField(required=True)


class Templates(db.Document):
    user = db.ReferenceField(User, reverse_delete_rule=db.CASCADE)
    name = db.StringField(max_length=120)
    subject = db.StringField()
    body = db.StringField()


class TemplateSchema(ma.Schema):
    id = fields.String()
    class Meta:
        model = Templates
        additional = ("user", "name", "subject", "body")



