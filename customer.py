from app import db, ma


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    created_at = db.Column(db.String(100))
    modified_at = db.Column(db.String(100))
    num_orders = db.Column(db.Float)

    def __init__(self, username, password, email, first_name, last_name, address, phone, created_at, modified_at, num_orders):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.created_at = created_at
        self.modified_at = modified_at
        self.num_orders = num_orders

# Customer Schema


class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name',
                  'address', 'phone', 'created_at', 'modified_at', 'num_orders')
