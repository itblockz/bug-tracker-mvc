# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user')  # user / developer
    
    def __repr__(self):
        return f'<User {self.id}: {self.name}>'


class Bug(db.Model):
    __tablename__ = 'bugs'
    
    id = db.Column(db.String(8), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    source = db.Column(db.String(100), nullable=False)  # ระบบหรือโมดูลที่พบบั๊ก
    created_date = db.Column(db.DateTime, default=datetime.now)
    severity_score = db.Column(db.Integer, default=0)  # คะแนนความรุนแรง
    status = db.Column(db.String(10), default='normal')  # normal / critical
    verified = db.Column(db.Boolean, default=False)
    verification_result = db.Column(db.String(20))  # fixed / won't fix
    
    def __repr__(self):
        return f'<Bug {self.id}: {self.title}>'


class BugReport(db.Model):
    __tablename__ = 'bug_reports'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bug_id = db.Column(db.String(8), db.ForeignKey('bugs.id'), nullable=False)
    report_date = db.Column(db.DateTime, default=datetime.now)
    report_type = db.Column(db.String(20), nullable=False)  # UI Bug / Logic Bug / Performance Bug
    
    # relationships
    user = db.relationship('User', backref='bug_reports')
    bug = db.relationship('Bug', backref='bug_reports')
    
    def __repr__(self):
        return f'<BugReport {self.id}: {self.report_type}>'