from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db import get_db_connection
from functools import wraps
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM tasks WHERE user_id = %s ORDER BY created_at DESC", (session['user_id'],))
        tasks = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('tasks/dashboard.html', tasks=tasks)

    except Exception as e:
        flash(f'Error loading tasks: {str(e)}', 'error')
        return render_template('tasks/dashboard.html', tasks=[])


@tasks_bp.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        deadline = request.form.get('deadline', None)

        if not title:
            flash('Title is required', 'error')
            return redirect(url_for('tasks.create_task'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO tasks (title, description, deadline, user_id) VALUES (%s, %s, %s, %s)",
                (title, description or None, deadline or None, session['user_id'])
            )
            conn.commit()
            cursor.close()
            conn.close()

            flash('Task created successfully!', 'success')
            return redirect(url_for('tasks.dashboard'))

        except Exception as e:
            flash(f'Error creating task: {str(e)}', 'error')
            return redirect(url_for('tasks.create_task'))

    return render_template('tasks/create_task.html')


@tasks_bp.route('/tasks/<int:task_id>')
@login_required
def task_details(task_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, session['user_id']))
        task = cursor.fetchone()
        cursor.close()
        conn.close()

        if not task:
            flash('Task not found', 'error')
            return redirect(url_for('tasks.dashboard'))

        return render_template('tasks/task_details.html', task=task)

    except Exception as e:
        flash(f'Error loading task: {str(e)}', 'error')
        return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM tasks WHERE id = %s AND user_id = %s", (task_id, session['user_id']))
        task = cursor.fetchone()

        if not task:
            flash('Task not found', 'error')
            cursor.close()
            conn.close()
            return redirect(url_for('tasks.dashboard'))

        if request.method == 'POST':
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            status = request.form.get('status', 'todo')

            if not title:
                flash('Title is required', 'error')
                cursor.close()
                conn.close()
                return redirect(url_for('tasks.edit_task', task_id=task_id))

            cursor.execute(
                "UPDATE tasks SET title = %s, description = %s, status = %s WHERE id = %s AND user_id = %s",
                (title, description or None, status, task_id, session['user_id'])
            )
            conn.commit()
            cursor.close()
            conn.close()

            flash('Task updated successfully!', 'success')
            return redirect(url_for('tasks.task_details', task_id=task_id))

        cursor.close()
        conn.close()
        return render_template('tasks/edit_task.html', task=task)

    except Exception as e:
        flash(f'Error updating task: {str(e)}', 'error')
        return redirect(url_for('tasks.dashboard'))


@tasks_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, session['user_id']))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Task deleted successfully!', 'success')
        return redirect(url_for('tasks.dashboard'))

    except Exception as e:
        flash(f'Error deleting task: {str(e)}', 'error')
        return redirect(url_for('tasks.dashboard'))
