from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///health.db'
db = SQLAlchemy(app)

class HealthLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    weight = db.Column(db.Float)
    medication_taken = db.Column(db.Boolean)
    notes = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        log = HealthLog(
            weight=float(request.form['weight']),
            medication_taken='medication' in request.form,
            notes=request.form['notes']
        )
        db.session.add(log)
        db.session.commit()
        return redirect('/')
    logs = HealthLog.query.order_by(HealthLog.date.desc()).all()
    return render_template('index.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)