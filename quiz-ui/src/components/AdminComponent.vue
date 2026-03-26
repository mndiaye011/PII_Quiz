<template>
  <div class="page-center fade-up">
    <div v-if="!isAuthenticated" class="form-card card">
      <div class="admin-icon">🔐</div>
      <h1 class="form-title">Bonjour Admin</h1>
      <div class="field">
        <label class="field-label">Mot de passe</label>
        <input
          class="input-field"
          type="password"
          v-model="password"
          placeholder="••••••••"
          @keyup.enter="login"
        />
      </div>
      <p v-if="errorMessage" class="error-msg">⚠️ {{ errorMessage }}</p>
      <button class="btn-navy" @click="login">Se connecter</button>
    </div>

    <div v-else class="admin-panel">
      <div class="panel-header">
        <h2 class="panel-title">⚙️ Panneau d'administration</h2>
        <button class="btn-outline logout-btn" @click="logout">Déconnexion</button>
      </div>

      <!-- Onglets -->
      <div class="tabs">
        <button
          class="tab"
          :class="{ active: activeTab === 'questions' }"
          @click="activeTab = 'questions'"
        >
          📝 Questions
        </button>
        <button
          class="tab"
          :class="{ active: activeTab === 'quizzes' }"
          @click="activeTab = 'quizzes'"
        >
          🎯 Quiz
        </button>
      </div>

      <!-- Contenu selon l'onglet actif -->
      <div class="tab-content">
        <QuestionList v-if="activeTab === 'questions'" />
        <QuizList     v-if="activeTab === 'quizzes'" />
      </div>
    </div>
  </div>
</template>

<script>
import QuestionList from './QuestionList.vue';
import QuizList from './QuizList.vue';
import adminStorageService from '@/services/AdminStorageServices.js';
import quizApiService from '@/services/QuizApiService.js';

export default {
  components: { QuestionList, QuizList },
  data() {
    return {
      password: '',
      errorMessage: '',
      isAuthenticated: !!adminStorageService.getToken(),
      activeTab: 'questions', // onglet ouvert par défaut
    };
  },
  methods: {
    async login() {
      try {
        const response = await quizApiService.login(this.password); // envoie { password }
        adminStorageService.saveToken(response.data.token);          // sauvegarde le JWT
        this.isAuthenticated = true;
        this.errorMessage = '';
      } catch {
        this.errorMessage = 'Mot de passe incorrect.';
      }
    },
    logout() {
      adminStorageService.clear();
      this.isAuthenticated = false;
    },
  },
};
</script>

<style scoped>
.admin-icon { font-size: 64px; text-align: center; margin-bottom: 8px; }
.form-card {
  width: 100%; max-width: 420px;
  display: flex; flex-direction: column;
  gap: 16px; text-align: center;
}
.form-title { font-size: 1.5rem; font-weight: 900; }
.field { display: flex; flex-direction: column; gap: 6px; text-align: left; }
.field-label { font-size: 13px; font-weight: 700; color: var(--text-mid); }
.error-msg { color: #d63030; font-size: 13px; font-weight: 600; text-align: left; }

.admin-panel { width: 100%; max-width: 900px; padding: 20px; }
.panel-header {
  display: flex; justify-content: space-between;
  align-items: center; margin-bottom: 24px;
}
.panel-title { font-size: 1.3rem; font-weight: 900; }
.logout-btn { width: auto; padding: 8px 18px; font-size: 14px; }

/* Onglets */
.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  border-bottom: 2px solid var(--border);
  padding-bottom: 0;
}
.tab {
  padding: 10px 20px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  font-family: var(--font);
  font-size: 14px;
  font-weight: 700;
  color: var(--text-mid);
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 8px 8px 0 0;
}
.tab:hover { color: var(--text-dark); background: var(--off-white); }
.tab.active {
  color: var(--navy);
  border-bottom-color: var(--navy);
  background: none;
}

.tab-content { padding-top: 8px; }
</style>