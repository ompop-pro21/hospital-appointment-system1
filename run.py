from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

# This is the new, smart command for the one-time setup.
@app.cli.command("seed-db")
def seed_db_command():
    """Creates database tables and the first admin user."""
    # Create all tables
    db.create_all()
    print("Initialized the database and created all tables.")

    # Check if the admin user already exists
    if User.query.filter_by(email='admin@gmail.com').first():
        print("Admin user already exists. Skipping creation.")
    else:
        # Create the admin user
        hashed_password = generate_password_hash('admin', method='pbkdf2:sha256')
        admin = User(
            username='ADMIN',
            email='admin@gmail.com',
            password_hash=hashed_password,
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Successfully created the first admin user.")


if __name__ == '__main__':
    app.run(debug=True)
