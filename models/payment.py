from models.base_model import BaseModel
import peewee as pw
from models.user import User
from models.image import Image

class Payment(BaseModel):
    amount = pw.CharField()
    user = pw.ForeignKeyField(User, backref="payments")
    image = pw.ForeignKeyField(Image, backref="payments")