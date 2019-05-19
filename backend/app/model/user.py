from werkzeug.security import generate_password_hash, check_password_hash
from app.extension import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    uid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_name = db.Column(db.String(64), nullable = False, unique = True)
    password_hash = db.Column(db.String(256), nullable = False)
    is_teacher = db.Column(db.Boolean(), nullable = False, default = False)
    avatar = db.Column(db.String(256), nullable = False, server_default = 'default.jpg')
    item_per_page = db.Column(db.Integer, nullable = False, server_default = '20')
	
    def __repr__(self):
        return self.name
	
    @property
    def id(self):
        return self.uid
    
    @property
    def password(self):
        raise AttributeError('Password is unreadble')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    @property
    def position(self):
        return 'Teacher' if self.is_teacher else 'Student'
    
    @position.setter
    def position(self, pos):
        if type(pos) == bool:
            self.is_teacher = pos
        else:
            self.is_teacher = pos == 'Teacher'
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
