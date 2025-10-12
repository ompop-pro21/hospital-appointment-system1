from app import create_app, db
from app.models import User

app = create_app()

# This is our existing command to create the tables
@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables from the models."""
    db.create_all()
    print("Initialized the database and created all tables.")

# --- THIS IS OUR NEW, ONE-TIME-USE COMMAND ---
@app.cli.command("create-first-admin")
def create_first_admin():
    """Creates the very first admin user."""
    # IMPORTANT: Use the exact email you registered on the live site
    admin_email = 'admin@gmail.com'
    user = User.query.filter_by(email=admin_email).first()
    if user:
        user.role = 'admin'
        db.session.commit()
        print(f"Success! User '{user.username}' at {admin_email} has been promoted to admin.")
    else:
        print(f"Error: Could not find a user with the email {admin_email}. Please register the user first.")

# This part remains the same
if __name__ == '__main__':
    app.run(debug=True)