from models.base_model import BaseModel
import peewee as pw
from models.user import User
import os

class Image(BaseModel):
    filename = pw.CharField(null=True)
    user = pw.ForeignKeyField(User, backref="images")

    def get_url(self):
        return os.getenv('AWS_DOMAIN') + self.filename
    
    def say_hello(self):
        print(f'hello my filename is {self.filename}')