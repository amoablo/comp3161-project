from flask_login import UserMixin

class User(UserMixin):
    # Using UserMixin instead of db.Model

    def __init__(self, user_id, first_name, last_name, email, gender, password):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.user_id)  # python 2 support
        except NameError:
            return str(self.user_id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.email)