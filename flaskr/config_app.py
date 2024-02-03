import os

def init_app(app):
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'prod'),
        DEBUG=int(os.environ.get('FLASK_DEBUG', '0')) == 1,
        DATABASE=os.path.join(app.instance_path, os.environ.get('DATABASE','flaskr.sqlite')),
    )
    
    try:
        #Neste ponto é criada a pasta que representa a instancia do app
        os.makedirs(app.instance_path)
    except OSError:
        pass