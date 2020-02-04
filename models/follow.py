from models.base_model import BaseModel
import peewee as pw
from models.user import User


class Follow(BaseModel):
    follower = pw.ForeignKeyField(User, backref='follows')
    followed = pw.ForeignKeyField(User, backref='requests')
    approved = pw.BooleanField(default=False)