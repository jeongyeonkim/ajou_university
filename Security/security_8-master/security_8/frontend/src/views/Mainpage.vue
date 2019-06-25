<template>
 <div class="container">
    <div class="card login">
      <div class="card-body">
        <h2 class="card-title text-center">Security_chat</h2>
        <h5 class="card-title text-center"> </h5>
        <form @submit.prevent="ChatList" class="text-center">
          <span>{{name}}</span>
          <div class="headline">security chat_1
          </div>
          <!-- <router-link to="/Chat" class="btn btn-primary">Enter Chat</router-link> -->
          <button v-on:click="chat_1" class="btn btn-primary">Enter Chat</button>
          <p></p>
          <div class="headline">security chat_2
          </div>
          <button v-on:click="chat_2" class="btn btn-primary">Enter Chat</button>
          <p></p>
          <div class="headline">security chat_3
          </div>
          <button v-on:click="chat_2" class="btn btn-primary">Enter Chat</button>
          <p></p>
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
    chat_1() {
        this.$router.push({ name: "Chat", params: { name: this.name } });
    }
  }
}
</script>


<style scoped>
</style>
