import re

# import bcrypt
from flask_app.models.user_model import User
from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# from flask_app.models.user_model import user_model ****

@app.route('/')
def login():
    return render_template( 'login.html' )
    # if not user_model.validate_user_model(request.form):
    #     # we redirect to the template with the form.
    #     return redirect( '/' )
    # #... do other things
    # return redirect('/dashboard')


@app.route( '/user/registration', methods = ['POST'] )
def registration():
    if User.validate_user( request.form ) == False:
        return redirect( '/' )
    
    user_exists = User.get_one_to_validate_email( request.form )
    if user_exists != None:
        flash( "This email already exists!", "error_registration_email" )
        return redirect( '/' )
    # proceed to create the user
    data = {
        **request.form,
        "password" : bcrypt.generate_password_hash( request.form['password'] )
    }
    user_id = User.create( data )
    
    session['first_name'] = data['first_name']
    session['email'] = data['email']
    session['user_id'] = user_id

    return redirect( '/user/welcome' ) #This needs to change to another display route 

@app.route('/user/login', methods = ['POST'])
def logon():
    return redirect( '/user/welcome' )


@app.route( '/user/process', methods = ['POST'] )
def process():
    pass

@app.route( '/user/welcome' )
def welcome():
    return render_template( 'welcome.html' )

@app.route( '/user/logout')
def logout():
    session.clear()
    return redirect( '/' )


# @app.route('/create', methods=['POST'])
# def create_user():
#     # if there are errors:
#     # We call the staticmethod on Burger model to validate
#     if not User_model.validate_user(request.form):
#     # redirect to the route where the burger form is rendered.
#         return redirect('/')
#     # else no errors:
#     User_model.save(request.form)
#     return redirect("/users_controller")

