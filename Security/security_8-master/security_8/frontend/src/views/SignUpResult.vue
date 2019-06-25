<template>
 <div class="container">
    <div class="card login">
      <div class="card-body">
        <h5 class="card-title text-center"> Register Success.</h5>
        <form @submit.prevent="ChatList" class="text-center">
          <button v-on:click="toLogin" class="btn btn-primary">Go to Login Page</button>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'default',
  data () {
    return {
      name: ""
    }
  },
  methods: {
    toLogin() {
        this.$router.push({ name: "Login", params: { name: this.name } });
    }
  }
}
</script>


<style scoped>
</style>
