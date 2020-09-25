# Slack App
I implmented this app as part of a coding challenge from WorkOS. It's a slack app
that is suppossed to keep track of the users of workspace, as well as update the
list of users as the users update their account and profile.

[Application URL](https://slack-user-app.sirajussalekin.com)

[Slack Workspace URL](https://workoscodingc-5is3828.slack.com)


## How to use
You should be able to access the list of users by `/users` slash command on the slack
workspace

You can test update on the existing users by changing the `Full Name` field since that's
one of the key pieces of information you'll see displayed on the list (out of a couple).


## Notes
This app contains the bare bone elements due to the scope and time constraints.
Currently we store very basic fields on the database. The schema is extensible 
to allow more fields. The app surface also contains the absolute minimum information
about the users.

Some immediate features/additions:
1. unittests
2. Pagination on the GET /users/ endpoint when you have a long list of users
3. Allow initial and overnight sync with a background job  
