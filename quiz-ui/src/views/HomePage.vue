<template>
  <div class="container mt-5 d-flex justify-content-between">


    <!-- Tableau des scores à gauche -->
    <div class="scores-container flex-grow-1">
      <div class="welcome-container">
        <h1 class="mb-8 text-center text-uppercase display-4">Bienvenue dans le quiz!</h1>
        <button class="btn btn-lg btn-outline-dark " type="button" @click="$router.push('start-new-quiz-page')">Démarrer
          le quiz!</button>
      </div>

      <br><br>
      <h2 class="text-uppercase text-center">Meilleurs scores</h2>
      <div class="table-responsive">
        <table class="table table-striped table-hover border-dark">
          <thead class="thead-dark">
            <tr>
              <th scope="col">#</th>
              <th scope="col">Pseudo</th>
              <th scope="col">Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(scoreEntry, index) in registeredScores" :key="scoreEntry.date">
              <th scope="row">{{ index + 1 }}</th>
              <td>{{ scoreEntry.playerName }}</td>
              <td>{{ scoreEntry.score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>


  </div>
</template>



<style>
.container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  /* Assure que les conteneurs restent alignés en haut sur de petits écrans */
}

.scores-container {
  flex: 1;
  /* Prend la moitié de l'espace disponible */
  padding: 20px;
}

.welcome-container {
  flex: 1.5;
  /* Prend une portion plus grande pour plus de visibilité */
  padding: 20px;
  background-color: #f8f9fa;
  /* Couleur de fond pour mettre en avant la section */
  border: 2px solid black;
  /* Bordure pour renforcer le style Sketchy */
  box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
  /* Ombre portée pour le relief */
  display: flex;
  /* Activation de Flexbox pour le centrage */
  flex-direction: column;
  /* Les enfants sont empilés verticalement */
  justify-content: center;
  /* Centrage vertical des enfants */
  align-items: center;
  /* Centrage horizontal des enfants */
}
</style>

<script>

import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "HomePage",
  data() {
    return {
      registeredScores: [],
    };
  },

  async created() {

    let response = await quizApiService.getQuizInfo();
    this.registeredScores = response.data.scores;
    participationStorageService.saveTotalQuestions(response.data.size);

  }
};
</script>
