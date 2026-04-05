<template>
  <div class="manager-wrap fade-up">
    <div class="top-bar">
      <span class="q-counter">Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</span>
      <span class="q-badge">{{ Math.round(completePercentage) }}%</span>
    </div>
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: completePercentage + '%' }"></div>
    </div>

    <!-- TIMER -->
    <div class="timer-wrap">
      <div class="timer-ring">
        <svg viewBox="0 0 60 60" class="timer-svg">
          <circle cx="30" cy="30" r="26" class="timer-bg" />
          <circle
            cx="30" cy="30" r="26"
            class="timer-arc"
            :class="{ warning: timeLeft <= 10, danger: timeLeft <= 5 }"
            :style="{ strokeDashoffset: dashOffset }"
          />
        </svg>
        <span class="timer-count" :class="{ warning: timeLeft <= 10, danger: timeLeft <= 5 }">
          {{ timeLeft }}
        </span>
      </div>
    </div>

    <QuestionDisplay :question="currentQuestion" @answer-selected="answerClickedHandler" />
  </div>
</template>

<script>
import QuestionDisplay from './QuestionDisplay.vue';
import participationStorageService from '@/services/ParticipationStorageService';
import quizApiService from '@/services/QuizApiService';
import userStorageService from '@/services/UserStorageService';

const TIMER_SECONDS = 30; // ← change cette valeur pour ajuster la durée
const CIRCUMFERENCE = 2 * Math.PI * 26; // 2πr avec r=26

export default {
  data() {
    return {
      currentQuestionPosition: 1,
      totalNumberOfQuestion: 0,
      completePercentage: 0,
      currentQuestion: {},
      selectedAnswer: [],
      timeLeft: TIMER_SECONDS,
      timerInterval: null,
    };
  },
  components: { QuestionDisplay },
  computed: {
    dashOffset() {
      // Arc SVG : plein = 0, vide = CIRCUMFERENCE
      return CIRCUMFERENCE * (1 - this.timeLeft / TIMER_SECONDS);
    }
  },
  methods: {
    startTimer() {
      this.stopTimer();
      this.timeLeft = TIMER_SECONDS;
      this.timerInterval = setInterval(() => {
        this.timeLeft--;
        if (this.timeLeft <= 0) {
          // Temps écoulé → on passe à la question suivante avec réponse 0 (aucune)
          this.answerClickedHandler(0);
        }
      }, 1000);
    },
    stopTimer() {
      if (this.timerInterval) {
        clearInterval(this.timerInterval);
        this.timerInterval = null;
      }
    },
    async loadQuestionByPosition() {
      const quiz = participationStorageService.getSelectedQuiz();
      const quizId = quiz ? quiz.id : null;
      this.completePercentage = ((this.currentQuestionPosition - 1) / this.totalNumberOfQuestion) * 100;
      let response = await quizApiService.getQuestion(this.currentQuestionPosition, quizId); // ← quizId ajouté
      this.currentQuestion = response.data;
      this.startTimer();
    },
    async answerClickedHandler(index) {
      this.stopTimer(); // ← arrête le timer dès qu'une réponse est donnée
      this.selectedAnswer.push(index);
      if (this.currentQuestionPosition >= this.totalNumberOfQuestion) {
        this.endQuiz();
      } else {
        this.currentQuestionPosition++;
        this.loadQuestionByPosition();
      }
    },
    async endQuiz() {
      const quiz = participationStorageService.getSelectedQuiz();
      const user = userStorageService.getUser(); // ← ajout
      let participant = {
        playerName: participationStorageService.getPlayerName(),
        answers: this.selectedAnswer,
        quizId: quiz ? quiz.id : null,
        userId: user ? user.id : null,  // ← ajout
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
        const response = await quizApiService.getQuizInfo();
        this.totalNumberOfQuestion = response.data.size;
      }
      this.loadQuestionByPosition();
    },
    // Important : stoppe le timer si on quitte la page
    beforeUnmount() {
      this.stopTimer();
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
.q-counter { font-size: 14px; font-weight: 700; color: var(--text-mid); }
.q-badge {
  font-size: 12px; font-weight: 800;
  background: var(--navy); color: white;
  padding: 3px 10px; border-radius: 99px;
}

/* Timer */
.timer-wrap {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}
.timer-ring {
  position: relative;
  width: 72px;
  height: 72px;
}
.timer-svg {
  width: 72px;
  height: 72px;
  transform: rotate(-90deg); /* démarre en haut */
}
.timer-bg {
  fill: none;
  stroke: var(--border);
  stroke-width: 4;
}
.timer-arc {
  fill: none;
  stroke: var(--navy);
  stroke-width: 4;
  stroke-linecap: round;
  stroke-dasharray: 163.36; /* CIRCUMFERENCE */
  stroke-dashoffset: 0;
  transition: stroke-dashoffset 1s linear, stroke 0.3s;
}
.timer-arc.warning { stroke: #f59e0b; }
.timer-arc.danger  { stroke: #ef4444; }

.timer-count {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 900;
  font-family: var(--font);
  color: var(--navy);
  transition: color 0.3s;
}
.timer-count.warning { color: #f59e0b; }
.timer-count.danger  { color: #ef4444; animation: pulse 0.5s infinite alternate; }

@keyframes pulse {
  from { transform: scale(1); }
  to   { transform: scale(1.15); }
}
</style>