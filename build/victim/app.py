"""
Lab - ARP Spoof Attack
    > Webapp for demo

This is intentional insecure code! Do NOT use for production!

(CC BY-SA 4.0) github.com/moospit
"""

from flask import Flask, request, redirect, url_for, Response

app = Flask(__name__)

@app.route('/')
def root() -> Response:
    """ Redirect all request to login """
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login() -> str:
    """ Minimal exmaple - authenticate a user """
    if request.method == 'POST':  # handle POST
        username = request.form.get('user', '')
        password = request.form.get('pass', '')
    else:  # handle GET
        username = request.args.get('user', '')
        password = request.args.get('pass', '')

    # ensure we got all the data we need
    if '' in (username, password):
        return 'Login needs user=<data>&pass=<data> as GET- or POST-parameters\n'

    return f'Succesfully logged in {username}\n'


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
