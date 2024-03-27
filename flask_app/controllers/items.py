from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.item import Item

@app.route('/item/create')
def recipe_form():
    if not session.get('user_id'):
        return redirect('/')
    else:
        return render_template('create.html')

@app.route('/item', methods=['POST'])
def create_item():
    if not session.get('user_id'):
        return redirect('/')
    else:
        if not Item.validate_item(request.form):
            return redirect('/item/create')
    data = {
        'item_name':request.form['item_name'],
        'user_id':session['user_id']
    }
    print("Session user_id:", session['user_id'])
    Item.save(data)
    return redirect('/dashboard')

@app.route('/item/<int:id>')
def one_item_display(id):
    if not session.get('user_id'):
        return redirect('/')
    else:
        data = {
            'id':id
        }
    item = Item.get_one_by_id(data)
    return render_template('show.html',item=item)


@app.route('/item/<int:id>/edit')
def edit_item(id):
    if not session.get('user_id'):
        return redirect('/')
    else:
        data = {
            'id':id
        }
    item = Item.get_one_by_id(data)
    return render_template('edit.html', item=item)

@app.route('/item/<int:id>', methods=['POST'])
def update_item(id):
    if not session.get('user_id'):
        return redirect('/')
    else:
        if not Item.validate_item(request.form):
            return redirect('/item/create')
    data = {
        'id':id,
        'item_name':request.form['item_name'],
        'user_id':session['user_id']
    }
    Item.update(data)
    return redirect('/dashboard')

@app.route('/item/<int:id>/delete')
def delete(id):
    data = {
        'id':id
    }
    Item.delete(data)
    return redirect('/dashboard')


