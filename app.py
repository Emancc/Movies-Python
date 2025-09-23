from flask import Flask, render_template, request
from models import(
    db,
    User,
    Movie,
)
from schemas import UserSchema
from marshmallow import ValidationError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://BD2021:BD2021itec@143.198.156.171:3306/movies_pp1'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/users', methods=['POST', 'GET'])
def Users():
    if request.method == 'POST':
        try:
           data = UserSchema().load(request.json)
        except ValidationError as err:
            return{"Mensaje": f"Error en la particion {err}"}
        new_user = User(name=data.get('name'), email=data.get('email'))
        db.session.add(new_user)
        db.session.commit()
        return UserSchema().dump(new_user)
    users = User.query.all()
    return UserSchema(many=True).dump(users)

@app.route('/users/<int:id>',methods=['GET','PATCH','PUT','DELETE'])
def user(id):
    user=User.query.get_or_404(id)
    if request.method == 'PUT':
        try:
           data = UserSchema().load(request.json)
        except ValidationError as err:
            return {"Error": err.messages}
        
        user.name = data['name']
        user.email = data['email']
        db.session.commit()

    if request.method == 'PATCH':
        try:
           data = UserSchema().load(request.json)
        except ValidationError as err:
            return {"Error": err.messages}
        
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email =data['email']
        db.session.commit()

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return {"Message":"Deleted User"}, 204
        
    return UserSchema().dump(user)

@app.route('/movies')
def Movies():
    movies = Movie.query.all()
    return [
        {
            "title": movie.title,
            "year": movie.year,
            #"gerne": movie.genres,     <---estos se rompen porque vienen de una clave foranea de otra tabla.
        }for movie in movies
    ]


if __name__ == '__main__':
    app.run(debug=True,port=5000)