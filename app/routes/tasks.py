# Task management routes
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database.db import get_db_connection  # <-- FIX ICI

tasks_bp = Blueprint('tasks', __name__)


# =========================
# Dashboard - Read Tasks
# =========================
@tasks_bp.route('/dashboard')
def dashboard():

    db = get_db_connection()  # <-- FIX
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT 
            tasks.id,
            tasks.title,
            tasks.description,
            tasks.deadline,
            teams.name AS team_name
        FROM tasks
        LEFT JOIN teams ON tasks.team_id = teams.id
    """

    cursor.execute(query)
    tasks = cursor.fetchall()

    return render_template('tasks/dashboard.html', tasks=tasks)


# =========================
# Create Task
# =========================
@tasks_bp.route('/create_task', methods=['GET', 'POST'])
def create_task():

    db = get_db_connection()  # <-- FIX
    cursor = db.cursor(dictionary=True)

    # Get teams for dropdown
    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()

    if request.method == 'POST':

        title = request.form.get('title')
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        team_id = request.form.get('team_id')

        if not title:
            flash("Title is required")
            return redirect(url_for('tasks.create_task'))

        insert_query = """
            INSERT INTO tasks (title, description, deadline, team_id)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (title, description, deadline, team_id)
        )

        db.commit()

        flash("Task created successfully")

        return redirect(url_for('tasks.dashboard'))

    return render_template(
        'tasks/create_task.html',
        teams=teams
    )


# =========================
# Edit Task
# =========================
@tasks_bp.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):

    db = get_db_connection()  # <-- FIX
    cursor = db.cursor(dictionary=True)

    # Get teams
    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()

    # Get task
    cursor.execute(
        "SELECT * FROM tasks WHERE id = %s",
        (task_id,)
    )

    task = cursor.fetchone()

    if not task:
        flash("Task not found")
        return redirect(url_for('tasks.dashboard'))

    if request.method == 'POST':

        title = request.form.get('title')
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        team_id = request.form.get('team_id')

        update_query = """
            UPDATE tasks
            SET
                title = %s,
                description = %s,
                deadline = %s,
                team_id = %s
            WHERE id = %s
        """

        cursor.execute(
            update_query,
            (
                title,
                description,
                deadline,
                team_id,
                task_id
            )
        )

        db.commit()

        flash("Task updated successfully")

        return redirect(url_for('tasks.dashboard'))

    return render_template(
        'tasks/edit_task.html',
        task=task,
        teams=teams
    )


# =========================
# Delete Task
# =========================
@tasks_bp.route('/delete_task', methods=['POST'])
def delete_task():

    task_id = request.form.get('task_id')

    if not task_id:
        flash("Task ID missing")
        return redirect(url_for('tasks.dashboard'))

    db = get_db_connection()  # <-- FIX
    cursor = db.cursor()

    delete_query = """
        DELETE FROM tasks
        WHERE id = %s
    """

    cursor.execute(delete_query, (task_id,))
    db.commit()

    flash("Task deleted successfully")

    return redirect(url_for('tasks.dashboard'))