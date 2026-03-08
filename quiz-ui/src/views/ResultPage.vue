<template>
  <div class="page-center fade-up">
    <div class="result-card card">
      <!-- Score hero -->
      <div class="score-hero">
        <div class="score-emoji">{{ scoreEmoji }}</div>
        <div class="score-number">{{ score }}<span class="score-total">/ {{ totalNumberOfQuestion }}</span></div>
        <p class="score-label">{{ scoreLabel }}</p>
        <p class="player-name">{{ playerName }}</p>
      </div>

      <!-- Score bar -->
      <div class="score-bar-wrap">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: scorePercent + '%' }"></div>
        </div>
        <span class="score-pct">{{ scorePercent }}%</span>
      </div>

      <!-- Tables -->
      <div class="tables-grid">
        <div class="table-block">
          <h3 class="table-title">Voisins de scores</h3>
          <div class="table-rows">
            <div v-if="playersBefore" class="table-row ellipsis">
              <span>···</span><span></span>
            </div>
            <div
              v-for="entry in getFivePlayerNearPlayer()"
              :key="entry.date"
              class="table-row"
              :class="{ 'is-you': entry.playerName === playerName }"
            >
              <span class="row-name">{{ entry.playerName }}</span>
              <span class="row-score">{{ entry.score }}</span>
            </div>
            <div v-if="playersAfter" class="table-row ellipsis">
              <span>···</span><span></span>
            </div>
          </div>
        </div>

        <div class="table-block">
          <h3 class="table-title">🏆 Top 5</h3>
          <div class="table-rows">
            <div
              v-for="(entry, index) in getFiveBest()"
              :key="entry.date"
              class="table-row"
              :class="{ 'is-you': entry.playerName === playerName }"
            >
              <span class="rank-medal">{{ medals[index] || (index + 1) }}</span>
              <span class="row-name">{{ entry.playerName }}</span>
              <span class="row-score">{{ entry.score }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="actions">
        <button class="btn-navy" @click="$router.push('/start-new-quiz-page')">Rejouer</button>
        <button class="btn-outline" @click="$router.push('/')">Accueil</button>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from "../services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "ResultPage",
  data() {
    return {
      registeredScores: [],
      score: 0,
      playerName: '',
      totalNumberOfQuestion: 0,
      playersBefore: false,
      playersAfter: false,
      medals: ['🥇', '🥈', '🥉', '4', '5'],
    };
  },
  computed: {
    scorePercent() {
      if (!this.totalNumberOfQuestion) return 0;
      return Math.round((this.score / this.totalNumberOfQuestion) * 100);
    },
    scoreEmoji() {
      const p = this.scorePercent;
      if (p >= 80) return '🎉';
      if (p >= 50) return '😊';
      if (p >= 30) return '😅';
      return '🧠';
    },
    scoreLabel() {
      const p = this.scorePercent;
      if (p >= 80) return 'Excellent !';
      if (p >= 50) return 'Bien joué !';
      if (p >= 30) return 'Pas mal...';
      return 'Continue d\'apprendre !';
    },
  },
  async created() {
    let response = await quizApiService.getQuizInfo();
    participationStorageService.saveTotalQuestions(response.data.size);
    this.registeredScores = response.data.scores;
    this.score = participationStorageService.getParticipationScore();
    this.playerName = participationStorageService.getPlayerName();
    this.totalNumberOfQuestion = participationStorageService.getTotalQuestions();
  },
  methods: {
    getFiveBest() {
      return [...this.registeredScores].sort((a, b) => b.score - a.score).slice(0, 5);
    },
    getFivePlayerNearPlayer() {
      let scores = [...this.registeredScores].sort((a, b) => b.score - a.score);
      let pos = scores.findIndex(s => s.playerName === this.playerName);
      let start = Math.max(0, pos - 2);
      this.playersBefore = start > 0;
      this.playersAfter = pos + 2 < scores.length - 1;
      return scores.slice(start, pos + 3);
    },
  },
};
</script>

<style scoped>
.result-card {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.score-hero {
  text-align: center;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
}
.score-emoji { font-size: 64px; margin-bottom: 8px; }
.score-number {
  font-size: 4rem;
  font-weight: 900;
  color: var(--navy);
  line-height: 1;
}
.score-total { font-size: 1.5rem; color: var(--text-light); }
.score-label { font-size: 18px; font-weight: 800; color: var(--text-dark); margin-top: 8px; }
.player-name { font-size: 14px; color: var(--text-mid); font-weight: 600; margin-top: 4px; }

.score-bar-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}
.score-bar-wrap .progress-bar { flex: 1; }
.score-pct { font-size: 13px; font-weight: 800; color: var(--navy); flex-shrink: 0; }

.tables-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
@media (max-width: 500px) { .tables-grid { grid-template-columns: 1fr; } }

.table-block { }
.table-title {
  font-size: 13px;
  font-weight: 800;
  color: var(--text-mid);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
}
.table-rows { display: flex; flex-direction: column; gap: 6px; }
.table-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--off-white);
  border-radius: 8px;
  font-size: 13px;
  border: 1px solid transparent;
}
.table-row.is-you {
  background: var(--navy);
  color: white;
  border-color: var(--navy);
}
.table-row.ellipsis {
  background: transparent;
  color: var(--text-light);
  font-size: 18px;
  border: none;
  padding: 2px 12px;
}
.rank-medal { flex-shrink: 0; font-size: 15px; }
.row-name { flex: 1; font-weight: 700; }
.row-score { font-weight: 800; }

.actions { display: flex; flex-direction: column; gap: 10px; }
</style>
