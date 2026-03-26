<template>
  <div class="quiz-list">
    <div class="list-header">
      <h3 class="list-title">Quiz <span class="count-badge">{{ quizzes.length }}</span></h3>
      <button class="btn-navy add-btn" @click="showForm = true" v-if="!showForm">
        + Nouveau quiz
      </button>
    </div>

    <!-- Formulaire de création -->
    <div v-if="showForm" class="inline-form card">
      <div class="form-header">
        <span class="form-label">Nouveau quiz</span>
        <button class="close-btn" @click="cancelForm">✕</button>
      </div>
      <div class="fields">
        <div class="field">
          <label class="field-label">Nom du quiz *</label>
          <input
            class="input-field"
            type="text"
            v-model="newQuiz.name"
            placeholder="Ex: Culture générale, Histoire..."
          />
        </div>
        <div class="field">
          <label class="field-label">Description</label>
          <input
            class="input-field"
            type="text"
            v-model="newQuiz.description"
            placeholder="Courte description (optionnel)"
          />
        </div>
      </div>
      <p v-if="errorMessage" class="error-msg">⚠️ {{ errorMessage }}</p>
      <button class="btn-navy submit-btn" @click="createQuiz">Créer le quiz</button>
    </div>

    <!-- Liste vide -->
    <div v-if="quizzes.length === 0 && !showForm" class="empty-state">
      <span class="empty-icon">📭</span>
      <p>Aucun quiz créé pour l'instant</p>
    </div>

    <!-- Liste des quiz -->
    <div class="q-table" v-if="quizzes.length > 0">
      <div class="q-row q-head">
        <span class="col-id">#</span>
        <span class="col-name">Nom</span>
        <span class="col-desc">Description</span>
        <span class="col-actions">Actions</span>
      </div>
      <div v-for="quiz in quizzes" :key="quiz.id" class="q-row">
        <span class="col-id">
          <span class="pos-badge">{{ quiz.id }}</span>
        </span>
        <span class="col-name">{{ quiz.name }}</span>
        <span class="col-desc q-text-trunc">{{ quiz.description || '—' }}</span>
        <span class="col-actions">
          <button class="action-btn del" @click="deleteQuiz(quiz.id)" title="Supprimer">🗑️</button>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from '@/services/QuizApiService';
import adminStorageService from '@/services/AdminStorageServices';

export default {
  data() {
    return {
      quizzes: [],
      showForm: false,
      errorMessage: '',
      newQuiz: { name: '', description: '' },
    };
  },
  methods: {
    async loadQuizzes() {
      try {
        const response = await quizApiService.getQuizzes();
        this.quizzes = response.data.quizzes;
      } catch {
        this.quizzes = [];
      }
    },
    async createQuiz() {
      if (!this.newQuiz.name.trim()) {
        this.errorMessage = 'Le nom du quiz est obligatoire.';
        return;
      }
      try {
        await quizApiService.postQuiz(this.newQuiz, adminStorageService.getToken());
        this.cancelForm();
        this.loadQuizzes();
      } catch {
        this.errorMessage = 'Erreur lors de la création.';
      }
    },
    async deleteQuiz(id) {
      if (confirm('Supprimer ce quiz ? Les questions associées resteront en base.')) {
        await quizApiService.deleteQuiz(id, adminStorageService.getToken());
        this.loadQuizzes();
      }
    },
    cancelForm() {
      this.showForm = false;
      this.errorMessage = '';
      this.newQuiz = { name: '', description: '' };
    },
  },
  created() {
    this.loadQuizzes();
  },
};
</script>

<style scoped>
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.list-title {
  font-size: 1.1rem;
  font-weight: 900;
  display: flex;
  align-items: center;
  gap: 8px;
}
.count-badge {
  background: var(--navy);
  color: white;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 99px;
}
.add-btn { width: auto; padding: 10px 20px; font-size: 14px; }

.inline-form { margin-bottom: 20px; padding: 20px; }
.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.form-label { font-size: 14px; font-weight: 800; color: var(--text-mid); }
.close-btn {
  background: none; border: none;
  font-size: 18px; cursor: pointer;
  color: var(--text-light); padding: 4px;
}
.close-btn:hover { color: var(--text-dark); }
.fields { display: flex; flex-direction: column; gap: 12px; margin-bottom: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field-label { font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-mid); }
.error-msg { color: #d63030; font-size: 13px; font-weight: 600; margin-bottom: 8px; }
.submit-btn { margin-top: 4px; }

.empty-state { text-align: center; padding: 48px 20px; color: var(--text-light); }
.empty-icon { font-size: 48px; display: block; margin-bottom: 8px; }

.q-table { display: flex; flex-direction: column; gap: 6px; }
.q-row {
  display: grid;
  grid-template-columns: 50px 1fr 2fr 60px;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius);
  background: var(--off-white);
  border: 1px solid var(--border);
  font-size: 14px;
}
.q-head {
  background: var(--navy); color: white;
  font-size: 12px; font-weight: 800;
  text-transform: uppercase; letter-spacing: 0.5px;
}
.pos-badge {
  background: var(--navy); color: white;
  width: 26px; height: 26px;
  border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 800;
}
.col-name { font-weight: 700; }
.q-text-trunc {
  overflow: hidden; text-overflow: ellipsis;
  white-space: nowrap; color: var(--text-mid);
}
.col-actions { display: flex; gap: 6px; }
.action-btn {
  background: none; border: none;
  cursor: pointer; font-size: 16px;
  padding: 4px; border-radius: 6px;
  transition: background 0.15s;
}
.action-btn:hover { background: var(--border); }
</style>