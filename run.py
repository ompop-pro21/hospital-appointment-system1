from app import create_app, db

app = create_app()

# This is the new part. It creates a special command for our terminal.
@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables from the models."""
    db.create_all()
    print("Initialized the database and created all tables.")

# This part remains the same
if __name__ == '__main__':
    app.run(debug=True)