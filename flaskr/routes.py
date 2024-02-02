from flask import render_template

def configure_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html', title_page='E-Commerce-Example')
    
    @app.route('/login/')
    def login():
        return render_template('auth/login.html')
    
    @app.route('/logout')
    def logout():
        return 'Logout'
    
    @app.route('/register/')
    def register():
        return render_template('auth/register.html')
    return app