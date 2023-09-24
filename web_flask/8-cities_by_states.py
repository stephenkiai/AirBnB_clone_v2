#!/usr/bin/python3

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display a list of states and cities."""
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda x: x.name)

   return render_template('8-cities_by_states.html', states=states_sorted)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
