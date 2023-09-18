import React, { useState, useEffect } from 'react';
import { fetchWorkouts, createWorkout, fetchExercises, createExercise, createSets } from  './components/APIservice';

function App() {
  const [workouts, setWorkouts] = useState([]);
  const [newWorkoutTitle, setNewWorkoutTitle] = useState('');

  useEffect(() => {
    // Fetch the list of workouts when the component mounts
    fetchWorkouts()
      .then((data) => {
        setWorkouts(data);
      })
      .catch((error) => {
        console.error('Error fetching workouts:', error);
      });
  }, []);

  const handleCreateWorkout = () => {
    // Create a new workout when the button is clicked
    createWorkout(newWorkoutTitle)
      .then((newWorkout) => {
        // Add the new workout to the list of workouts
        setWorkouts([...workouts, newWorkout]);
        setNewWorkoutTitle(''); // Clear the input field
      })
      .catch((error) => {
        console.error('Error creating workout:', error);
      });
  };

  return (
    <div>
      <h1>Workouts</h1>
      <ul>
        {workouts.map((workout) => (
          <li key={workout.id}>{workout.title}</li>
        ))}
      </ul>
      <input
        type="text"
        value={newWorkoutTitle}
        onChange={(e) => setNewWorkoutTitle(e.target.value)}
      />
      <button onClick={handleCreateWorkout}>Create Workout</button>
    </div>
  );
}

export default App