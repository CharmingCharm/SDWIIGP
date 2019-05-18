from app.extension import db

class TestSet(db.Model):
    __tablename__ = 'testset'

    testset_id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    tests = db.relationship(
        'Test',
        secondary = 'test_in_testset',
        backref = db.backref('testsets', lazy = 'dynamic'),
        lazy = 'dynamic'
    )
    submissions = db.relationship('Submission', lazy = 'dynamic')
