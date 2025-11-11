<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">Username:</label>
        <input id="username" v-model="username" />
      </div>
      <div>
        <label for="password">Password:</label>
        <input id="password" v-model="password" type="password" />
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

