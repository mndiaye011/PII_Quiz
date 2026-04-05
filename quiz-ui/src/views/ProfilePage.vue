<template>
  <div class="page-center fade-up">
    <div class="profile-card card">
      <div class="profile-header">
        <div class="avatar">{{ user.username.charAt(0).toUpperCase() }}</div>
        <div>
          <h1 class="username">{{ user.username }}</h1>
          <p class="stats">{{ history.length }} participation{{ history.length > 1 ? 's' : '' }}</p>
        </div>
        <button class="btn-outline logout-btn" @click="logout">Déconnexion</button>
      </div>

      <div class="section-title">📊 Mon historique</div>

      <div v-if="history.length === 0" class="empty">
        <span>🎯</span>
        <p>Pas encore de participation. Lance ton premier quiz !</p>
        <button class="btn-navy" @click="$router.push('/select-quiz')">Jouer maintenant</button>
      </div>

      <div v-else class="history-list">
        <div v-for="entry in history" :key="entry.id" class="history-row">
          <div class="history-left">
            <span class="quiz-name">{{ entry.quizName || 'Quiz général' }}</span>
            <span class="history-date">{{ entry.date }}</span>
          </div>
          <div class="history-right">
            <div class="score-bar-wrap">
              <div class="mini-bar">
                <div class="mini-fill" :style="{ width: scorePercent(entry) + '%', background: scoreColor(entry) }"></div>
              </div>
              <span class="score-text" :style="{ color: scoreColor(entry) }">
                {{ entry.score }}/{{ entry.totalQuestions || '?' }}
              </span>
            </div>
            <span class="score-badge" :style="{ background: scoreColor(entry) }">
              {{ scorePercent(entry) }}%
            </span>
          </div>
        </div>
      </div>

      <button class="btn-navy play-btn" @click="$router.push('/select-quiz')">🎯 Jouer</button>
    </div>
  </div>
</template>

<script>
import quizApiService from '@/services/QuizApiService';
import userStorageService from '@/services/UserStorageService';

export default {
  data() {
    return { user: userStorageService.getUser(), history: [] };
  },
  async created() {
    if (!this.user) { this.$router.push('/login'); return; }
    try {
      const res = await quizApiService.getUserHistory(this.user.id);
      this.history = res.data.history;
    } catch { this.history = []; }
  },
  methods: {
    logout() {
      userStorageService.logout();
      this.$router.push('/');
    },
    scorePercent(entry) {
      if (!entry.totalQuestions) return 0;
      return Math.round((entry.score / entry.totalQuestions) * 100);
    },
    scoreColor(entry) {
      const p = this.scorePercent(entry);
      if (p >= 80) return '#22c55e';
      if (p >= 50) return '#f59e0b';
      return '#ef4444';
    },
  },
};
</script>

<style scoped>
.profile-card { width: 100%; max-width: 600px; display: flex; flex-direction: column; gap: 20px; }
.profile-header { display: flex; align-items: center; gap: 16px; padding-bottom: 20px; border-bottom: 1px solid var(--border); }
.avatar {
  width: 56px; height: 56px; border-radius: 50%;
  background: var(--navy); color: white;
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; font-weight: 900; flex-shrink: 0;
}
.username { font-size: 1.3rem; font-weight: 900; }
.stats { font-size: 13px; color: var(--text-mid); margin-top: 2px; }
.logout-btn { margin-left: auto; width: auto; padding: 8px 16px; font-size: 13px; }
.section-title { font-size: 14px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-mid); }
.empty { text-align: center; padding: 24px; color: var(--text-light); display: flex; flex-direction: column; gap: 10px; align-items: center; }
.empty span { font-size: 48px; }
.history-list { display: flex; flex-direction: column; gap: 8px; }
.history-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 14px 16px; background: var(--off-white);
  border-radius: var(--radius); border: 1px solid var(--border);
}
.history-left { display: flex; flex-direction: column; gap: 3px; }
.quiz-name { font-size: 14px; font-weight: 700; color: var(--text-dark); }
.history-date { font-size: 12px; color: var(--text-light); }
.history-right { display: flex; align-items: center; gap: 10px; }
.score-bar-wrap { display: flex; align-items: center; gap: 6px; }
.mini-bar { width: 80px; height: 6px; background: var(--border); border-radius: 99px; overflow: hidden; }
.mini-fill { height: 100%; border-radius: 99px; transition: width 0.4s; }
.score-text { font-size: 13px; font-weight: 700; }
.score-badge { color: white; font-size: 11px; font-weight: 800; padding: 3px 8px; border-radius: 99px; }
.play-btn { margin-top: 4px; }
</style>