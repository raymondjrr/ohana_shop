Project Name: Ohana Shop

Description:

Do you struggle with remembering what to buy when at the store? Are you tired of asking your family members what they need? With Ohana Shop, no item is left behind. Family members can add items that they need to an 'easy to read' shared shopping list. When you're ready to shop, login and view the list of items needed and start shopping!
Installation:

Install Flask, PyMySql, B-crypt, pipenv shell
Usage:

New users must register. If registered, start by logging in. Form fields have validations such as '@email.com format required', 'password and confirm password must match' and 'minimum 2 characters required for name'. When registering, passwords are hashed when stored into the database. from flask_app.config.mysqlconnection import connectToMySQL from flask import flash, request import re
need to import re for REGEX
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')

2nd need to validate email that email is in a '@' format
class User: def init(self,data): self.id = data['id'] self.first_name = data['first_name'] self.last_name = data['last_name'] self.email = data['email'] self.password = data['password'] self.created_at = data['created_at'] self.updated_at = data['updated_at'] self.creator = None

@classmethod
def save(cls, data):
    query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
    return connectToMySQL("family_list").query_db(query, data)

@classmethod
def email_exists(cls, email):
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = {"email": email}
    result = connectToMySQL("family_list").query_db(query, data)
    return bool(result)

@classmethod
def get_by_email(cls, data):
    query = "SELECT * FROM users WHERE email = %(email)s;"
    result = connectToMySQL("family_list").query_db(query,data)
# Didn't find a matching user
    if len(result) < 1:
        return False
    return cls(result[0])

@classmethod
def get_by_id(cls, data):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    result = connectToMySQL("family_list").query_db(query,data)
    return cls(result[0])

@staticmethod
def validate_user(user):
    is_valid = True
    # Start of validations
# Validates that email is in '@' format
    if not EMAIL_REGEX.match(user['email']):
        flash("Enter a valid email address")
        is_valid = False
    elif User.email_exists(user['email']):
        flash("Email already exists. Please choose a different email")
# Validates that username is at least 2 characters
    if len(user['first_name']) < 2:
        flash("First name must be at least 2 characters")
        is_valid = False

    if len(user['last_name']) < 2:
        flash("Last name must be at least 2 characters")
        is_valid = False

# Validates that password is at least 8 characters
    if len(user['password']) < 8:
        flash("Password must be at least 8 characters")
        is_valid = False

# Validates that password and confirm password match
    if user['password'] != request.form['confirm_password']:
        flash("Password and Confirm Password must match")
        is_valid = False

    return is_valid
All routes are protected. If a user is not in session and attempts to access other webpages within the app, they will be redirected to login/register page: if not session.get('user_id'): return redirect('/')
Once logged in, users can add, view, edit or delete items. Only the specific user that added the item has the ability to edit or delete item. @app.route('/item/int:id/edit') def edit_item(id): if not session.get('user_id'): return redirect('/') else: data = { 'id':id } item = Item.get_one_by_id(data) return render_template('edit.html', item=item)
@app.route('/item/int:id', methods=['POST']) def update_item(id): if not session.get('user_id'): return redirect('/') else: if not Item.validate_item(request.form): return redirect('/item/create') data = { 'id':id, 'item_name':request.form['item_name'], 'user_id':session['user_id'] } Item.update(data) return redirect('/dashboard')

@app.route('/item/int:id/delete') def delete(id): data = { 'id':id } Item.delete(data) return redirect('/dashboard')