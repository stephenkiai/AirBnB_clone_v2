#!/usr/bin/python3
"""
Start a Flask web application.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Display a list of states."""
    states = storage.all(State).values()
    states_sorted = sorted(states, key=lambda x: x.name)

    return render_template('8-states.html', states=states_sorted)


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Display a state's cities or 'Not found!'."""
    state = storage.get(State, id)

    if state:
        cities = sorted(state.cities, key=lambda x: x.name)
        return render_template('9-states.html', state=state, cities=cities)

    return render_template('9-states.html', state=None)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
