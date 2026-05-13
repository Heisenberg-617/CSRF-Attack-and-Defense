from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from functools import wraps
from database.db import get_db_connection
from werkzeug.security import generate_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Access denied: Admin privileges required.', 'error')
            return redirect(url_for('tasks.dashboard'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/users')
@admin_required
def manage_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY id")
        users = cursor.fetchall()
    except Exception as e:
        flash(f'Error loading users: {str(e)}', 'error')
        users = []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/create', methods=['POST'])
@admin_required
def create_user():
    """
    CSRF VULNERABILITY: The 'role' is taken directly from the form data.
    An attacker can force an admin to create another admin account.
    """
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    # Secured 
    role = request.form.get('role', 'guest')
    # STRICT WHITELIST: If the submitted role isn't in this list, force it to 'guest'
    if role not in ['guest', 'responsable_equipe', 'responsable_projet']:
        role = 'guest'

    if not username or not email or not password:
        flash('All fields are required.', 'error')
        return redirect(url_for('admin.manage_users'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        pw_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
            (username, email, pw_hash, role)
        )
        conn.commit()
        flash(f'User "{username}" created with role "{role}".', 'success')
    except Exception as e:
        flash(f'Error creating user: {str(e)}', 'error')
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/users/<int:user_id>/role', methods=['POST'])
@admin_required
def update_role(user_id):
    new_role = request.form.get('role')
    if new_role in ['admin', 'responsable_equipe', 'responsable_projet', 'guest']:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET role = %s WHERE id = %s", (new_role, user_id))
            conn.commit()
            flash('Role updated successfully.', 'success')
        except Exception as e:
            flash(f'Error updating role: {str(e)}', 'error')
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conn' in locals(): conn.close()
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == session.get('user_id'):
        flash('You cannot delete your own account.', 'error')
        return redirect(url_for('admin.manage_users'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        flash('User deleted successfully.', 'success')
    except Exception as e:
        flash(f'Error deleting user: {str(e)}', 'error')
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
        
    return redirect(url_for('admin.manage_users'))