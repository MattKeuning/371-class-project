<template>
  <div>
    <h2>Edit Profile</h2>
    <form @submit.prevent="saveProfile">
      <div>
        <label for="name">Name:</label>
        <input id="name" v-model="profile.name" type="text" required />
      </div>
      <div>
        <label for="email">Email:</label>
        <input id="email" v-model="profile.email" type="email" required />
      </div>
      <div>
        <label for="age">Age:</label>
        <input id="age" v-model.number="profile.age" type="number" required />
      </div>
      <button type="submit">Save</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const profile = ref({
  name: '',
  email: '',
  age: null
})

const loadProfile = async () => {
  try {
    const response = await fetch('/api/profiles/me')
    if (response.ok) {
      profile.value = await response.json()
    }
  } catch (error) {
    console.error('Error loading profile:', error)
  }
}

const saveProfile = async () => {
  try {
    const response = await fetch('/api/profiles/me', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(profile.value)
    })
    if (response.ok) {
      alert('Profile updated successfully')
    } else {
      alert('Error updating profile')
    }
  } catch (error) {
    console.error('Error saving profile:', error)
  }
}

onMounted(loadProfile)
</script>

<style scoped>
form {
  max-width: 400px;
  margin: 0 auto;
}

div {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  padding: 10px 20px;
  background-color: #42b883;
  color: white;
  border: none;
  cursor: pointer;
}
</style>