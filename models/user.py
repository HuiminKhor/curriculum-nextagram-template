from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(UserMixin,BaseModel):
    name = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    profileimg = pw.CharField(default='hello.jpg')

    def follow(self, user):
        from models.follow import Follow
        if self.id != user.id and self.is_following(user) == False and self.is_requesting(user) == False:
            follow = Follow(follower_id = self.id, followed_id = user.id)
            follow.save()
        else:
            return 0    


    def approve(self, user):
        from models.follow import Follow    
        if user.is_requesting(self):
            Follow.update(approved = True).where(Follow.followed_id == self.id, Follow.follower_id == user.id).execute() 
        else:
            return 0    

    def is_following(self, user):
        from models.follow import Follow    
        result = Follow.select().where(Follow.follower_id == self.id, Follow.followed_id == user.id, Follow.approved == True)
        if len(result) > 0:
            return True
        else:
            return False

    def is_requesting(self, user):
        from models.follow import Follow    
        result = Follow.select().where(Follow.follower_id == self.id, Follow.followed_id == user.id, Follow.approved == False)
        if len(result) > 0:
            return True
        else:
            return False

    def get_requests(self):
        from models.follow import Follow    
        result = User.select().join(Follow, on=(Follow.follower_id == User.id)).where(Follow.followed_id == self.id, Follow.approved == False)
        return result

    def get_followers(self):
        from models.follow import Follow    
        result = User.select().join(Follow, on=(Follow.follower_id == User.id)).where(Follow.followed_id == self.id, Follow.approved == True)
        return result


    def get_requesting(self):
        from models.follow import Follow    
        result = User.select().join(Follow, on=(Follow.followed_id == User.id)).where(Follow.follower_id == self.id, Follow.approved == False)
        return result        

    
    def get_following(self):
        from models.follow import Follow    
        result = User.select().join(Follow, on=(Follow.followed_id == User.id)).where(Follow.follower_id == self.id, Follow.approved == True)
        return result

    def unfollow(self, user):
        from models.follow import Follow    
        if self.is_following(user):
            Follow.delete().where(Follow.follower_id == self.id, Follow.followed_id == user.id, Follow.approved == True).execute()
        else:
            return 0 

    def cancel_request(self, user):
        from models.follow import Follow    
        if self.is_requesting(user):
            Follow.delete().where(Follow.follower_id == self.id, Follow.followed_id == user.id, Follow.approved == False).execute()
        else: 
            return 0
            

    def reject(self, user):
        from models.follow import Follow    
        if user.is_requesting(self):
            Follow.delete().where(Follow.followed_id == self.id, Follow.follower_id == user.id, Follow.approved == False).execute()
        else:
            return 0

    def validate(self):
          
        # check if username is valid
        username_is_taken = User.get_or_none(User.name == self.name)

        if username_is_taken != None:
            self.errors.append('Username is taken')

        # check if email is valid
        email_is_taken = User.get_or_none(User.email == self.email)

        if email_is_taken != None:
            self.errors.append('Email is invalid')

        # check if password is long enough

        if len(self.password) < 6:
            self.errors.append('Password too short')
        
        self.password = generate_password_hash(self.password)

    def validate_update(self):
        self.errors=[]

        if self.newname != self.name:
            username_is_taken = User.get_or_none(User.name == self.newname)

            if username_is_taken != None:
                self.errors.append('Username is taken')

        if self.newemail != self.email:
            email_is_taken = User.get_or_none(User.email == self.newemail)

            if email_is_taken != None:
                self.errors.append('Email is invalid')




             

          




    #     duplicate_username = User.get_or_none(User.username==self.username)
    #     password_regex = 

    #     if duplicate_username:
    #         self.errors.append("username not unique")
    #     if re.search(password_regex,self.password) == None:
    #         self.errors.append("Minimum eight characters, at least one uppercase letter")  
    #     else :
    #         self.password = generate_password_hash(self.password)      
