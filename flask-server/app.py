from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime
import os

# Initialize app
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

CORS(app, origins=["http://localhost:3000"])

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db       
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Workout Class/Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    workouts = db.relationship("Workout", backref="users")

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    exercises = db.relationship("Exercise", backref="workout")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, date):
        self.title = title
        self.date = date

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
    exercise_name = db.Column(db.String(100), nullable=False)
    sets = db.relationship("Sets", backref="exercise")
    
    def __init__(self, exercise_name):
        self.exercise_name = exercise_name

class Sets(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    def __init__(self, reps, weight):
        self.reps = reps
        self.weight = weight


# Workout Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        include_fk = True

class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        include_fk = True
        model = Workout

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        include_fk = True

class SetsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sets
        include_fk = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

set_schema = SetsSchema()
sets_schema = SetsSchema(many=True)

# Create a Workout

@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()

    username = data['username']
    password = data['password']

    new_user = Users(username, password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/user/<user_id>/workouts', methods=['POST'])
def add_workout(user_id):

    user = Users.query.get(user_id)

    workoutData = request.get_json()

    title = workoutData['title']
    new_workout = Workout(title=title, date=datetime.now())
    user.workouts.append(new_workout)

    db.session.add(new_workout)
    db.session.commit()

    return workout_schema.jsonify(new_workout)

@app.route('/workouts/<workout_id>/exercises', methods=['POST'])
def add_exercises(workout_id):
    workout = Workout.query.get(workout_id)

    exerciseData = request.json

    exercise_name = exerciseData['exercise_name']

    new_exercise = Exercise(exercise_name)
    workout.exercises.append(new_exercise)

    db.session.add(new_exercise)
    db.session.commit()

    return exercise_schema.jsonify(new_exercise)

@app.route('/exercises/<exercise_id>/sets', methods=['Post'])
def add_sets(exercise_id):
    exercise = Exercise.query.get(exercise_id)

    reps = request.json['reps']
    weight = request.json['weight']

    new_set = Sets(reps, weight)
    exercise.sets.append(new_set)

    db.session.add(new_set)
    db.session.commit()

    return set_schema.jsonify(new_set)

# Get all Products
@app.route('/user', methods=['GET'])
def get_users():
    all_users = Users.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    single_user = Users.query.get(user_id)
    result = user_schema.dump(single_user)
    return jsonify(result)

@app.route('/user/<user_id>/workouts', methods=['GET'])
def get_user_workouts(user_id):
    user = Users.query.get(user_id)

    all_workouts = user.workouts
    result = workouts_schema.dump(all_workouts)
    return jsonify(result)

@app.route('/workouts/<workout_id>/exercises', methods=['GET'])
def get_exercises_for_workout(workout_id):
    workout = Workout.query.get(workout_id)

    all_exercises = workout.exercises
    result = exercises_schema.dump(all_exercises)
    return jsonify(result)

@app.route('/exercises/<exercise_id>/sets', methods=['GET'])
def get_sets_for_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)

    all_sets = exercise.sets
    result = sets_schema.dump(all_sets)
    return jsonify(result)

# Line Runs server in development mode
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)



