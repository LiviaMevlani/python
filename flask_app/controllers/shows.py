from flask_app import app
from flask import render_template, redirect, session, request, flash, jsonify
from flask_app.models.show import Show
from flask_app.models.user import User

@app.route('/add/show')
def AddShow():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    return render_template('createshow.html', loggedUser=loggedUser)


@app.route('/create/show', methods = ['POST'])
def createShow():
    if 'user_id' not in session:
        return redirect('/')
    if not Show.validate_show(request.form):
        return redirect(request.referrer)
    data = {
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Show.create(data)
    return redirect('/')


@app.route('/showInfo/<int:id>')
def viewShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'show_id': id,
        'id': session['user_id']
    }
    show = Show.get_show_by_id(data)
    loggedUser = User.get_user_by_id(data)
    usersWhoLiked = Show.get_likers(data)
    likersDetails = Show.get_likers_info(data)
    return render_template('showInfo.html', show=show, loggedUser=loggedUser, usersWhoLiked=usersWhoLiked, likersDetails=likersDetails)


@app.route('/edit/show/<int:id>')
def editShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'show_id': id,
        'id': session['user_id']
    }
    show = Show.get_show_by_id(data)
    if not show:
        return redirect('/')
    loggedUser = User.get_user_by_id(data)
    if show['user_id'] != loggedUser['id']:
        return redirect('/')

    return render_template('editShow.html', show=show, loggedUser=loggedUser)


@app.route('/update/show/<int:id>', methods = ['POST'])
def updateShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'show_id': id,
        'id': session['user_id']
    }
    show = Show.get_show_by_id(data)
    if not show:
        return redirect('/')
    loggedUser = User.get_user_by_id(data)
    if show['user_id'] != loggedUser['id']:
        return redirect('/')
    
    if len(request.form['title'])<1 or len(request.form['network'])<1 or len(request.form['release_date'])<1 or len(request.form['description'])<1 :
        flash('All fields required', 'allRequired')
        return redirect(request.referrer)
    
    updateData = {
        'title': request.form['title'],
        'network': request.form['network'],
        'release_date': request.form['release_date'],
        'description': request.form['description'],
        'id': id
    }
    if not Show.validate_show(updateData):
        return redirect(request.referrer)
    Show.update_show(updateData)
    return redirect('/showInfo/'+ str(id))
    
    

@app.route('/delete/show/<int:id>')
def deleteShow(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'show_id': id,
        'id': session['user_id']
    }
    show = Show.get_show_by_id(data)
    if not show:
        return redirect('/')
    loggedUser = User.get_user_by_id(data)
    if loggedUser['id'] == show['user_id']:
        Show.delete_all_likes(data)
        Show.delete_show(data)
    return redirect('/')


@app.route('/like/<int:id>')
def addLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'show_id': id,
        'id': session['user_id']
    }
    usersWhoLiked = Show.get_likers(data)
    if session['user_id'] not in usersWhoLiked:
        Show.addLike(data)
        return redirect(request.referrer)
    return redirect(request.referrer)


@app.route('/unlike/<int:id>')
def removeLike(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'show_id': id,
        'id': session['user_id']
    }    
    Show.removeLike(data)
        
    return redirect(request.referrer)