export default {
  clear() {
    window.localStorage.removeItem("playerName");
    window.localStorage.removeItem("participationScore");
  },
  savePlayerName(playerName) {
    window.localStorage.setItem("playerName", playerName);
  },
  getPlayerName() {
    return window.localStorage.getItem("playerName");
  },
  saveParticipationScore(participationScore) {
    window.localStorage.setItem("participationScore", participationScore);
  },
  getParticipationScore() {
    return window.localStorage.getItem("participationScore");
  },
  saveTotalQuestions(total) {
    window.localStorage.setItem("totalQuestions", total);
  },
  getTotalQuestions() {
    return window.localStorage.getItem("totalQuestions");
  },
  saveSelectedQuiz(quiz) {
    window.localStorage.setItem("selectedQuiz", JSON.stringify(quiz));
  },
  getSelectedQuiz() {
    const q = window.localStorage.getItem("selectedQuiz");
    return q ? JSON.parse(q) : null;
  },
};