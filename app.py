# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_tasks():
    db = get_db()
    cur = db.execute('select * from tasks order by id desc')
    tasks = cur.fetchall()
    return render_template('show_tasks.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    db = get_db()
    db.execute('insert into tasks (title, text, completed) values (?, ?, ?)',
               [request.form['title'], request.form['text'], 'False'])
    db.commit()
    flash('New task was successfully posted')
    return redirect(url_for('show_tasks'))

@app.route('/edit', methods=['POST'])
def edit_task():
    title = request.form['title']
    text = request.form['description']
    task_id = int(request.form['task-id'])

    db = get_db()
    db.execute("UPDATE tasks SET title = ?, text = ? WHERE id = ?", (title, text, task_id))
    db.commit()

    flash('Task was successfully edited')
    return redirect(url_for('show_tasks'))

@app.route('/delete', methods=['POST'])
def delete_task():
    task = int(request.form['task-to-delete'])

    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task,))
    db.commit()

    flash('Task was successfully deleted')
    return redirect(url_for('show_tasks'))

@app.route('/complete', methods=['POST'])
def complete_task():
    task_id = int(request.form['task-id'])

    db = get_db()
    curs = db.execute('SELECT completed FROM tasks WHERE id = ?', (task_id,))
    completion = curs.fetchone()[0]

    if completion == 'False':
        db.execute('UPDATE tasks SET completed = ? WHERE id = ?', ('True', task_id))
    elif completion == 'True':
        db.execute('UPDATE tasks SET completed = ? WHERE id = ?', ('False', task_id))

    db.commit()

    return redirect(url_for('show_tasks'))