<template>
  <div>
    <h1>Login</h1>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="login">Login</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login() {
      axios.post('/api/login', {
        username: this.username,
        password: this.password
      }).then(response => {
        console.log(response);
      }).catch(error => {
        console.error(error);
      });
    }
  }
}
</script>
