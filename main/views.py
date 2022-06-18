from django.forms import ValidationError
from flask import *
from main import app
from .models import User, Templates, TemplateSchema
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash





@app.route("/template/<template_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def template_id(template_id):
    """
        Pass in the id of template using url. The following request methods

        - GET: returns the template if it exists

        - PUT: modify the template if it exists, pass in the variables
        'template_name', 'subject', 'body' as json to modify existing template

        - Del: deletes existing template
    """
    
    if request.method == "GET":
        template = Templates.objects(id=template_id).first()

        if not template:
            return jsonify(message="Template doesn't exist"), 404

        identity = get_jwt_identity()

        if template.user.email != identity:
            return jsonify(message="You have are not the owner of this template. Therefore you have no access"), 403

        template_dump = TemplateSchema().dump(template)
        print(template.user.email)
        return jsonify(template_dump)
    
    elif request.method == "PUT":
        template = Templates.objects(id=template_id).first()
        identity = get_jwt_identity()

        if template.user.email != identity:
            return jsonify(message="You are not the author of this template therefore you can not edit it"), 403

        template.name = request.json.get("template_name")
        template.subject = request.json.get("subject")
        template.body = request.json.get("body")

        template.save()

        update_template = Templates.objects(id=template_id).first()
        return jsonify({
            "name": update_template.name,
            "subject": update_template.subject,
            "body": update_template.body
        })

    else:
        template = Templates.objects(id=template_id).first()
        identity = get_jwt_identity()

        if template.user.email != identity:
            return jsonify(message="You are not the author of this template therefore you don't have such permission"), 403

        template.delete()

        return jsonify(message="Delete was successful")



@app.route("/template", methods=["POST", "GET"])
@jwt_required()
def template():
    """
        Accepts two request methods.

        - GET: returns all templates in JSON form
        
        - POST: Pass in the 'template_name', 'subject' and 'body' as
        JSON to store a template.

        This route requires a token in the header for authorization before you can access it.    
    """

    if request.method == "GET":
        user_identity = get_jwt_identity()
        user = User.objects(email=user_identity).first()
        all_templates = Templates.objects(user=user.id)
        template_dump = TemplateSchema(many=True).dump(all_templates)
        return jsonify(template_dump)

    else:
        user_identity = get_jwt_identity()

        user = User.objects(email=user_identity).first()

        # check if user is existent
        if not user:
            return jsonify(message="No user found")

        name = request.json.get("template_name")
        subject = request.json.get("subject")
        body = request.json.get("body")

        template = Templates(name=name, subject=subject, body=body, user=user)
        template.save()

        return jsonify(message="Template saved")



@app.route("/register", methods=["POST"])
def register():
    """
        Route to register users. Pass in first name, last name,
        email and password as json from url endpoint using POST requesty method, 
        stores the data in the database and returns a jwt
    """

    first_name = request.json.get("first_name").lower()
    last_name = request.json.get("last_name").lower()
    email = request.json.get("email")
    password = request.json.get("password")

    try:
        email_check = User.objects(email=email).first()
    except:
        return jsonify(message="Check your credentials")


    if email_check:
        return jsonify({"message": "email already exists"}), 401

    try:
        user = User(first_name=first_name, email=email, last_name=last_name, password=generate_password_hash(password))
        user.save()
    except:
        return jsonify(message="Check your credentials")

    access_token = create_access_token(identity=email)
    return jsonify(message="registration successful")



@app.route("/login", methods=["POST"])
def login():
    """
        Route to login user. Pass in email and password 
        as json from url endpoint using POST request method, 
        validates user and returns a jwt upon validation
    """

    email = request.json.get("email")
    password = request.json.get("password")

    user = User.objects(email=email).first()

    if not user:
        return jsonify({"message": "user does not exist"}), 401

    
    confirm_password = check_password_hash(user.password, password)

    if email and confirm_password:
        access_token = create_access_token(identity=user.email)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"message": "incorrect username or password"}), 401