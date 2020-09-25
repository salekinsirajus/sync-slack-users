import os

from flask import current_app as app, request
from flask import jsonify, abort

from models import db, User
from util import create_user_in_database, format_user_info, format_special_message
from util import sync_users
from exceptions import UserAlreadyExistsError


@app.route("/")
def root():
    return "Slack User sync app"




@app.route("/users/", methods=["POST",])
def get_users():
    """Returns a list of users from the database
    
    """
    # v2 feature:
    #   Paginate the query
    #   Accept pagination parameters from the slack app interface
    data = db.session.query(User).all()

    results = []
    for each in data:
        results.append(format_user_info(each))

    if len(results) < 1:
        # Ideally, the user should not get here 
        # You want to sync the users on app install on the workspace
        message = "No user found on this workspace"
        results.append(format_special_message(message))

    rv = {
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Users on this Workspace:",
                }
            },

            {
                "type": "section",
                "fields": results 
            }
        ]
    }

    return jsonify(rv) 


@app.route("/events/", methods=["POST",])
def respond_to_challenge():
    """Endpoint to communicate with Slack's events API.

    Responds to slack verification challenges as well process user events.
    """

    app.logger.info("Receiving an event from slack")
    data = request.get_json()
    if data.get('token') != os.getenv('SLACK_VERIFICATION_TOKEN'):
        # returns 401
        abort(401, "Cannot validate sender")

    if 'challenge' in data:
        rv = {"challenge": data['challenge']}
        return jsonify(rv)

    event = data.get('event')
    if event['type'] != 'user_change':
        return "We current process user_change events only"

    event_user = event.get('user')

    synced_user = db.session.query(User).filter(User.id == event_user['id']).first()

    fields = ["id", "deleted", "is_admin", "is_app_user",
              "is_bot", "is_owner", "is_primary_owner",
              "is_restricted", "is_ultra_restricted", 
              "team_id", "name", "real_name"]

    try:
        if synced_user is None:
            create_user_in_database(db, event_user, User)
            return
    except UserAlreadyExistsError:
        pass

    # updating the user
    for field in fields:
        setattr(synced_user, field, event_user.get(field))

    try:
        db.session.commit()
    except Exception as err:
        db.session.rollback()


    return "Processed user update event"


@app.route("/sync")
def manual_sync():
    """This is a hack"""
    access_token = os.getenv('SLACK_ACCESS_TOKEN')
    sync_users(app, db, User, access_token)

    return "Synced users"
