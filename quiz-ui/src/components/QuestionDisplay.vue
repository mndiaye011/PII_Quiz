<template>
  <div class="q-card card fade-up" :key="question.id">
    <div class="q-header">
      <p v-if="question.title" class="q-title">{{ question.title }}</p>
      <p class="q-text">{{ question.text }}</p>
    </div>
    <img v-if="question.image" :src="question.image" class="q-image" />
    <div class="answers">
      <button
        v-for="(answer, index) in question.possibleAnswers"
        :key="answer.text"
        class="answer-btn"
        @click="$emit('answer-selected', index + 1)"
      >
        <span class="letter">{{ letters[index] }}</span>
        {{ answer.text }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: { question: { type: Object } },
  emits: ['answer-selected'],
  data() {
    return { letters: ['A', 'B', 'C', 'D', 'E', 'F'] };
  },
};
</script>

<style scoped>
.q-card {
  margin-top: 20px;
  padding: 28px;
}
.q-header { margin-bottom: 20px; }
.q-title {
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-light);
  margin-bottom: 6px;
}
.q-text {
  font-size: 17px;
  font-weight: 800;
  color: var(--text-dark);
  line-height: 1.5;
}
.q-image {
  width: 100%;
  border-radius: var(--radius);
  margin-bottom: 20px;
  max-height: 240px;
  object-fit: cover;
}
.answers {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
