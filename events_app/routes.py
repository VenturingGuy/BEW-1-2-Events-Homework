"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint('main', __name__)


##########################################
#           Routes                       #
##########################################

@main.route('/', methods=['GET', 'POST'])
def index():
        
    """Show upcoming events to users!"""
    # TODO: Get all events and send to the template
    events = ''

    try:
        events = Event.query.all()
    except:
        print("No Active Events")
    for event in events:
        print(type(event.date_and_time))

    return render_template("index.html", events=events)


@main.route('/event/<event_id>', methods=['GET'])
def event_detail(event_id):
    """Show a single event."""
    # TODO: Get the event with the given id and send to the template
    event = ""
    try:
        event = Event.query.filter_by(id=event_id).one()
    except:
        print("Error: No Event Found")

    return render_template("event_detail.html", event=event, guests=event.guests)


@main.route('/event/<event_id>', methods=['POST'])
def rsvp(event_id):
    """RSVP to an event."""
    is_returning_guest = request.form.get("returning")
    guest_name = request.form.get("guest_name")
    event = Event.query.filter_by(id=event_id).one()

    if is_returning_guest:
        try:
            guest = Guest.query.filter_by(name=guest_name).one()
        except:
            flash("An error has occurred. Please try again.")
            return redirect(url_for("main.event_detail", event_id=event_id))
    else:
        guest_email = request.form.get("email")
        guest_number = request.form.get("number")
        guest = Guest(name=guest_name, email=guest_email, number=guest_number)
    guest.events_attending.append(event)
    db.session.add(guest)
    db.session.commit()
    
    flash("RSVP Successful.")
    return redirect(url_for('main.event_detail', event_id=event_id))


@main.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new event."""

    if request.method == "POST":
        new_event_title = request.form.get("title")
        new_event_description = request.form.get("description")
        date = request.form.get("date")
        time = request.form.get("time")

        try:
            date_and_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        except ValueError:
            print("Error: Incorrect Format")

        new_event = Event(
            title=new_event_title,
            description=new_event_description,
            date_and_time=date_and_time,
        )

        db.session.add(new_event)
        db.session.commit()
        flash("Event created.")

        return redirect(url_for("main.index"))
    else:
        return render_template("create.html")


@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    # TODO: Get the guest with the given id and send to the template
    guest = ''
    try:
        guest = Guest.query.filter_by(id=guest_id).one()
    except:
        print("No Guest Was Found")
    return render_template(
        "guest_detail.html", guest=guest, events_attending=guest.events_attending
    )
