<template>
  <div class="edition-form">
    <div class="fields-grid">
      <div class="field">
        <label class="field-label">Titre</label>
        <input class="input-field" type="text" v-model="currentQuestion.title" placeholder="Titre de la question" />
      </div>
      <div class="field">
        <label class="field-label">Position</label>
        <input class="input-field" type="number" v-model="currentQuestion.position" :max="totalQuestion + 1" min="1" />
      </div>
    </div>
    <div class="field">
      <label class="field-label">Texte de la question</label>
      <input class="input-field" type="text" v-model="currentQuestion.text" placeholder="Texte complet de la question" />
    </div>
    <div class="field">
      <label class="field-label">Image (optionnel)</label>
      <img v-if="currentQuestion.image" :src="currentQuestion.image" class="image-preview" />
      <ImageUpload @file-change="imageFileChangedHandler" />
    </div>
    <div class="field">
      <label class="field-label">Réponses — sélectionne la bonne réponse</label>
      <div class="answers-list">
        <div
          v-for="(answer, i) in currentQuestion.possibleAnswers"
          :key="i"
          class="answer-row"
          :class="{ selected: selectedAnswer === i }"
          @click="selectedAnswer = i"
        >
          <span class="answer-letter">{{ letters[i] }}</span>
          <input
            type="text"
            class="answer-input"
            v-model="answer.text"
            placeholder="Texte de la réponse"
            @click.stop
          />
          <span class="correct-dot" :class="{ active: selectedAnswer === i }">✓</span>
        </div>
        <button type="button" class="add-answer-btn" @click="addAnswer">+ Ajouter une réponse</button>
      </div>
    </div>
    <button type="button" class="btn-navy submit-btn" v-if="create" @click="addQuestion">Ajouter la question</button>
    <button type="button" class="btn-navy submit-btn" v-else @click="modifyQuestion">Enregistrer les modifications</button>
  </div>
</template>

<script>
import ImageUpload from '@/components/ImageUpload.vue';
import quizApiService from '@/services/QuizApiService';
import adminStorageService from '@/services/AdminStorageServices';

export default {
  components: { ImageUpload },
  props: {
    question: { type: Object },
    create: { type: Boolean, default: true },
    originalPosition: { type: Number },
  },
  emits: ['question-update'],
  data() {
    return {
      totalQuestion: 0,
      currentQuestion: {
        title: '', text: '', image: '', position: 1,
        possibleAnswers: [{ text: '', isCorrect: false }, { text: '', isCorrect: false }],
      },
      selectedAnswer: 0,
      letters: ['A', 'B', 'C', 'D', 'E', 'F'],
    };
  },
  methods: {
    imageFileChangedHandler(file) { this.currentQuestion.image = file; },
    addAnswer() {
      this.currentQuestion.possibleAnswers.push({ text: '', isCorrect: false });
    },
    checkQuestion() {
      return this.currentQuestion.title && this.currentQuestion.text && this.currentQuestion.possibleAnswers.length > 0;
    },
    async addQuestion() {
      this.currentQuestion.possibleAnswers[this.selectedAnswer].isCorrect = true;
      if (!this.checkQuestion()) { alert('Veuillez remplir tous les champs'); return; }
      try {
        await quizApiService.postQuestion(this.currentQuestion, adminStorageService.getToken());
        this.$emit('question-update');
      } catch (e) { console.error(e); }
    },
    async modifyQuestion() {
      if (!this.checkQuestion()) { alert('Veuillez remplir tous les champs'); return; }
      for (let i = 0; i < this.currentQuestion.possibleAnswers.length; i++) {
        this.currentQuestion.possibleAnswers[i].isCorrect = (this.selectedAnswer === i);
      }
      try {
        await quizApiService.putQuestion(this.originalPosition, this.currentQuestion, adminStorageService.getToken());
        this.$emit('question-update');
      } catch (e) { console.error(e); }
    },
  },
  async created() {
    let response = await quizApiService.getQuizInfo();
    this.totalQuestion = response.data.size;
    if (this.question) {
      this.currentQuestion = { ...this.question };
      this.selectedAnswer = this.question.possibleAnswers.findIndex(a => a.isCorrect);
    }
  },
};
</script>

<style scoped>
.edition-form { display: flex; flex-direction: column; gap: 16px; }
.fields-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 12px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field-label { font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: var(--text-mid); }
.image-preview {
  width: 100%;
  max-height: 140px;
  object-fit: cover;
  border-radius: var(--radius);
  margin-bottom: 8px;
  border: 1px solid var(--border);
}
.answers-list { display: flex; flex-direction: column; gap: 8px; }
.answer-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.15s;
  background: var(--off-white);
}
.answer-row:hover { border-color: var(--navy); }
.answer-row.selected { border-color: var(--navy); background: var(--navy); }
.answer-row.selected .answer-input { background: transparent; color: white; }
.answer-letter {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 800;
  flex-shrink: 0;
}
.answer-row.selected .answer-letter { background: rgba(255,255,255,0.2); color: white; }
.answer-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-family: var(--font);
  font-size: 14px;
  font-weight: 600;
  color: var(--text-dark);
}
.correct-dot {
  font-size: 16px;
  color: transparent;
  font-weight: 900;
  transition: color 0.15s;
}
.correct-dot.active { color: #4ade80; }
.add-answer-btn {
  padding: 10px;
  border: 1.5px dashed var(--border);
  border-radius: var(--radius);
  background: none;
  color: var(--text-mid);
  font-family: var(--font);
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s;
}
.add-answer-btn:hover { border-color: var(--navy); color: var(--navy); }
.submit-btn { margin-top: 8px; }
</style>
