<script setup>
import AdminComponent from '@/components/AdminComponent.vue'
</script>

<template>
  <div class="container mt-5">
    <!-- Titre centré pour accueillir l'administrateur -->
    <div class="row">
      <div class=" text-center mb-5">
        <h1>Bienvenue, Admin</h1>
      </div>
      <AdminComponent />
    </div>

  </div>
</template>


<style scoped>
.container {
  max-width: 1000px;
  margin: auto;
}
</style>
