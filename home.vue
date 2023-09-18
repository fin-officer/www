<template>
  <div>
    <h1>Special Offer</h1>
    <p>Join our newsletter to stay updated!</p>
    <input v-model="email" placeholder="Your email" />
    <button @click="subscribe">Subscribe</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      email: ''
    }
  },
  methods: {
    subscribe() {
      axios.post('/api/subscribe', {
        email: this.email
      }).then(response => {
        console.log(response);
      }).catch(error => {
        console.error(error);
      });
    }
  }
}
</script>
