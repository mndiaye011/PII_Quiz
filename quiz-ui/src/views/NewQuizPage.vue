<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService';

const username = ref('');
const errorMessage = ref('');
const router = useRouter();

function launchNewQuiz() {
  if (!username.value.trim()) {
    errorMessage.value = 'Veuillez entrer votre pseudo avant de commencer.';
    return;
  }
  participationStorageService.savePlayerName(username.value);
  router.push('/questions');
}
</script>

<template>
  <div class="page-center fade-up">
    <div class="hero-emoji">😤</div>
    <div class="form-card card">
      <h1 class="form-title">Prêt à relever le défi ?</h1>
      <p class="form-sub">Choisis un pseudo pour commencer</p>
      <div class="field">
        <label class="field-label">Votre pseudo</label>
        <input
          class="input-field"
          type="text"
          v-model="username"
          placeholder="Jean Michel"
          @keyup.enter="launchNewQuiz"
        />
      </div>
      <p v-if="errorMessage" class="error-msg">⚠️ {{ errorMessage }}</p>
      <button class="btn-navy" @click="launchNewQuiz">Démarrer le quiz</button>
    </div>
  </div>
</template>

<style scoped>
.hero-emoji {
  font-size: 110px;
  line-height: 1;
  margin-bottom: 20px;
  animation: bob 3s ease-in-out infinite;
}
@keyframes bob {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
.form-card {
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.form-title {
  font-size: 1.4rem;
  font-weight: 900;
  color: var(--text-dark);
  text-align: center;
}
.form-sub {
  color: var(--text-mid);
  font-size: 14px;
  text-align: center;
  margin-top: -8px;
}
.field { display: flex; flex-direction: column; gap: 6px; }
.field-label { font-size: 13px; font-weight: 700; color: var(--text-mid); }
.error-msg { color: #d63030; font-size: 13px; font-weight: 600; }
</style>
