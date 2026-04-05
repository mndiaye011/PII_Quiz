import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = { "Content-Type": "application/json" };
    if (token != null) headers.authorization = "Bearer " + token;
    return instance({ method, headers, url: resource, data })
      .then(response => ({ status: response.status, data: response.data }))
      .catch(error => { console.error(error); throw error; });
  },
  getQuizInfo(quizId = null) {
    const url = quizId ? `quiz-info?quizId=${quizId}` : "quiz-info";
    return this.call("get", url);
  },
  getQuestion(position, quizId = null) {
    const url = quizId ? `questions/${position}?quizId=${quizId}` : `questions/${position}`;
    return this.call("get", url);
  },
  getQuestions(token) { return this.call("get", "questions", null, token); },
  postParticipation(participant) { return this.call("post", "participations", participant); },
  login(password) { return this.call("post", "login", { password }); },
  postQuestion(question, token) { return this.call("post", "questions", question, token); },
  putQuestion(position, question, token) { return this.call("put", `questions/${position}`, question, token); },
  deleteQuestion(id, token) { return this.call("delete", `questions/${id}`, null, token); },
  getQuizzes() { return this.call("get", "quizzes"); },
  postQuiz(quiz, token) { return this.call("post", "quizzes", quiz, token); },
  deleteQuiz(id, token) { return this.call("delete", `quizzes/${id}`, null, token); },
  registerUser(data) { return this.call("post", "users/register", data); },
  loginUser(data) { return this.call("post", "users/login", data); },
  getUserHistory(userId) { return this.call("get", `users/${userId}/history`); },
};