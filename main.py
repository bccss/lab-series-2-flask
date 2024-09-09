from flask import Flask, request, redirect, url_for, render_template # Necessary Imports from the flask library
from flask_sqlalchemy import SQLAlchemy # Imports the flask SQL tookit for simple database access

app = Flask(__name__) #
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Class that uses functions from sqlalchemy to set all attributes for an event
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Event {self.name}>'

@app.route('/') # Route for the index page of the app
def index():
    events = Event.query.all() # Queries all events stored in our database
    return render_template('index.html', events=events) # Returns the index.html template with queried events

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/add', methods=['POST']) # Route for handling POST requests to add a new event
def add_event():
    name = request.form.get('name') # Retrieves the event name from the form
    date = request.form.get('date') # Retrieves the event date from the form
    description = request.form.get('description') # Retrieves the event description from the form
    location = request.form.get('location') # Retrieves the event location from the form
    new_event = Event(name=name, date=date, description=description, location=location) # Creates a new Event instance
    db.session.add(new_event) # Adds the new event to the database session
    db.session.commit() # Commits the changes to the database
    return redirect(url_for('index')) # Redirects to the index page after adding the event

@app.route('/edit/<int:id>', methods=['GET', 'POST']) # Route for handling GET and POST requests to edit an existing event
def edit_event(id):
    event = Event.query.get_or_404(id) # Retrieves the event by ID or returns a 404 error if not found
    if request.method == 'POST': # If the request method is POST, update the event
        event.name = request.form.get('name') # Updates the event name from the form
        event.date = request.form.get('date') # Updates the event date from the form
        event.description = request.form.get('description') # Updates the event description from the form
        event.location = request.form.get('location') # Updates the event location from the form
        db.session.commit() # Commits the changes to the database
        return redirect(url_for('index')) # Redirects to the index page after updating the event
    return render_template('edit.html', event=event) # Renders the edit.html template with the event details


@app.route('/delete/<int:id>') # Route for handling the deletion of an event
def delete_event(id):
    event = Event.query.get_or_404(id) # Retrieves the event by ID or returns a 404 error if not found
    db.session.delete(event) # Deletes the event from the database session
    db.session.commit() # Commits the changes to the database
    return redirect(url_for('index')) # Redirects to the index page after deleting the event

if __name__ == '__main__':
    with app.app_context(): # Creates an application context for running database commands
      db.create_all() # Creates database tables for the defined models
    app.run(debug=True) # Runs the Flask development server in debug mode