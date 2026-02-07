# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Bug, User, BugReport

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # สำหรับ session

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    sort_by = request.args.get('sort', 'severity')  # default เรียงตามความรุนแรง
    
    if sort_by == 'reports':
        # เรียงตามจำนวนรายงาน (มาก -> น้อย)
        from sqlalchemy import func
        bugs = db.session.query(Bug, func.count(BugReport.id).label('report_count'))\
            .outerjoin(BugReport)\
            .group_by(Bug.id)\
            .order_by(func.count(BugReport.id).desc())\
            .all()
        # แปลงผลลัพธ์
        bugs = [(b[0], b[1]) for b in bugs]
    else:
        # เรียงตามคะแนนความรุนแรง (มาก -> น้อย = ร้ายแรงก่อน)
        bugs = [(b, len(b.bug_reports)) for b in Bug.query.order_by(Bug.severity_score.desc()).all()]
    
    return render_template('index.html', bugs=bugs, sort_by=sort_by)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)
        
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            return redirect(url_for('index'))
        else:
            error = 'ไม่พบผู้ใช้นี้'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/bug/<bug_id>')
def bug_detail(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    reports = BugReport.query.filter_by(bug_id=bug_id).all()
    
    # เช็คใน Controller แทน
    already_reported = False
    if 'user_id' in session:
        already_reported = BugReport.query.filter_by(
            user_id=session['user_id'],
            bug_id=bug_id
        ).first() is not None
    
    return render_template('bug_detail.html', 
                           bug=bug, 
                           reports=reports,
                           already_reported=already_reported)

CRITICAL_THRESHOLD = 3  # จำนวนรายงานที่ทำให้เป็น critical

@app.route('/bug/<bug_id>/report', methods=['POST'])
def report_bug(bug_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    bug = Bug.query.get_or_404(bug_id)
    
    # ถ้าตรวจสอบแล้ว ไม่ให้รายงาน
    if bug.verified:
        return redirect(url_for('bug_detail', bug_id=bug_id))
    
    # เช็คว่าเคยรายงานแล้วหรือยัง
    existing = BugReport.query.filter_by(
        user_id=session['user_id'],
        bug_id=bug_id
    ).first()
    
    if existing:
        return redirect(url_for('bug_detail', bug_id=bug_id))
    
    report_type = request.form.get('report_type')
    report = BugReport(
        user_id=session['user_id'],
        bug_id=bug_id,
        report_type=report_type
    )
    db.session.add(report)
    
    # เช็คจำนวนรายงาน ถ้าเกิน threshold เปลี่ยนเป็น critical
    report_count = BugReport.query.filter_by(bug_id=bug_id).count()
    if report_count >= CRITICAL_THRESHOLD:
        bug.status = 'critical'
    
    db.session.commit()
    
    return redirect(url_for('bug_detail', bug_id=bug_id))

@app.route('/bug/<bug_id>/verify', methods=['POST'])
def verify_bug(bug_id):
    if 'user_id' not in session or session.get('user_role') != 'developer':
        return redirect(url_for('login'))
    
    bug = Bug.query.get_or_404(bug_id)
    
    # ถ้าตรวจสอบแล้ว ไม่ให้ทำซ้ำ
    if bug.verified:
        return redirect(url_for('bug_detail', bug_id=bug_id))
    
    bug.verification_result = request.form.get('verification_result')  # fixed / won't fix
    bug.verified = True
    db.session.commit()
    
    return redirect(url_for('bug_detail', bug_id=bug_id))

@app.route('/summary')
def summary():
    critical_bugs = Bug.query.filter_by(status='critical').all()
    verified_bugs = Bug.query.filter_by(verified=True).all()
    
    return render_template('summary.html', 
                           critical_bugs=critical_bugs, 
                           verified_bugs=verified_bugs)

if __name__ == '__main__':
    app.run(debug=True)