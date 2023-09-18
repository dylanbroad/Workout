const BASE_URL = 'http://localhost:5000';

// Helper function for making GET requests
async function get(endpoint) {
  const response = await fetch(`${BASE_URL}${endpoint}`);
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return response.json();
}

// Helper function for making POST requests with JSON data
async function post(endpoint, data) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return response.json();
}

// Fetch all workouts
export function fetchWorkouts() {
    return get('/workout/all');
  }
  
  // Fetch exercises for a specific workout
  export function fetchExercises(workoutId) {
    return get(`/workout/exercises/${workoutId}/`);
  }
  
  export function fetchSets(workoutId, exerciseId, setId) {
    return get(`/workout/exercises/sets/${workoutId}/${exerciseId}/${setId}`);
  }
  // Create a new workout
  export function createWorkout(title) {
    return post('/workout', { title });
  }
  
  // Create a new exercise for a workout
  export function createExercise(workoutId, exerciseId, exerciseName) {
    return post(`/workout/exercises/${workoutId}/${exerciseId}`, { exercise_name: exerciseName });
  }

  export function createSets(workoutId, exerciseId, reps, weight) {
    return post(`/workout/exercises/sets/${workoutId}/${exerciseId}`, { reps: reps}, { weight: weight});
  }
