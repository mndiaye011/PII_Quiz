<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService';

const username = ref('');
const errorMessage = ref('');
const router = useRouter();

function launchNewQuiz() {
  console.log("Launch new quiz with", username.value);
  if (!username.value.trim()) {
    errorMessage.value = 'Veuillez entrer votre username avant de commencer le quiz.';
    return;
  }
  participationStorageService.savePlayerName(username.value);
  router.push('/questions');
}
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 70vh; /* S'assure que le conteneur prend toute la hauteur de la page */
}

form {
  width: 100%;
}

.mb-3 {
  width: 100%;
}

button {
  width: 100%;
}
</style>

<template>
  <div class="container">
    <h1>Démarrer un nouveau quiz</h1>
    <form>
      <div class="mb-3">
        <label for="username" class="form-label">Entrer votre nom</label>
        <input type="text" class="form-control" id="username" v-model="username" placeholder="nom"/>
      </div>
      <button type="button" class="btn btn-primary" @click="launchNewQuiz">Commencer</button>
    </form>
    <br>
    <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
  </div>
</template>
