<template>
  <div class="App">
    <header class="App-header">
      <img :src="logo" class="App-logo" alt="logo" />
      <p>
        Edit <code>src/App.vue</code> and save to reload.
      </p>
      <a
        class="App-link"
        href="https://vuejs.org"
        target="_blank"
        rel="noopener noreferrer"
      >
        Learn Vue
      </a>
    </header>
  </div>
</template>

<script setup>
import logo from './logo.svg'
</script>

<style scoped>
.App {
  text-align: center;
}

.App-logo {
  height: 40vmin;
  pointer-events: none;
}

@media (prefers-reduced-motion: no-preference) {
  .App-logo {
    animation: App-logo-spin infinite 20s linear;
  }
}

.App-header {
  background-color: #282c34;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: calc(10px + 2vmin);
  color: white;
}

.App-link {
  color: #61dafb;
}

@keyframes App-logo-spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>