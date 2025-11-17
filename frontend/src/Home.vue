<script setup>
import { ref } from "vue";

const workouts = ref([]);

const exerciseName = ref("");
const sets = ref("");
const reps = ref("");
const weight = ref("");
const unit = ref("Reps");

const currentWorkout = ref(null);

function ensureWorkout() {
  if (!currentWorkout.value) {
    currentWorkout.value = {
      id: Date.now(),
      name: "Workout", 
      date: new Date().toLocaleDateString(),
      exercises: [],
      expanded: true
    };
    workouts.value.unshift(currentWorkout.value);
  }
}

function addExercise() {
  if (!exerciseName.value.trim()) return;

  ensureWorkout();

  currentWorkout.value.exercises.push({
    id: Date.now(),
    name: exerciseName.value,
    sets: sets.value,
    amount: reps.value,
    unit: unit.value,
    weight: weight.value
  });

  exerciseName.value = "";
  sets.value = "";
  reps.value = "";
  weight.value = "";
  unit.value = "Reps";
}

function toggleWorkout(workout) {
  workout.expanded = !workout.expanded;
}

function renameWorkout(workout, event) {
  workout.name = event.target.value;
}
</script>


<template>
  <div class="container">
    <!-- Add Exercise Section -->
    <section class="add-section">
      <h2>Add Exercise</h2>

      <div class="inputs">
        <input v-model="exerciseName" placeholder="Exercise Name" />
        <input v-model="sets" placeholder="Sets" type="number" />
        <div class="rep-time-input">
          <input v-model="reps" placeholder="Amount" type="number" />
          <select v-model="unit" class="input-select">
            <option value="Reps">Reps</option>
            <option value="seconds">Seconds</option>
          </select>
        </div>
        <input v-model="weight" placeholder="Weight (lbs)" type="number" />
      </div>

      <button @click="addExercise" class="btn">Add Exercise</button>
    </section>

    <hr />

    <!-- Workout History -->
    <section class="history-section">
      <h2>Workout History</h2>

      <div v-for="workout in workouts" :key="workout.id" class="workout">
        <div class="workout-header" @click="toggleWorkout(workout)">
          
          <input
            class="workout-name"
            :value="workout.name"
            @input="renameWorkout(workout, $event)"
          />

          <span class="date">{{ workout.date }}</span>
          <span class="arrow">{{ workout.expanded ? "▲" : "▼" }}</span>
        </div>

        <div v-if="workout.expanded" class="exercise-list">
          <div
            v-for="exercise in workout.exercises"
            :key="exercise.id"
            class="exercise"
          >
            <strong>{{ exercise.name }}</strong> —
            {{ exercise.sets }} × {{ exercise.amount }} {{ exercise.unit }}
            <span v-if="exercise.weight"> @ {{ exercise.weight }} lbs</span>


          </div>
        </div>
      </div>
    </section>
  </div>
</template>


<style scoped>
.container {
  max-width: 600px;
  margin: 40px auto;
  padding: 10px;
  font-family: sans-serif;
}

h2 {
  text-align: left;
  margin-bottom: 10px;
}

.inputs {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

input {
  padding: 8px;
  flex: 1;
  min-width: 130px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

select {
  padding: 8px;
  flex: 1;
  min-width: 130px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: white;
  appearance: none;
  color: #a3a3aa;

}


.btn {
  margin-top: 10px;
  background: #4c6ef5;
  color: white;
  padding: 10px;
  width: 100%;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background: #3b5bdb;
}

.workout {
  background: #f4f4f4;
  padding: 12px;
  border-radius: 8px;
  margin-top: 15px;
}

.workout-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.workout-name {
  border: none;
  background: none;
  font-weight: bold;
  font-size: 1.1em;
  width: 50%;
}

.workout-name:focus {
  outline: 1px solid #ccc;
  background: #fff;
}

.date {
  font-size: 0.9em;
  color: #666;
}

.exercise-list {
  margin-top: 10px;
}

.exercise {
  padding: 5px 0;
  border-bottom: 1px solid #ddd;
}

.arrow {
  font-size: 18px;
  padding-left: 10px;
}

.rep-time-input {
  display: flex;
  gap: 10px;  
  flex: 1;
}


</style>



