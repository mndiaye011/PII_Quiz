<script setup>
import QuestionManager from '@/components/QuestionsManager.vue'
</script>

<template>
  <header>
    <div class="container-sm text-center w-25 mt-5">
      <div class="wrapper">
        <QuestionManager />
      </div>
    </div>
  </header>
</template>


<script>

import participationStorageService from '@/services/ParticipationStorageService';
export default {

  components: {
    QuestionManager
  },

  created() {

    participationStorageService.saveParticipationScore(0);

  }
}
</script>