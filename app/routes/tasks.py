from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.database.db import get_db_connection
from datetime import date

tasks_bp = Blueprint('tasks', __name__)

# =========================
# Dashboard - Liste des tâches
# =========================
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

# =========================
# Créer une tâche
# =========================
@tasks_bp.route('/create_task', methods=['GET', 'POST'])
def create_task():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        
        # RAPPEL LOGIQUE : On récupère la valeur du Select
        team_id = request.form.get('team_id')
        # Si c'est une chaîne vide (option par défaut), on met None pour MySQL
        if not team_id:
            team_id = None

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

    # Pour afficher la liste des équipes dans le formulaire
    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('tasks/create_task.html', teams=teams)

# =========================
# Modifier une tâche
# =========================
@tasks_bp.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        deadline = request.form.get('deadline')
        
        # RAPPEL LOGIQUE : Même traitement pour l'édition
        team_id = request.form.get('team_id')
        if not team_id:
            team_id = None

        cursor.execute(
            "UPDATE tasks SET title=%s, description=%s, deadline=%s, team_id=%s WHERE id=%s",
            (title, description, deadline, team_id, task_id)
        )
        db.commit()
        cursor.close()
        db.close()
        flash("Task updated successfully", "success")
        return redirect(url_for('tasks.dashboard'))

    # GET : Récupération et formatage de la date pour le HTML
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    
    if task and task['deadline']:
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

# =========================
# Supprimer une tâche (Cible CSRF)
# =========================
@tasks_bp.route('/delete_task', methods=['POST'])
def delete_task():
    task_id = request.form.get('task_id')
    if not task_id:
        flash("Task ID missing", "danger")
        return redirect(url_for('tasks.dashboard'))

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    db.commit()
    cursor.close()
    db.close()
    flash("Task deleted successfully", "success")
    return redirect(url_for('tasks.dashboard'))

# =========================
# Détails d'une tâche
# =========================
@tasks_bp.route('/task/<int:task_id>')
def task_details(task_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT tasks.*, teams.name AS team_name 
        FROM tasks 
        LEFT JOIN teams ON tasks.team_id = teams.id 
        WHERE tasks.id = %s
    """
    cursor.execute(query, (task_id,))
    task = cursor.fetchone()
    cursor.close()
    db.close()

    if not task:
        flash("Task not found", "danger")
        return redirect(url_for('tasks.dashboard'))

    return render_template('tasks/task_details.html', task=task)