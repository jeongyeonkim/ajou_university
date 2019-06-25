<template>
  <div class="container">
    <div class="card login">
      <div class="card-body">
        <h2 class="card-title text-center">Sign Up</h2>
        <form @submit.prevent="signup" class="text-center">
          <div class="form-group">
            <input
              type="text"
              class="form-control"
              placeholder="Enter your ID"
              name="name"
              v-model="name"
            />
            <p></p>
            <input
              type="text"
              class="form-control"
              placeholder="Enter your Email"
              name="email"
              v-model="email"
            />
            <p></p>
            <input
              type="password"
              class="form-control"
              placeholder="Enter your Password"
              name="password"
              v-model="password"
            />
            <p></p>
            <input
              type="password"
              class="form-control"
              placeholder="Enter your Password Again"
              name="password_again"
              v-model="password_again"
            />
            <p v-if="errorText" class="text-danger">{{ errorText }}</p>
            
          </div>
          <button type="submit" class="btn btn-primary">Create Account</button>
          <p></p>
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
    signup() {
        this.$router.push({ name: "SignUpResult", params: { name: this.name } });
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
