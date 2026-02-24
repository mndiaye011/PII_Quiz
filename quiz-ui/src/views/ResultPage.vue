<template>
  <div class="container mt-5">
    <div class="text-center mb-5">
      <h1>Résultat</h1>
      <p>Félicitations, <strong>{{ playerName }}</strong>!</p>
      <p>Vous avez obtenu <strong>{{ score }} / {{ totalNumberOfQuestion }}</strong></p>
    </div>

    <!-- Les deux tableaux côte à côte -->
    <div class="row justify-content-center mb-5">
      <!-- Les voisins de scores -->
      <div class="col-md-6">
        <h2 class="text-center">Tes voisins de scores</h2>
        <div class="table-responsive">
          <table class="table table-striped table-bordered table-hover">
            <thead class="thead-light">
              <tr>
                <th scope="col">Pseudo</th>
                <th scope="col">Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="playersBefore">
                <td>...</td>
                <td>...</td>
              </tr>
              <tr v-for="(scoreEntry) in getFivePlayerNearPlayer()" :key="scoreEntry.date">
                <td>{{ scoreEntry.playerName }}</td>
                <td>{{ scoreEntry.score }}</td>
              </tr>
              <tr v-if="playersAfter">
                <td>...</td>
                <td>...</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Les 5 meilleurs scores -->
      <div class="col-md-6">
        <h2 class="text-center">Les 5 meilleurs</h2>
        <div class="table-responsive">
          <table class="table table-striped table-bordered table-hover">
            <thead class="thead-dark">
              <tr>
                <th scope="col">#</th>
                <th scope="col">Pseudo</th>
                <th scope="col">Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(scoreEntry, index) in getFiveBest()" :key="scoreEntry.date">
                <th scope="row">{{ index + 1 }}</th>
                <td>{{ scoreEntry.playerName }}</td>
                <td>{{ scoreEntry.score }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="text-center">
      <button class="btn btn-primary btn-lg" type="button" @click="$router.push('/')">Retour à la home</button>
    </div>
  </div>
</template>




<style scoped>
.container {
  max-width: 1000px;
  margin: auto;
}

.table-responsive {
  margin-top: 20px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}

thead.thead-light {
  background-color: #eef;
}

thead.thead-dark {
  background-color: #ddd;
}

h1,
h2 {
  color: #333;
}

button.btn {
  margin-top: 20px;
}
</style>



<script>
import quizApiService from "../services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: "ResultPage",
  data() {
    return {
      registeredScores: [],
      score: 0,
      playerName: '',
      totalNumberOfQuestion: 0,
      playersBefore: false,
      playersAfter: false,
    };
  },
  async created() {

    let response = await quizApiService.getQuizInfo();
    participationStorageService.saveTotalQuestions(response.data.size);

    this.registeredScores = response.data.scores;
    this.score = participationStorageService.getParticipationScore();
    this.playerName = participationStorageService.getPlayerName();
    this.totalNumberOfQuestion = participationStorageService.getTotalQuestions();
  },
  methods: {

    getFiveBest() {
      let scores = this.registeredScores;
      scores.sort(function (a, b) {
        return b.score - a.score;
      });
      return scores.slice(0, 5);
    },

    getFivePlayerNearPlayer() {
      let scores = this.registeredScores;
      scores.sort(function (a, b) {
        return b.score - a.score;
      });
      let playerPosition = scores.findIndex(score => score.playerName === this.playerName);
      let maxIndex = Math.max(0, playerPosition - 2);

      let fiveBest = scores.slice(maxIndex, playerPosition + 3);
      console.log(playerPosition);
      console.log(scores);
      console.log(fiveBest);

      if (playerPosition - 2 > 1) {
        this.playersBefore = true;
      }
      if (playerPosition + 2 < scores.length - 1) {
        this.playersAfter = true;
      }
      return fiveBest;
    }
  }
};
</script>