<template>
  <div class="manager-wrap fade-up">
    <div class="top-bar">
      <span class="q-counter">Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</span>
      <span class="q-badge">{{ Math.round(completePercentage) }}%</span>
    </div>
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: completePercentage + '%' }"></div>
    </div>
    <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
  </div>
</template>

<script>
import QuestionDisplay from './QuestionDisplay.vue';
import participationStorageService from '@/services/ParticipationStorageService';
import quizApiService from '@/services/QuizApiService';

export default {
  data() {
    return {
      currentQuestionPosition: 1,
      totalNumberOfQuestion: 0,
      completePercentage: 0,
      currentQuestion: {},
      selectedAnswer: [],
    };
  },
  components: { QuestionDisplay },
  methods: {
    async loadQuestionByPosition() {
      this.completePercentage = ((this.currentQuestionPosition - 1) / this.totalNumberOfQuestion) * 100;
      let response = await quizApiService.getQuestion(this.currentQuestionPosition);
      this.currentQuestion = response.data;
    },
    async answerClickedHandler(index) {
      this.selectedAnswer.push(index);
      if (this.currentQuestionPosition >= this.totalNumberOfQuestion) {
        this.endQuiz();
      } else {
        this.currentQuestionPosition++;
        this.loadQuestionByPosition();
      }
    },
    async endQuiz() {
      let participant = {
        playerName: participationStorageService.getPlayerName(),
        answers: this.selectedAnswer,
      };
      let response = await quizApiService.postParticipation(participant);
      participationStorageService.saveParticipationScore(response.data.score);
      this.$router.push('/result');
    },
  },
  async created() {
  const stored = participationStorageService.getTotalQuestions();
  if (stored) {
    this.totalNumberOfQuestion = parseInt(stored);
  } else {
    // Fallback si pas de valeur en localStorage
    const response = await quizApiService.getQuizInfo();
    this.totalNumberOfQuestion = response.data.size;
  }
  this.loadQuestionByPosition();
  },
};
</script>

<style scoped>
.manager-wrap {
  max-width: 640px;
  margin: 0 auto;
  padding: 32px 20px;
}
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.q-counter {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-mid);
}
.q-badge {
  font-size: 12px;
  font-weight: 800;
  background: var(--navy);
  color: white;
  padding: 3px 10px;
  border-radius: 99px;
}
</style>
