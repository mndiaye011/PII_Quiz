<template>
  <div class="page-center fade-up">
    <div class="sel-hero">
      <div class="sel-emoji">💪</div>
      <h1 class="sel-title">Choisir un Quiz</h1>
      <p class="sel-sub">Sélectionne un thème pour commencer</p>
    </div>

    <div class="quiz-grid" v-if="quizzes.length > 0">
      <div
        v-for="quiz in quizzes"
        :key="quiz.id"
        class="quiz-card"
        @click="selectQuiz(quiz)"
      >
        <span class="quiz-icon">📚</span>
        <h3 class="quiz-name">{{ quiz.name }}</h3>
        <p class="quiz-desc">{{ quiz.description || 'Pas de description' }}</p>
        <span class="quiz-start">Démarrer →</span>
      </div>
    </div>

    <div v-else class="empty-state">
      <p>Aucun quiz disponible pour l'instant.</p>
    </div>
  </div>
</template>

<script>
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';

export default {
  data() {
    return { quizzes: [] };
  },
  async created() {
    try {
      const response = await quizApiService.getQuizzes();
      this.quizzes = response.data.quizzes || [];
    } catch {
      this.quizzes = [];
    }
  },
  methods: {
    async selectQuiz(quiz) {
      participationStorageService.saveSelectedQuiz(quiz);
      // Charge le nombre de questions de ce quiz
      const info = await quizApiService.getQuizInfo(quiz.id);
      participationStorageService.saveTotalQuestions(info.data.size);
      this.$router.push('/start-new-quiz-page');
    }
  }
};
</script>

<style scoped>
.sel-hero { text-align: center; margin-bottom: 32px; }
.sel-emoji { font-size: 80px; display: block; margin-bottom: 12px;
  animation: bob 3s ease-in-out infinite; }
@keyframes bob {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
.sel-title { font-size: 1.8rem; font-weight: 900; }
.sel-sub { color: var(--text-mid); font-size: 15px; margin-top: 6px; }

.quiz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  width: 100%;
  max-width: 720px;
}
.quiz-card {
  background: var(--white);
  border: 1.5px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 24px 20px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.quiz-card:hover {
  border-color: var(--navy);
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}
.quiz-icon { font-size: 36px; }
.quiz-name { font-size: 1rem; font-weight: 900; color: var(--text-dark); }
.quiz-desc { font-size: 13px; color: var(--text-mid); flex: 1; }
.quiz-start { font-size: 13px; font-weight: 800; color: var(--navy); margin-top: 8px; }

.empty-state { color: var(--text-light); font-style: italic; }
</style>

