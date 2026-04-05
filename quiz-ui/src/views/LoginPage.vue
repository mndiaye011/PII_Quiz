<template>
  <div class="page-center fade-up">
    <div class="login-emoji">{{ isRegister ? '📝' : '👤' }}</div>
    <div class="form-card card">
      <div class="toggle-tabs">
        <button :class="{ active: !isRegister }" @click="isRegister = false">Connexion</button>
        <button :class="{ active: isRegister }" @click="isRegister = true">Inscription</button>
      </div>
      <h1 class="form-title">{{ isRegister ? 'Créer un compte' : 'Bon retour !' }}</h1>
      <div class="field">
        <label class="field-label">Pseudo</label>
        <input class="input-field" type="text" v-model="username" placeholder="Ton pseudo" @keyup.enter="submit" />
      </div>
      <div class="field">
        <label class="field-label">Mot de passe</label>
        <input class="input-field" type="password" v-model="password" placeholder="••••••••" @keyup.enter="submit" />
      </div>
      <p v-if="errorMessage" class="error-msg">⚠️ {{ errorMessage }}</p>
      <button class="btn-navy" @click="submit">
        {{ isRegister ? 'Créer mon compte' : 'Se connecter' }}
      </button>
      <p class="skip-link" @click="$router.push('/select-quiz')">
        Continuer sans compte →
      </p>
    </div>
  </div>
</template>

<script>
import quizApiService from '@/services/QuizApiService';
import userStorageService from '@/services/UserStorageService';

export default {
  data() {
    return { username: '', password: '', errorMessage: '', isRegister: false };
  },
  methods: {
    async submit() {
      if (!this.username.trim() || !this.password.trim()) {
        this.errorMessage = 'Remplis tous les champs.';
        return;
      }
      try {
        let response;
        if (this.isRegister) {
          response = await quizApiService.registerUser({ username: this.username, password: this.password });
        } else {
          response = await quizApiService.loginUser({ username: this.username, password: this.password });
        }
        userStorageService.saveUser(response.data);
        this.$router.push('/select-quiz');
      } catch (e) {
        this.errorMessage = this.isRegister ? 'Ce pseudo est déjà pris.' : 'Pseudo ou mot de passe incorrect.';
      }
    },
  },
};
</script>

<style scoped>
.login-emoji { font-size: 80px; text-align: center; margin-bottom: 16px; animation: bob 3s ease-in-out infinite; }
@keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
.form-card { width: 100%; max-width: 420px; display: flex; flex-direction: column; gap: 16px; }
.toggle-tabs { display: flex; border-radius: var(--radius); overflow: hidden; border: 1.5px solid var(--border); }
.toggle-tabs button {
  flex: 1; padding: 10px; border: none; background: var(--off-white);
  font-family: var(--font); font-size: 14px; font-weight: 700;
  color: var(--text-mid); cursor: pointer; transition: all 0.2s;
}
.toggle-tabs button.active { background: var(--navy); color: white; }
.form-title { font-size: 1.3rem; font-weight: 900; text-align: center; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field-label { font-size: 13px; font-weight: 700; color: var(--text-mid); }
.error-msg { color: #d63030; font-size: 13px; font-weight: 600; }
.skip-link { text-align: center; font-size: 13px; color: var(--text-light); cursor: pointer; font-weight: 600; }
.skip-link:hover { color: var(--navy); }
</style>