# seed.py
from app import app
from models import db, Bug, User, BugReport

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # เพิ่ม Users (>= 10 คน)
    users = [
        User(name='สมชาย', role='user'),
        User(name='สมหญิง', role='user'),
        User(name='สมศักดิ์', role='user'),
        User(name='สมศรี', role='user'),
        User(name='สมปอง', role='user'),
        User(name='สมใจ', role='user'),
        User(name='สมหมาย', role='user'),
        User(name='สมพร', role='user'),
        User(name='สมบัติ', role='user'),
        User(name='นักพัฒนา', role='developer'),
    ]
    db.session.add_all(users)
    
    # เพิ่ม Bugs (>= 8 รายการ, มีทั้ง critical และ normal)
    bugs = [
        # บั๊ก normal
        Bug(id='10000001', title='ปุ่ม Login ไม่ตอบสนอง', source='Auth Module', severity_score=30, status='normal'),
        Bug(id='10000002', title='หน้าแสดงผลช้าเกินไป', source='Dashboard', severity_score=40, status='normal'),
        Bug(id='10000003', title='ภาษาไทยแสดงผิดพลาด', source='Report Module', severity_score=25, status='normal'),
        Bug(id='10000004', title='Tooltip ไม่แสดง', source='UI Components', severity_score=20, status='normal'),
        # บั๊ก critical
        Bug(id='20000001', title='ระบบล่มเมื่อ Upload ไฟล์ใหญ่', source='File Upload', severity_score=90, status='critical'),
        Bug(id='20000002', title='ข้อมูลหายเมื่อกด Save', source='Database', severity_score=95, status='critical'),
        Bug(id='20000003', title='Session หมดอายุบ่อยเกินไป', source='Auth Module', severity_score=85, status='critical'),
        Bug(id='20000004', title='API Timeout ตลอดเวลา', source='Backend API', severity_score=88, status='critical'),
    ]
    db.session.add_all(bugs)
    db.session.commit()
    
    # เพิ่ม BugReports สำหรับบั๊ก critical (>= 3 รายงาน)
    reports = [
        # บั๊ก 20000001 - 3 รายงาน
        BugReport(user_id=1, bug_id='20000001', report_type='Performance Bug'),
        BugReport(user_id=2, bug_id='20000001', report_type='Logic Bug'),
        BugReport(user_id=3, bug_id='20000001', report_type='UI Bug'),
        # บั๊ก 20000002 - 4 รายงาน
        BugReport(user_id=1, bug_id='20000002', report_type='Logic Bug'),
        BugReport(user_id=2, bug_id='20000002', report_type='Logic Bug'),
        BugReport(user_id=3, bug_id='20000002', report_type='Performance Bug'),
        BugReport(user_id=4, bug_id='20000002', report_type='Logic Bug'),
        # บั๊ก 20000003 - 3 รายงาน
        BugReport(user_id=5, bug_id='20000003', report_type='Logic Bug'),
        BugReport(user_id=6, bug_id='20000003', report_type='Performance Bug'),
        BugReport(user_id=7, bug_id='20000003', report_type='UI Bug'),
        # บั๊ก 20000004 - 3 รายงาน
        BugReport(user_id=8, bug_id='20000004', report_type='Performance Bug'),
        BugReport(user_id=9, bug_id='20000004', report_type='Logic Bug'),
        BugReport(user_id=1, bug_id='20000004', report_type='Performance Bug'),
        # บั๊ก normal - 1-2 รายงาน (ไม่ถึง critical)
        BugReport(user_id=1, bug_id='10000001', report_type='UI Bug'),
        BugReport(user_id=2, bug_id='10000002', report_type='Performance Bug'),
    ]
    db.session.add_all(reports)
    db.session.commit()
    
    print('เพิ่มข้อมูลเรียบร้อย!')
    print(f'Users: {User.query.count()}')
    print(f'Bugs: {Bug.query.count()}')
    print(f'BugReports: {BugReport.query.count()}')