<template>
  <div class="page-center fade-up">
    <div class="hero">
      <div class="hero-emoji">🧠</div>
      <h1 class="hero-title">Quiz Cognitique</h1>
      <p class="hero-sub">Teste tes connaissances en culture générale</p>
      <button class="btn-navy hero-btn" @click="$router.push('/start-new-quiz-page')">
        Démarrer le quiz !
      </button>
    </div>

    <div class="scores-section" v-if="registeredScores.length > 0">
      <h2 class="scores-title">🏆 Meilleurs scores</h2>
      <div class="scores-list">
        <div
          v-for="(entry, index) in registeredScores.slice(0, 5)"
          :key="entry.date"
          class="score-row"
        >
          <span class="rank">{{ medals[index] || (index + 1) }}</span>
          <span class="name">{{ entry.playerName }}</span>
          <span class="score">{{ entry.score }} pts</span>
        </div>
      </div>
    </div>
    <p v-else class="no-scores">Sois le premier à entrer dans le classement !</p>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: [],
      medals: ['🥇', '🥈', '🥉'],
    };
  },
  async created() {
    let response = await quizApiService.getQuizInfo();
    this.registeredScores = response.data.scores;
    participationStorageService.saveTotalQuestions(response.data.size);
  }
};
</script>

<style scoped>
.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-align: center;
  margin-bottom: 48px;
}
.hero-emoji {
  font-size: 120px;
  line-height: 1;
  margin-bottom: 8px;
  filter: drop-shadow(0 8px 24px rgba(18,18,42,0.1));
  animation: bob 3s ease-in-out infinite;
}
@keyframes bob {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
.hero-title {
  font-size: 2rem;
  font-weight: 900;
  color: var(--text-dark);
  letter-spacing: -0.5px;
}
.hero-sub {
  color: var(--text-mid);
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 8px;
}
.hero-btn { max-width: 360px; font-size: 17px; padding: 16px 32px; }

.scores-section {
  width: 100%;
  max-width: 400px;
}
.scores-title {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text-dark);
  margin-bottom: 14px;
  text-align: center;
}
.scores-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.score-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--off-white);
  border-radius: var(--radius);
  border: 1px solid var(--border);
}
.rank { font-size: 18px; width: 28px; text-align: center; flex-shrink: 0; }
.name { flex: 1; font-weight: 700; font-size: 14px; color: var(--text-dark); }
.score { font-weight: 800; font-size: 14px; color: var(--navy); }

.no-scores {
  color: var(--text-light);
  font-size: 14px;
  font-style: italic;
  text-align: center;
}
</style>
