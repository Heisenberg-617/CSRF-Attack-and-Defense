# CSRF Defense Demo

A practical Flask web application designed to demonstrate CSRF vulnerabilities, secure and insecure workflows, and the difference between normal app navigation and attacker-crafted payloads.

---

## Defense notes

- Issue:
  - no CSRF token
  - trusts session cookies blindly

- Fix (conceptually):
  - CSRF tokens (Flask-WTF / custom)
  - SameSite cookies
  - origin validation

---

## No CSRF token:

1. added dependency
Flask-WTF==1.2.1

2. Initialize CSRF Protection

When you pass your app instance to CSRFProtect(app), behind the scenes it does three things automatically:

a. It generates a secret password for the user's session
The moment a user logs in, this extension generates a long, random, unpredictable string (a token). It saves this token into the user's session cookie.

b. It injects that password into your HTML forms
Because you added {{ csrf_token() }} inside your forms, Flask quietly replaces that tag with a hidden input field containing that exact random string.
(So when you view the page source of your secure app, you'll see <input type="hidden" name="csrf_token" value="a8f9c2...">)

c. It checks every POST request before your code even runs
This is the magic part. It intercepts every incoming POST request. It looks at the hidden token in the form data, compares it to the token in the user's session cookie, and asks two questions:
Are they identical?
Are they recent?
If the answer to either is no, the extension instantly kills the request and throws a 400 Bad Request error. Your actual Python route code (def create_user():) never even wakes up.

3. Add Defense-in-Depth (Cookies) in app.py

Force CSRF token to be sent in a cookie (instead of form field) for better security
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True if you ever use HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # THIS IS THE CRITICAL CSRF COOKIE DEFENSE

4. The Template Updates (The bulk of the work)
Because you used raw HTML forms instead of WTForms objects, you must manually inject the hidden token into EVERY SINGLE <form method="POST"> across all your templates.

Inside every <form> tag, add this line as the very first thing:
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">