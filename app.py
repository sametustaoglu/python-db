# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL veritabanı bağlantısı için yapılandırma
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://adminuser:Passwd123@dbserver.postgres.database.azure.com:5432/mydb'
# postgres://adminuser:{your_password}@dbserver.postgres.database.azure.com/postgres?sslmode=require
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name

# Veritabanını başlatan fonksiyon
def init_db():
    with app.app_context():
        db.create_all()
        print("Veritabanı başarıyla oluşturuldu.")

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/users')
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append(user.name)
    return ', '.join(result)

@app.route('/add_user/<name>')
def add_user(name):
    new_user = User(name)
    db.session.add(new_user)
    db.session.commit()
    return 'User added successfully: {}'.format(name)

if __name__ == '__main__':
    # Veritabanını başlatma
    init_db()

    # Flask uygulamasını çalıştırma
    app.run()
