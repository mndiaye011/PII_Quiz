<template>
  <div>
    <button class="btn btn-primary mt-3" @click="NewQuestion">Ajouter une question</button>
    <table class="table table-striped mt-3">
      <thead>
        <tr>
          <th scope="col">Position</th>
          <th scope="col">Titre</th>
          <th scope="col">Questions</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="question in questions" :key="question.position">
          <td>{{ question.position }}</td>
          <td>{{ question.title }}</td>
          <td>{{ question.text }}</td>
          <td>
            <button class="btn btn-info btn-sm" @click="EditQuestion(question)">Modifier</button>
            <button class="btn btn-danger btn-sm" @click="DeleteQuestion(question.position)">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>

    <QuestionEdition v-if="createQuestion" :create="true" @question-update="UpdateQuestion" />

    <!-- Modal -->
    <div class="modal fade" id="editQuestionModal" tabindex="-1" aria-labelledby="editQuestionModalLabel"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="editQuestionModalLabel">Modifier la question</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <QuestionEdition v-if="editingQuestion" :create="false" :question="editingQuestion"
              :originalPosition="editingQuestion.position" @question-update="UpdateQuestion" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import quizApiService from '@/services/QuizApiService';
import adminStorageService from "@/services/AdminStorageServices";
import QuestionEdition from './QuestionEdition.vue';
import * as bootstrap from 'bootstrap'; // Import Bootstrap

export default {
  data() {
    return {
      questions: [],
      size: 0,
      createQuestion: false,
      editingQuestion: null
    }
  },
  components: {
    QuestionEdition
  },
  methods: {
    async UpdateQuestion() {
      this.createQuestion = false;
      this.editingQuestion = null;
      let response = await quizApiService.getQuestions(adminStorageService.getToken());
      this.questions = response.data.questions;
      this.size = response.data.size;
      console.log(this.questions);
    },
    NewQuestion() {
      this.createQuestion = true;
    },
    EditQuestion(question) {
      this.editingQuestion = { ...question };
      var modal = new bootstrap.Modal(document.getElementById('editQuestionModal'));
      modal.show();
    },
    async DeleteQuestion(position) {
      await quizApiService.deleteQuestion(position, adminStorageService.getToken());
      this.UpdateQuestion();
    }
  },
  created() {
    this.UpdateQuestion()
  },
}
</script>
