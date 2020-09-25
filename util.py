from exceptions import UserAlreadyExistsError
from sqlalchemy.exc import IntegrityError
from slack import WebClient
from slack.errors import SlackApiError


def create_user_in_database(db, data, model):
    fields = [
          "id", "deleted", "is_admin", "is_app_user",
          "is_bot", "is_owner", "is_primary_owner",
          "is_restricted", "is_ultra_restricted", "team_id","name", "real_name"
    ]
    temp = dict()
    for k in fields:
        attr = data.get(k)
        temp[k] = attr
    x = model(**temp)

    try:
        db.session.add(x)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise UserAlreadyExistsError

    except Exception as err:
        print(f"Something went wrong. Details: {err}")
        db.session.rollback()

    return


def format_special_message(message):
    return { 
        "type": "plain_text",
        "text": message, 
    }


def format_user_info(user):
    deactivated = "(deactivated)" if user.deleted else ""
    bot = "(bot)" if user.is_bot else ""
    text = (
        f"<{user.real_name}{deactivated}{bot}>"
    )

    return { 
        "type": "plain_text",
        "text": text, 
    }


def sync_users(app, db, model, access_token):
    slack_client = WebClient(token=access_token)

    try:
        data = slack_client.users_list()
    except SlackApiError as err:
        print(err)

    for user in data['members']:
        try:
            create_user_in_database(db, user, model)
        except UserAlreadyExistsError:
            # Sync the next user
            pass
