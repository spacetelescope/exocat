from flask import abort
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import Response
from flask import url_for
from flask import make_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/current_table/')
def current_table():
    """
    Renders a template that displays the current table.

    Returns
    -------
    current_table.html : obj
        The template for ``current_table.html``.
    """

    return render_template('current_table.html')

@app.route('/About_ExoCat/')
def about_exocat():
    """
    Renders a template that displays the About page.

    Returns
    -------
    About_ExoCat.html : obj
        The template for ``About_ExoCat.html``.
    """

    return render_template('About_ExoCat.html')