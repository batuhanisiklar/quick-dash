from app import db, User, app
from werkzeug.security import generate_password_hash

with app.app_context():
    User.query.delete()
    db.session.commit()

    db.create_all()

    # Admin kullanıcıları oluştur
    admin1 = User(
        name='Batuhan',
        surname='Isiklar',
        email='admin1@admin.com',
        password=generate_password_hash('admin'),
        is_admin=True,
        is_online=False
    )

    admin2 = User(
        name='Ahmet',
        surname='Yilmaz',
        email='admin2@admin.com',
        password=generate_password_hash('admin'),
        is_admin=True,
        is_online=False
    )

    admin3 = User(
        name='Mehmet',
        surname='Demir',
        email='admin3@admin.com',
        password=generate_password_hash('admin'),
        is_admin=True,
        is_online=False
    )

    # Normal kullanıcıları oluştur
    user1 = User(
        name='Cemre',
        surname='Hallacoglu',
        email='user1@user.com',
        password=generate_password_hash('password'),
        is_admin=False,
        is_online=False
    )

    user2 = User(
        name='Ayse',
        surname='Kaya',
        email='user2@user.com',
        password=generate_password_hash('password'),
        is_admin=False,
        is_online=False
    )

    user3 = User(
        name='Fatma',
        surname='Celik',
        email='user3@user.com',
        password=generate_password_hash('password'),
        is_admin=False,
        is_online=False
    )

    user4 = User(
        name='Ali',
        surname='Ozturk',
        email='user4@user.com',
        password=generate_password_hash('password'),
        is_admin=False,
        is_online=False
    )

    user5 = User(
        name='Zeynep',
        surname='Sahin',
        email='user5@user.com',
        password=generate_password_hash('password'),
        is_admin=False,
        is_online=False
    )

    user6 = User(
        name='Merve',
        surname='Arslan',
        email='user6@user.com',
        password=generate_password_hash('password'),
        is_admin=False,
        is_online=False
    )

    user7 = User(
        name='Emre',
        surname='Yildiz',
        email='user7@user.com',
        password=generate_password_hash('password'),
        is_admin=False,
        is_online=False
    )

    # Kullanıcıları veritabanına ekle
    db.session.add(admin1)
    db.session.add(admin2)
    db.session.add(admin3)
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)
    db.session.add(user6)
    db.session.add(user7)
    db.session.commit()