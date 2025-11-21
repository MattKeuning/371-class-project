<script setup>
import { ref, nextTick, computed } from "vue";


const workouts = ref([]);
const templates = ref([]);
const completedWorkouts = ref([]);

const exerciseName = ref("");
const sets = ref("");
const reps = ref("");
const weight = ref("");
const unit = ref("reps");

const currentWorkout = ref(null);
const templateName = ref("");
const editingIndex = ref(null);

const showHistory = ref(false);

const allChecked = computed(() => {
  if (!currentWorkout.value) return false;
  return currentWorkout.value.exercises.length > 0 &&
         currentWorkout.value.exercises.every(ex => ex.completed === true);
});


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

  const updatedExercise = {
    id: Date.now(),
    name: exerciseName.value,
    sets: sets.value,
    amount: reps.value,
    unit: unit.value.toLowerCase(),
    weight: weight.value,
    completed: false
  };

  if (editingIndex.value !== null) {
    currentWorkout.value.exercises.splice(editingIndex.value, 1, updatedExercise);
    editingIndex.value = null; 
  } else {
    currentWorkout.value.exercises.push(updatedExercise);
  }

  exerciseName.value = "";
  sets.value = "";
  reps.value = "";
  weight.value = "";
  unit.value = "reps";
}



function saveWorkout() {
  if (!currentWorkout.value || currentWorkout.value.exercises.length === 0) {
    alert("Cannot save an empty or non-existent workout.");
    return;
  }
  
  const name = templateName.value.trim() || "New Template";

  const newTemplate = {
    id: Date.now(),
    name: name,
    exercises: JSON.parse(JSON.stringify(currentWorkout.value.exercises)) // Deep copy exercises
  };
  
  templates.value.push(newTemplate);
  templateName.value = ""; 
  
  alert(`Workout "${name}" saved to templates!`);
}

function loadWorkout(template) {

  if (currentWorkout.value) {
    workouts.value = workouts.value.filter(w => w.id !== currentWorkout.value.id);
  }

  const loadedExercises = JSON.parse(JSON.stringify(template.exercises));

loadedExercises.forEach(ex => {
  ex.completed = false;
});

currentWorkout.value = {
  id: Date.now(),
  name: template.name + " (Loaded)",
  date: new Date().toLocaleDateString(),
  exercises: loadedExercises,
  expanded: true
};
  if (!workouts.value.find(w => w.id === currentWorkout.value.id)) {
     workouts.value.unshift(currentWorkout.value);
  }
  
  alert(`Loaded workout: ${currentWorkout.value.name}`);
}


function editExercise(exercise, index) {
  exerciseName.value = exercise.name;
  sets.value = exercise.sets;
  reps.value = exercise.amount;
  unit.value = exercise.unit.toLowerCase();
  weight.value = exercise.weight;

  editingIndex.value = index; 
}


function toggleWorkout(workout) {
  workout.expanded = !workout.expanded;
}

function renameWorkout(workout, event) {
  workout.name = event.target.value;
}

function toggleComplete(index) {
  const ex = currentWorkout.value.exercises[index];
  ex.completed = !ex.completed;
}

function deleteExercise(index) {
  const ex = currentWorkout.value.exercises[index];

  const confirmDelete = confirm(`Delete "${ex.name}"?`);

  if (!confirmDelete) return;

  currentWorkout.value.exercises.splice(index, 1);
}

function finishWorkout() {
  if (!currentWorkout.value) return;

  const finished = {
    id: Date.now(),
    name: currentWorkout.value.name,
    date: new Date().toLocaleDateString(),
    exercises: JSON.parse(JSON.stringify(currentWorkout.value.exercises))
  };

  completedWorkouts.value.unshift(finished);

  currentWorkout.value = null;

  alert("Workout completed and added to history!");
}


function saveTemplateFromHistory(workout) {
  const name = prompt("Template name:", workout.name);
  if (!name) return;

  const newTemplate = {
    id: Date.now(),
    name: name.trim(),
    exercises: JSON.parse(JSON.stringify(workout.exercises))
  };

  const exists = templates.value.some(t =>
    templatesAreEqual(t, newTemplate)
  );

  if (exists) {
    alert("This template already exists.");
    return;
  }

  templates.value.push(newTemplate);
  alert(`Saved "${name}" as a template!`);
}


function deleteTemplate(id) {
  const confirmDelete = confirm("Delete this template?");

  if (!confirmDelete) return;

  templates.value = templates.value.filter(t => t.id !== id);
}


function templatesAreEqual(a, b) {
  if (a.exercises.length !== b.exercises.length) return false;

  const sortKey = ex =>
    `${ex.sets}-${ex.amount}-${ex.unit}-${ex.weight}`;

  const sortedA = [...a.exercises].sort((x, y) => sortKey(x).localeCompare(sortKey(y)));
  const sortedB = [...b.exercises].sort((x, y) => sortKey(x).localeCompare(sortKey(y)));

  for (let i = 0; i < sortedA.length; i++) {
    const exA = sortedA[i];
    const exB = sortedB[i];

    if (
      exA.sets !== exB.sets ||
      exA.amount !== exB.amount ||
      exA.unit !== exB.unit ||
      exA.weight !== exB.weight
    ) {
      return false;
    }
  }

  return true;
}

</script>


<template>
  <div class="container">
    <section class="add-section">
      <h2>Add Exercise</h2>

      <div class="inputs">
        <input v-model="exerciseName" placeholder="Exercise Name" />
        <input v-model="sets" placeholder="Sets" type="number" />
        <div class="rep-time-input">
          <input v-model="reps" placeholder="Amount" type="number" />
          <select v-model="unit" class="input-select">
            <option value="reps">Reps</option>
            <option value="seconds">Seconds</option>
          </select>
        </div>
        <input v-model="weight" placeholder="Weight (lbs)" type="number" />
      </div>

      <button @click="addExercise" class="btn">Add Exercise</button>
    </section>


<section class="current-workout-section" v-if="currentWorkout">
  <h2>Current Workout</h2>

  <div class="workout current-workout-box">
    <div class="workout-header">
      <input
        class="workout-name"
        :value="currentWorkout.name"
        @input="renameWorkout(currentWorkout, $event)"
      />
      <span class="date">{{ currentWorkout.date }}</span>
    </div>

    <div class="exercise-list">
      <div
        v-for="(exercise, index) in currentWorkout.exercises"
        :key="exercise.id"
        class="exercise-row"
      >
        <div
          class="exercise-info"
          :class="{ completed: exercise.completed }"
          @click="editExercise(exercise, index)"
        >
          <strong>{{ exercise.name }}</strong> —
          {{ exercise.sets }} × {{ exercise.amount }} {{ exercise.unit }}
          <span v-if="exercise.weight"> @ {{ exercise.weight }} lbs</span>
        </div>

        <div class="exercise-actions">
          <button class="icon-btn" @click.stop="toggleComplete(index)">✔</button>
          <button class="icon-btn delete" @click.stop="deleteExercise(index)">🗑</button>
        </div>
      </div>
      <div v-if="allChecked" class="complete-actions">
        <button class="btn" @click="finishWorkout">Complete Workout and add to History ✔</button>
      </div>
    </div>
  </div>
</section>
    <section class="templates-section">
  <h2 v-if="templates.length > 0">Saved Templates</h2>

  <div
    v-for="template in templates"
    :key="template.id"
    class="workout"
  >
    <div class="workout-header">
      <strong>{{ template.name }}</strong>

      <div style="display: flex; gap: 10px;">
        <button class="btn-inline" @click="loadWorkout(template)">
  Load as Current Workout
</button>

<button class="btn-inline delete-btn" @click.stop="deleteTemplate(template.id)">
  Delete
</button>

      </div>
    </div>

    <div class="exercise-list">
      <div
        v-for="ex in template.exercises"
        :key="ex.id"
        class="exercise"
      >
        <strong>{{ ex.name }}</strong> —
        {{ ex.sets }} × {{ ex.amount }} {{ ex.unit }}
        <span v-if="ex.weight"> @ {{ ex.weight }} lbs</span>
      </div>
    </div>
  </div>
</section>



    <button
  class="btn"
    style="margin-top: 50px;"
    @click="showHistory = !showHistory"
    >
    {{ showHistory ? "Hide Workout History" : "Show Workout History" }}
    </button>



    <section class="history-section" v-if="showHistory && completedWorkouts.length > 0">
  <h2>Workout History</h2>

  <div
    v-for="workout in completedWorkouts"
    :key="workout.id"
    class="workout"
  >
    <div class="workout-header">
      <strong>{{ workout.name }}</strong>
      <span class="date">{{ workout.date }}</span>
    </div>

    <div class="exercise-list">
      <div
        v-for="ex in workout.exercises"
        :key="ex.id"
        class="exercise"
      >
        <strong>{{ ex.name }}</strong> —
        {{ ex.sets }} × {{ ex.amount }} {{ ex.unit }}
        <span v-if="ex.weight"> @ {{ ex.weight }} lbs</span>
      </div>

      <button
        class="btn small-btn"
        style="margin-top: 10px;"
        @click="saveTemplateFromHistory(workout)"
      >
        Save as Template
      </button>

    </div>
  </div>
</section>

<p v-if="showHistory && completedWorkouts.length === 0" style="color:#666; text-align:center; margin-top:15px;">
  No workout history yet.
</p>



  </div>
</template>


<style scoped>


.primary-btn {
  background: #4c6ef5;
  color: white;
}

.primary-btn:hover {
  background: #3b5bdb;
}

.save-btn {
  flex: 1;
  min-width: 130px;
  background: #7950f2;
  color: white;
}

.save-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.save-btn:hover:not(:disabled) {
  background: #5f3dc4;
}

.current-workout-section {
  padding: 10px 0;
  border-bottom: 2px solid #ccc;
  margin-bottom: 20px;
}

.current-workout-box {
  background: #e8f9e8;
  border: 5px solid #b6e6b6;
  border-radius: 10px;
  padding: 15px;
}

.templates-section {
  margin-top: 20px;
}

.templates-section .workout-header strong {
  margin-right: 15px;
}


.save-section .inputs {
  align-items: center;
}

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




.exercise-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid #ddd;
}

.exercise-info {
  flex: 1;
  cursor: pointer;
}

.exercise-info.completed {
  color: green;
  text-decoration: line-through;
}

.exercise-actions {
  display: flex;
  gap: 8px;
}

.icon-btn {
  background: #eee;
  border: none;
  padding: 4px 8px;
  border-radius: 5px;
  cursor: pointer;
}

.icon-btn:hover {
  background: #ddd;
}

.icon-btn.delete {
  background: #f88;
}

.icon-btn.delete:hover {
  background: #e44;
}

.delete-btn {
  background: #f44336;
  color: white;
}

.delete-btn:hover {
  background: #d32f2f;
}


.template-load-btn {
  padding: 10px 18px;   
  min-width: 160px;     
  width: auto !important;
  white-space: nowrap;
  font-size: 0.9rem;
}


.btn-inline {
  background: #4c6ef5;
  color: white;
  padding: 10px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  white-space: nowrap;
  width: auto;
}

.btn-inline:hover {
  background: #3b5bdb;
}

.btn-inline.delete-btn {
  background: #e44;
}

.btn-inline.delete-btn:hover {
  background: #c33;
}

</style>



