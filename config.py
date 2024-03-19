from flask_session import Session
import os

def config_upload(app):
    UPLOAD_FOLDER=os.path.join(app.root_path,"static/imagens")
    app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def config_session(app):
    app.config["SESSION_PERMANENT"]=False
    app.config["SESSION_TYPE"]="filesystem"
    Session(app)

def config_mail(app):
    app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = '482123c1148de7'
    app.config['MAIL_PASSWORD'] = '62cf064b09525c'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False