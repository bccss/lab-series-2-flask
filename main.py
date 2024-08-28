from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Event {self.name}>'

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

@app.route('/add', methods=['POST'])
def add_event():
    name = request.form.get('name')
    date = request.form.get('date')
    description = request.form.get('description')
    location = request.form.get('location')
    new_event = Event(name=name, date=date, description=description, location=location)
    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    event = Event.query.get_or_404(id)
    if request.method == 'POST':
        event.name = request.form.get('name')
        event.date = request.form.get('date')
        event.description = request.form.get('description')
        event.location = request.form.get('location')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', event=event)

@app.route('/delete/<int:id>')
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
      db.create_all()
    app.run(debug=True)
