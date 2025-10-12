from app import create_app, db
from app.models import User

app = create_app()

@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables from the models."""
    db.create_all()
    print("Initialized the database and created all tables.")

# --- This temporary, secret route is CRITICAL for this final step ---
@app.route("/setup/promote-first-admin/make-me-admin-now-12345")
def promote_first_admin():
    """Finds the first registered user and promotes them to admin."""
    # Find the very first user in the database
    user = User.query.first()
    if user:
        user.role = 'admin'
        db.session.commit()
        print(f"--- SECRET URL VISITED: User '{user.username}' promoted to admin. ---")
        return f"<h1>Success!</h1><p>User '{user.username}' has been promoted to admin. You can now log in. Please remove this setup route from your run.py file now for security.</p>"
    else:
        print("--- SECRET URL VISITED: No user found to promote. ---")
        return "<h1>Error</h1><p>No users found in the database. Please register the first user first.</p>"


if __name__ == '__main__':
    app.run(debug=True)
