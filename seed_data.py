"""
Run this once after creating the database tables to populate demo data:

    python seed_data.py

Creates:
- Your custom host + 2 demo hosts
- 3 resources with different risk levels (to demonstrate policy engine branching)
"""

from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import Host, Resource

app = create_app()

with app.app_context():
    db.create_all()  # creates any tables that don't exist yet

    if Host.query.filter_by(email="sudhanshusinghh99@gmail.com").first() is None:
        my_host = Host(
            name="Sudhanshu Singh",
            email="sudhanshusinghh99@gmail.com",
            password_hash=generate_password_hash("sudh123"),
            department="IT",
        )
        db.session.add(my_host)
        db.session.commit()
        print(f"Created host: id={my_host.id} ({my_host.email})")
    else:
        print("Your host already exists, skipping.")

    if Host.query.filter_by(email="aditi@company.com").first() is None:
        host1 = Host(
            name="Aditi Sharma",
            email="aditi@company.com",
            password_hash=generate_password_hash("password123"),
            department="Engineering",
        )
        host2 = Host(
            name="Rahul Verma",
            email="rahul@company.com",
            password_hash=generate_password_hash("password123"),
            department="Facilities",
        )
        db.session.add_all([host1, host2])
        db.session.commit()
        print(f"Created hosts: id={host1.id} ({host1.email}), id={host2.id} ({host2.email})")
    else:
        print("Demo hosts already exist, skipping.")

    if Resource.query.first() is None:
        lobby = Resource(name="Main Lobby", location="Ground Floor", risk_level="low")
        meeting_room = Resource(name="Conference Room A", location="1st Floor", risk_level="low")
        server_room = Resource(name="Server Room", location="Basement", risk_level="high")
        db.session.add_all([lobby, meeting_room, server_room])
        db.session.commit()
        print(f"Created resources: "
              f"id={lobby.id} ({lobby.name}, {lobby.risk_level}), "
              f"id={meeting_room.id} ({meeting_room.name}, {meeting_room.risk_level}), "
              f"id={server_room.id} ({server_room.name}, {server_room.risk_level})")
    else:
        print("Resources already exist, skipping.")

    print("\nYour login -> email: sudhanshusinghh99@gmail.com | password: sudh123")
    print("Demo login -> email: aditi@company.com | password: password123")
    print("Use the printed resource IDs above when registering a visit.")