<template>
  <div class="container">
    <div class="card login">
      <div class="card-body">
        <h2 class="card-title text-center">Login</h2>
        <form @submit.prevent="login" class="text-center">
          <div class="form-group">
            <input
              type="text"
              class="form-control"
              placeholder="ID"
              name="name"
              v-model="name"
            />
            <p v-if="errorText" class="text-danger">{{ errorText1 }}</p>
            <p></p>
            <input
              type="password"
              class="form-control"
              placeholder="Password"
              name="password"
              v-model="password"
            />
            <p v-if="errorText" class="text-danger">{{ errorText2 }}</p>
          </div>
          <button type="submit" class="btn btn-primary">Login</button>
          <p></p>
          <router-link to="/signup" class="btn btn-link">Register</router-link>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "login",
  date() {
    return {
      name: "",
      password:"",
      errorText: null
    };
  },
  methods: {
    login() {
      if (this.name && this.password) { 
        this.$router.push({ name: "Chat", params: { name: this.name } });
      } else if (this.name){
        this.errorText2 = "Please Enter a Password!";
      } else {
        this.errorText1 = "Please Enter a name first!";
      }
    },
    signup(){
      this.$router.push({ name: "SignUp", params: { name: this.name } });
    }
  }
};
</script>

<style>
.login {
  max-width: 450px;
  margin-top: 50px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>
