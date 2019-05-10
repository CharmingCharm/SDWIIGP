from werkzeug.security import generate_password_hash, check_password_hash
from app.extension import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    uid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_name = db.Column(db.String(64), nullable = False, unique = True)
    password_hash = db.Column(db.String(256), nullable = False)
    is_teacher = db.Column(db.Boolean(), nullable = False, default = False)
	
    def __repr__(self):
        return self.name
	
    # Flask-Login需要
    @property
    def id(self):
        return self.uid
    
    @property
    def password(self):
        raise AttributeError('密码不可读')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    @property
    def position(self):
        return 'Teacher' if self.is_teacher else 'Student'
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
