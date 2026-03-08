<template>
  <div class="question-list">
    <div class="list-header">
      <h3 class="list-title">Questions <span class="count-badge">{{ questions.length }}</span></h3>
      <!-- FIX 3: appelle la méthode openCreateForm() -->
      <button class="btn-navy add-btn" @click="openCreateForm()" v-if="!createQuestion">
        + Ajouter
      </button>
    </div>

    <!-- Create form inline -->
    <div v-if="createQuestion" class="inline-form card">
      <div class="form-header">
        <span class="form-label">Nouvelle question</span>
        <button class="close-btn" @click="createQuestion = false">✕</button>
      </div>
      <QuestionEdition :create="true" @question-update="UpdateQuestion" />
    </div>

    <!-- Empty state -->
    <div v-if="questions.length === 0 && !createQuestion" class="empty-state">
      <span class="empty-icon">📭</span>
      <p>Aucune question pour l'instant</p>
    </div>

    <!-- Questions table -->
    <div class="q-table" v-if="questions.length > 0">
      <div class="q-row q-head">
        <span class="col-pos">#</span>
        <span class="col-title">Titre</span>
        <span class="col-text">Question</span>
        <span class="col-actions">Actions</span>
      </div>
      <div
        v-for="question in questions"
        :key="question.position"
        class="q-row"
      >
        <span class="col-pos"><span class="pos-badge">{{ question.position }}</span></span>
        <span class="col-title">{{ question.title }}</span>
        <span class="col-text q-text-trunc">{{ question.text }}</span>
        <span class="col-actions">
          <button class="action-btn edit" @click="openEdit(question)" title="Modifier">✏️</button>
          <button class="action-btn del" @click="DeleteQuestion(question.position)" title="Supprimer">🗑️</button>
        </span>
      </div>
    </div>

    <!-- Edit modal -->
    <div class="modal-overlay" v-if="editingQuestion" @click.self="editingQuestion = null">
      <div class="modal-box card fade-up">
        <div class="modal-head">
          <h3 class="modal-title">Modifier la question</h3>
          <button class="close-btn" @click="editingQuestion = null">✕</button>
        </div>
        <QuestionEdition
          :create="false"
          :question="editingQuestion"
          :originalPosition="editingQuestion.position"
          @question-update="UpdateQuestion"
        />
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from '@/services/QuizApiService';
import adminStorageService from '@/services/AdminStorageServices';
import QuestionEdition from './QuestionEdition.vue';

export default {
  components: { QuestionEdition },
  data() {
    return {
      questions: [],
      createQuestion: false,
      editingQuestion: null,
    };
  },
  methods: {
    async UpdateQuestion() {
      this.createQuestion = false;
      this.editingQuestion = null;
      try {
        let response = await quizApiService.getQuestions(adminStorageService.getToken());
        this.questions = response.data.questions;
      } catch {
        this.questions = [];
      }
    },
    openEdit(question) {
      this.editingQuestion = { ...question };
    },
    // FIX 3: méthode correctement définie, appelée par @click="openCreateForm()"
    openCreateForm() {
      this.createQuestion = true;
      this.$nextTick(() => {
        const el = document.querySelector('.inline-form');
        if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    },
    async DeleteQuestion(position) {
      if (confirm('Supprimer cette question ?')) {
        await quizApiService.deleteQuestion(position, adminStorageService.getToken());
        this.UpdateQuestion();
      }
    },
  },
  created() { this.UpdateQuestion(); },
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

.inline-form {
  margin-bottom: 20px;
  padding: 20px;
}
.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.form-label { font-size: 14px; font-weight: 800; color: var(--text-mid); }
.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: var(--text-light);
  padding: 4px;
}
.close-btn:hover { color: var(--text-dark); }

.empty-state {
  text-align: center;
  padding: 48px 20px;
  color: var(--text-light);
}
.empty-icon { font-size: 48px; display: block; margin-bottom: 8px; }

.q-table {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.q-row {
  display: grid;
  grid-template-columns: 50px 1fr 2fr 80px;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius);
  background: var(--off-white);
  border: 1px solid var(--border);
  font-size: 14px;
}
.q-head {
  background: var(--navy);
  color: white;
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.pos-badge {
  background: var(--navy);
  color: white;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 800;
}
.col-title { font-weight: 700; }
.q-text-trunc {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--text-mid);
}
.col-actions { display: flex; gap: 6px; }
.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  padding: 4px;
  border-radius: 6px;
  transition: background 0.15s;
}
.action-btn:hover { background: var(--border); }

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(18,18,42,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}
.modal-box {
  width: 100%;
  max-width: 640px;
  max-height: 90vh;
  overflow-y: auto;
}
.modal-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.modal-title { font-size: 1.1rem; font-weight: 900; }
</style>
