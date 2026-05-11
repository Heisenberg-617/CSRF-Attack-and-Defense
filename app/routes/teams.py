# Team management routes
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.db import get_db_connection

teams_bp = Blueprint('teams', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour accéder à cette page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@teams_bp.route('/teams', methods=['GET', 'POST'])
@login_required
def manage_teams():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        team_name = request.form.get('name', '').strip()
        team_description = request.form.get('description', '').strip()

        if not team_name:
            flash("Le nom de l'équipe ne peut pas être vide.", "warning")
            cursor.close()
            conn.close()
            return redirect(url_for('teams.manage_teams'))

        try:
            cursor.execute(
                "INSERT INTO teams (name, description) VALUES (%s, %s)",
                (team_name, team_description or None)
            )
            conn.commit()
            flash(f"L'équipe '{team_name}' a été créée avec succès !", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Erreur lors de la création : {str(e)}", "danger")

        cursor.close()
        conn.close()
        return redirect(url_for('teams.manage_teams'))

    cursor.execute("SELECT * FROM teams ORDER BY created_at DESC")
    all_teams = cursor.fetchall()

    cursor.execute(
        "SELECT tasks.id, tasks.title, teams.name AS team_name FROM tasks LEFT JOIN teams ON tasks.team_id = teams.id WHERE tasks.user_id = %s ORDER BY tasks.created_at DESC",
        (session['user_id'],)
    )
    user_tasks = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('teams.html', teams=all_teams, tasks=user_tasks)


# Cible CSRF : pas de token, pas de validation CSRF
@teams_bp.route('/tasks/assign', methods=['POST'])
@login_required
def assign_task_to_team():

    task_id = request.form.get('task_id')
    team_id = request.form.get('team_id')

    # Validate that both IDs are present and numeric
    if not task_id or not team_id:
        flash("Données d'assignation invalides.", "danger")
        return redirect(url_for('tasks.dashboard'))

    try:
        task_id = int(task_id)
        team_id = int(team_id)
    except (ValueError, TypeError):
        flash("Données d'assignation invalides.", "danger")
        return redirect(url_for('tasks.dashboard'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Ownership check : only the task owner can assign it to a team
        cursor.execute(
            "UPDATE tasks SET team_id = %s WHERE id = %s AND user_id = %s",
            (team_id, task_id, session['user_id'])
        )
        rows_affected = cursor.rowcount
        conn.commit()

        if rows_affected == 0:
            flash("Tâche introuvable ou vous n'êtes pas le propriétaire.", "warning")
        else:
            flash("La tâche a bien été assignée à l'équipe !", "success")

    except Exception as e:
        flash(f"Erreur lors de l'assignation : {str(e)}", "danger")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

    return redirect(url_for('tasks.dashboard'))