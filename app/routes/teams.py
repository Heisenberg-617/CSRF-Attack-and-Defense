# Team management routes
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# On suppose que tu as un module de base de données pour récupérer une connexion MySQL
# Adapte l'import selon la structure réelle de ton projet (ex: database.db ou db_connect)
# from database import get_db_connection 

teams_bp = Blueprint('teams', __name__)

# Simulons une fonction de connexion si tu n'as pas encore configuré MySQL
# (À remplacer par ta vraie connexion MySQL)
def get_db_connection():
    # import mysql.connector
    # return mysql.connector.connect(host="localhost", user="root", password="", database="csrf_lab")
    pass


### 1. Afficher et Créer des Équipes
@teams_bp.route('/teams', methods=['GET', 'POST'])
def manage_teams():
    # Vérification que l'utilisateur est bien connecté (Session)
    if 'user_id' not in session:
        flash("Veuillez vous connecter pour accéder à cette page.", "danger")
        return redirect(url_for('auth.login')) # Adapte selon le nom de ta route de login

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Récupération du nom de l'équipe depuis le formulaire
        team_name = request.form.get('name')
        
        if team_name:
            # Insertion dans la base de données
            cursor.execute("INSERT INTO teams (name) VALUES (%s)", (team_name,))
            conn.commit()
            flash(f"L'équipe '{team_name}' a été créée avec succès !", "success")
        else:
            flash("Le nom de l'équipe ne peut pas être vide.", "warning")
        
        cursor.close()
        conn.close()
        return redirect(url_for('teams.manage_teams'))

    # Si GET : On récupère toutes les équipes pour les afficher
    cursor.execute("SELECT * FROM teams")
    all_teams = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('teams.html', teams=all_teams)


### 2. Assigner une tâche à une équipe
# C'est cette route POST qui sera la cible parfaite pour la démo de l'attaque CSRF !
@teams_bp.route('/tasks/assign', methods=['POST'])
def assign_task_to_team():
    if 'user_id' not in session:
        flash("Accès non autorisé.", "danger")
        return redirect(url_for('auth.login'))

    # Récupération des données du formulaire
    task_id = request.form.get('task_id')
    team_id = request.form.get('team_id')

    if not task_id or not team_id:
        flash("Données d'assignation invalides.", "danger")
        return redirect(url_for('tasks.dashboard')) # Redirige vers le tableau de bord des tâches

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Mise à jour de la tâche avec l'ID de l'équipe correspondante
        cursor.execute(
            "UPDATE tasks SET team_id = %s WHERE id = %s", 
            (team_id, task_id)
        )
        conn.commit()
        flash("La tâche a bien été assignée à l'équipe !", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Erreur lors de l'assignation : {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()

    # Redirection vers le dashboard des tâches pour voir le changement
    return redirect(url_for('tasks.dashboard'))