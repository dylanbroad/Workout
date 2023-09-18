from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from datetime import datetime
import os

app = Flask("WorkoutAPI")
api = Api(app)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

CORS(app, origins=["http://localhost:3000"])

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db       
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Workout Model
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    exercises = db.relationship("Exercise", backref="workout")

    def __init__(self, title):
        self.title = title

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
    exercise_name = db.Column(db.String(100), nullable=False)
    sets = db.relationship("Sets", backref="exercise")
    
    def __init__(self, exercise_name, workout_id):
        self.exercise_name = exercise_name
        self.workout_id = workout_id


class Sets(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)

    def __init__(self, reps, weight, exercise_id):
        self.reps = reps
        self.weight = weight
        self.exercise_id = exercise_id

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

db.create_all()
Workout_schema = WorkoutSchema()
Exercies_schema = ExerciseSchema()
Sets_schema = SetsSchema()

@app.route('/workout', methods=['POST'])
def post_workout():
    args = parser.parse_args()
    title = args['title']

    new_workout = Workout(title = title)
    db.session.add(new_workout)
    db.session.commit()

    serialized_workout = Workout_schema.dump(new_workout)
    return jsonify(serialized_workout), 201

@app.route('/workout/<workout_id>', methods=['GET'])
def get_workout(workout_id):
    if workout_id == "all":
        # Return all workouts
        workouts = Workout.query.all()
        serialized_workouts = [Workout_schema.dump(workout) for workout in workouts]
        return jsonify(serialized_workouts)
    
    # Find a specific workout by ID
    workout = Workout.query.get(workout_id)
    if not workout:
        abort(404, message=f"Workout with ID {workout_id} not found")

    # Serialize and return the specific workout
    serialized_workout = Workout_schema.dump(workout)
    return jsonify(serialized_workout)

@app.route('/workout/<workout_id>', methods=["DELETE"])
def delete_workout(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        abort(404, message=f"Workout with ID {workout_id} not found")
    db.session.delete(workout)
    db.session.commit()

    return jsonify({"message": f"Workout with ID {workout_id} has been deleted"}), 200
    
@app.route('/workout/exercises/<workout_id>/<exercise_id>', methods=["GET"])
def get_exercise(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    
    if exercise_id == "all":
        if not workout:
            abort(404, message=f"Workout with ID {workout_id} not found")

        exercises = Exercise.query.filter_by(workout_id=workout.id).all()
        serialized_exercises = [ExerciseSchema().dump(exercise) for exercise in exercises]
        return jsonify(serialized_exercises)
    
    exercise = Exercise.query.get(exercise_id)

    if not workout:
        abort(404, message=f"Workout with ID {workout_id} not found")

    if not exercise or exercise.workout_id != workout.id:
        abort(404, message=f"Exercise with ID {exercise_id} not found in Workout with ID {workout_id}")

    serialized_exercise = ExerciseSchema().dump(exercise)
    return jsonify(serialized_exercise)

@app.route('/workout/exercises/<workout_id>', methods=["POST"])
def post_exercise(workout_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        abort(404, message=f"Workout with ID {workout_id} not found")

    # Use request.get_json() to parse JSON data from the request body
    data = request.get_json()
    exercise_name = data.get('exercise_name')

    new_exercise = Exercise(exercise_name=exercise_name, workout_id=workout.id)
    db.session.add(new_exercise)
    db.session.commit()

    serialized_exercise = ExerciseSchema().dump(new_exercise)
    return jsonify(serialized_exercise), 201

@app.route('/workout/exercises/<workout_id>/<exercise_id>', methods=["DELETE"])
def delete_exercise(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    if not workout:
        abort(404, message=f"Workout with ID {workout_id} not found")

    if not exercise or exercise.workout_id != workout.id:
        abort(404, message=f"Exercise with ID {exercise_id} not found in Workout with ID {workout_id}")        

    db.session.delete(exercise)
    db.session.commit()

    return jsonify({"message": f"Exercise with ID {exercise_id} has been deleted"}), 200

@app.route('/workout/exercises/sets/<workout_id>/<exercise_id>', methods=['POST'])
def post_set(workout_id, exercise_id):
    exercise = Exercise.query.filter_by(workout_id=workout_id, id=exercise_id).first()

    if not exercise:
        abort(404, message=f"Exercise with ID {exercise_id} not found in Workout with ID {workout_id}")        

    data = request.get_json()
    reps = data.get('reps')
    weight = data.get('weight')

    new_set = Sets(reps = reps, weight = weight, exercise_id=exercise.id)
    db.session.add(new_set)
    db.session.commit()

    serialized_set = SetsSchema().dump(new_set)
    return jsonify(serialized_set), 201

@app.route('/workout/exercises/sets/<workout_id>/<exercise_id>/<set_id>', methods=["GET"])
def get_set(workout_id, exercise_id, set_id):
    exercise = Exercise.query.filter_by(workout_id=workout_id, id=exercise_id).first()
    if set_id == "all":
        sets = Sets.query.filter_by(exercise_id=exercise.id).all()
        serialized_sets = [SetsSchema().dump(set) for set in sets]
        return jsonify(serialized_sets)
    
    sets = Sets.query.get(set_id)

    if not exercise:
        abort(404, message=f"Exercise with ID {exercise_id} not found in Workout with ID {workout_id}")

    serialized_sets = SetsSchema().dump(sets)
    return jsonify(serialized_sets)

@app.route('/workout/exercises/sets/<workout_id>/<exercise_id>/<set_id>', methods=["DELETE"])
def delete_set(workout_id, exercise_id, set_id):
    exercise = Exercise.query.filter_by(workout_id=workout_id, id=exercise_id).first()
    set = Sets.query.get(set_id)
    if not exercise:
        abort(404, message=f"Exercise with ID {exercise_id} not found in Workout with ID {workout_id}")        
    db.session.delete(set)
    db.session.commit()

    return jsonify({"message": f"Set with ID {set_id} has been deleted"}), 200

if __name__ == '__main__':
    app.run()