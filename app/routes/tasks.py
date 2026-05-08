from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database.db import get_db_connection
from datetime import date # Import nécessaire pour le formatage

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/dashboard')
def dashboard():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT tasks.id, tasks.title, tasks.description, tasks.deadline, teams.name AS team_name
        FROM tasks
        LEFT JOIN teams ON tasks.team_id = teams.id
    """
    cursor.execute(query)
    tasks = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('tasks/dashboard.html', tasks=tasks)

@tasks_bp.route('/create_task', methods=['GET', 'POST'])
def create_task():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        team_id = request.form.get('team_id')

        if not title:
            flash("Title is required", "danger")
            return redirect(url_for('tasks.create_task'))

        cursor.execute(
            "INSERT INTO tasks (title, description, deadline, team_id) VALUES (%s, %s, %s, %s)",
            (title, description, deadline, team_id)
        )
        db.commit()
        cursor.close()
        db.close()
        flash("Task created successfully", "success")
        return redirect(url_for('tasks.dashboard'))

    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('tasks/create_task.html', teams=teams)

@tasks_bp.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        team_id = request.form.get('team_id')

        cursor.execute(
            "UPDATE tasks SET title=%s, description=%s, deadline=%s, team_id=%s WHERE id=%s",
            (title, description, deadline, team_id, task_id)
        )
        db.commit()
        cursor.close()
        db.close()
        flash("Task updated successfully", "success")
        return redirect(url_for('tasks.dashboard'))

    # GET : Récupération et formatage de la date
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    
    if task and task['deadline']:
        # IMPORTANT : Convertit l'objet date en string YYYY-MM-DD pour le HTML
        if isinstance(task['deadline'], (date,)):
            task['deadline'] = task['deadline'].strftime('%Y-%m-%d')

    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()
    cursor.close()
    db.close()
    
    if not task:
        flash("Task not found", "warning")
        return redirect(url_for('tasks.dashboard'))

    return render_template('tasks/edit_task.html', task=task, teams=teams)

@tasks_bp.route('/delete_task', methods=['POST'])
def delete_task():
    task_id = request.form.get('task_id')
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.commit()
    cursor.close()
    db.close()
    flash("Task deleted successfully", "success")
    return redirect(url_for('tasks.dashboard'))