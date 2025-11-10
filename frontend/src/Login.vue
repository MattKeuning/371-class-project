<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="login">
            <div>
                <label for="username">Username:</label>
                <input id="username" v-model="auth.username" type="text" required />
            </div>
            <div>
                <label for="password">Password:</label>
                <input id="password" v-model="auth.password" type="password" required />
            </div>
            <button type="submit">Login</button>
    </div>