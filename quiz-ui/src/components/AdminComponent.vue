<script setup>
import QuestionList from "./QuestionList.vue";

</script>

<template>

  <div class="container-sm ">


    <!-- Connexion pour les non-administrateurs -->
    <div v-if="!adminMode" class="login-wrapper p-4">
      <h2>Connexion</h2>
      <br>
      <input type="password" v-model="password" placeholder="Mot de passe" class="form-control mb-3">
      <button class="btn btn-success" type="button" @click="checkPassword">Connexion</button>
      <p v-if="errorLogin" class="text-danger mt-2">Erreur d'identifiant</p>
    </div>

    <!-- Affichage pour les administrateurs connectés -->
    <div v-if="adminMode" class="admin-panel p-4">
      <QuestionList />
      <button class="btn btn-primary mt-3" type="button" @click="logout">Déconnexion</button>
    </div>

  </div>
</template>

<style scoped>
.container-sm {
  max-width: 500px;
  margin: 0 auto;
  padding-top: 20px;
}

.login-wrapper,
.admin-panel {
  background: #f8f9fa;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

.form-control {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
}

.btn {
  width: 100%;
}

.text-danger {
  color: #dc3545;
}
</style>



<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorageServices";
export default {
  data() {
    return {
      errorLogin: false,
      password: '',
      adminMode: false,
    }
  },
  methods: {
    async checkPassword() {
      let response = await quizApiService.login({ password: this.password });
      if (response && response.status === 200) {
        this.errorLogin = false;
        this.adminMode = true;
        adminStorageService.saveToken(response.data.token);
      } else {
        this.errorLogin = true;
      }
    },

    logout() {
      adminStorageService.clear();
      this.adminMode = false;
    }
  },
}

</script>