"""
Flask app to demonstrate the UP API:
1. OAuth connection
2. Read user info
3. Create a generic event in the feed
"""
import flask
import keys
import requests_oauthlib


app = flask.Flask(__name__)
app.secret_key = keys.secret_key


UP = {
    'client_id': keys.up_id,
    'client_secret': keys.up_secret,
    'redirect_uri': 'https://herodemo.com/up_authorized',
    'scope': ['basic_read', 'extended_read', 'generic_event_write'],
    'authorization_url': 'https://jawbone.com/auth/oauth2/auth',
    'request_token_url': 'https://jawbone.com/auth/oauth2/token'
}


@app.route('/up_login')
def up_login():
    """
    Redirect to the UP login for approval

    :return: Flask redirect
    """
    oauth = requests_oauthlib.OAuth2Session(
        UP['client_id'],
        redirect_uri=UP['redirect_uri'],
        scope=UP['scope'])
    authorization_url, state = oauth.authorization_url(
        UP['authorization_url'])
    return flask.redirect(authorization_url)


@app.route('/up_authorized')
def up_authorized():
    """
    Callback from UP to finish oauth handshake

    :return: Print out token for now
    """
    oauth = requests_oauthlib.OAuth2Session(UP['client_id'])

    #
    # Super hack to fake https for test env
    #
    url = flask.request.url
    url = url[:4] + 's' + url[4:]

    tokens = oauth.fetch_token(
        UP['request_token_url'],
        authorization_response=url,
        client_secret=UP['client_secret'])

    flask.session['tokens'] = tokens
    return flask.redirect(flask.url_for('home'))


@app.route('/disconnect')
def disconnect():
    """
    Remove the UP tokens from the session.

    :return: redirect to the homepage
    """
    if 'tokens' in flask.session:
        del flask.session['tokens']
    return flask.redirect(flask.url_for('home'))


@app.route('/create_generic')
def create_generic():
    """
    Create a generic event in the feed.

    :return: redirect to the homepage
    """
    up_oauth = requests_oauthlib.OAuth2Session(
        keys.up_id,
        token=flask.session['tokens'])
    up_oauth.post(
        'https://jawbone.com/nudge/api/users/@me/generic_events',
        data={
            'verb': 'created',
            'title': 'Demo Event',
            'note': 'This is a generic event'})
    return flask.redirect(flask.url_for('home'))


def get_user_info():
    """
    Retrieve user details from UP.

    :return: JSON of the user details
    """
    up_oauth = requests_oauthlib.OAuth2Session(
        keys.up_id,
        token=flask.session['tokens'])
    upr = up_oauth.get('https://jawbone.com/nudge/api/users/@me')
    return upr.json()


@app.route('/')
def home():
    """
    Render the homepage.

    :return: rendered homepage template
    """
    if 'tokens' in flask.session:
        user_info = get_user_info()
    else:
        user_info = None

    return flask.render_template(
        'herodemo.html',
        user_info=user_info)


if __name__ == '__main__':
    app.run(debug=True)
