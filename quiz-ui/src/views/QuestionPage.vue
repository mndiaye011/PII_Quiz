<template>
  <div>
    <QuestionManager />
  </div>
</template>

<script>
import QuestionManager from '@/components/QuestionsManager.vue';
import participationStorageService from '@/services/ParticipationStorageService';

export default {
  components: { QuestionManager },
  created() {
    participationStorageService.saveParticipationScore(0);
  }
}
</script>
