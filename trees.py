from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.tree import Tree
from flask_app.models.user import User


@app.route('/new/tree')
def new_tree():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new.html',user=User.get_by_id(data))


@app.route('/create/tree',methods=['POST'])
def create_tree():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tree.validate_tree(request.form):
        return redirect('/new/tree')
    data = {
        "species":request.form["species"],
        "location": request.form["location"],
        "reason": request.form["reason"],
        "date": request.form["date"],
        "user_id": session["user_id"]
    }
    Tree.save(data)
    return redirect('/dashboard')


@app.route('/edit/tree/<int:id>')
def edit_tree(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html",tree=Tree.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/tree',methods=['POST'])
def update_tree():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Tree.validate_tree(request.form):
        return redirect('/new/tree')
    data = {
        "species":request.form["species"],
        "location": request.form["location"],
        "reason": request.form["reason"],
        "date": request.form["date"],
        "id": request.form['id']
    }
    Tree.update(data)
    return redirect('/dashboard')

@app.route('/trees')
def trees():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('my_trees.html',user=User.get_by_id(data),trees=Tree.get_all())


@app.route('/destroy/tree/<int:id>')
def destroy_tree(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Tree.destroy(data)
    return redirect('/trees')


@app.route('/tree/<int:id>')
def show_tree(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show.html",tree=Tree.get_one(data),user=User.get_by_id(user_data))


@app.route('/visit/<int:tree_id>/visit', methods = ["POST"])
def visitor(tree_id):
    data = {
        'user_id': session['user_id'],
        'tree_id': tree_id
    }
    Tree.visitor(data)
    
    return redirect('/dashboard')




