from flask import (
    render_template,
    request,
    session,
    redirect, 
    url_for,
    flash
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
import os

def configure_routes(app):
    
    @app.route('/')
    def index():
        if 'user_id' in session.keys():
            return render_template(
                'index.html', 
                title_header=os.environ.get('TITLE_HEADER','E-Commerce-Example'),
                title_body=os.environ.get('TITLE_BODY','E-Commerce-Example'),
                copyright_organization=os.environ.get('COPYRIGHT_ORGANIZATION','Your Organization'),
                copyright_year=os.environ.get('COPYRIGHT_YEAR', 2024)    
            )
        return redirect(url_for("login"))
    
    @app.route('/login/', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template(
                'auth/login.html',
                title_body=os.environ.get('TITLE_BODY','E-Commerce-Example'),
                copyright_year=os.environ.get('COPYRIGHT_YEAR', 2024)    
            )    
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            db = get_db()
            error = None
            user = db.execute(
                'SELECT * from user WHERE username = ?',
                (username,)
            ).fetchone()
            if user is None:
                error = 'Username incorreto'
            elif not check_password_hash(user['password'], password):
                error = 'Incorrect password.'
            if error is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))
            flash(error)
        return render_template(
            'auth/register.html',
            title_body=os.environ.get('TITLE_BODY','E-Commerce-Example'),
            copyright_year=os.environ.get('COPYRIGHT_YEAR', 2024)    
        )
    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))
    
    @app.route('/register/', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            db = get_db()
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'

            if error is None:
                try:
                    db.execute(
                        "INSERT INTO user (username, password) VALUES (?, ?)",
                        (username, generate_password_hash(password)),
                    )
                    db.commit()
                except db.IntegrityError:
                    error = f"User {username} is already registered."
                else:
                    return redirect(url_for("login"))

            flash(error)
        return render_template('auth/register.html')
    return app