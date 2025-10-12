from app import create_app, db
from app.models import User
import secrets # Import the secrets library

app = create_app()

@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables from the models."""
    db.create_all()
    print("Initialized the database and created all tables.")

# --- THIS IS OUR NEW, TEMPORARY, SECRET ROUTE ---
# We generate a long, random, secret string to make the URL hard to guess.
# IMPORTANT: This secret will change every time the server restarts.
SECRET_SETUP_KEY = secrets.token_hex(16)

@app.route(f"/setup/promote-first-admin/{SECRET_SETUP_KEY}")
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
        return "<h1>Error</h1><p>No users found in the database. Please register the first user and then restart the server to try again.</p>"


if __name__ == '__main__':
    app.run(debug=True)
```
3.  **Save the file.**

#### Step 2: Push This Final Change to GitHub

Now, send this updated code to GitHub. This will trigger a new deployment on Render.

1.  In your VS Code terminal, run these commands:
    ```bash
    git add .
    git commit -m "feat: Add temporary secret route to create first admin"
    git push
    ```

#### Step 3: The One-Time Action on the Live Site

This is the final sequence. You must do these steps in order.

1.  **Wait for the Deployment to Finish:** Go to the Render logs and wait until you see the `Your service is live` message. This deployment will create a new, clean, empty database.

2.  **Register Your Admin User (Again):**
    * Go to your live website's registration page:
        **[https://hospital-appointment-system1-rdqx.onrender.com/register](https://hospital-appointment-system1-rdqx.onrender.com/register)**
    * Create your admin account (e.g., `admin@gmail.com`). This is now the *first and only user* in the database.

3.  **Find and Visit Your Secret URL:**
    * Now, go to the **Logs** on your Render dashboard.
    * Because your server has just restarted, it has generated a new secret key. You need to find it in the logs. Look for a line that starts with `[INFO]`. It will show your server starting up. **The secret URL is not printed directly.** *This was a mistake in my plan.*

    **Let's pivot to a simpler, hardcoded secret for this one-time use.**

    **CORRECTION - PLEASE UPDATE `run.py` ONE LAST TIME WITH THIS:**

```python
# ... (imports are the same)
app = create_app()
# ... (init-db is the same)

# --- CORRECTED SECRET ROUTE ---
@app.route("/setup/promote-first-admin/make-me-admin-now-12345")
def promote_first_admin():
    # ... (the rest of the function is the same as above)
    user = User.query.first()
    if user:
        user.role = 'admin'
        db.session.commit()
        return f"<h1>Success!</h1><p>User '{user.username}' has been promoted. Please remove this route from run.py now.</p>"
    else:
        return "<h1>Error</h1><p>No user found. Please register first.</p>"

# ... (if __name__ == '__main__': ... is the same)

