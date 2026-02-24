<template>
  <div id="app" class="d-flex flex-column min-vh-100">
    <header>
      <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container-fluid">
          <router-link class="navbar-brand" to="/">Quiz SNK</router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarColor01"
            aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarColor01">
            <ul class="navbar-nav me-auto">
              <li class="nav-item">
                <router-link class="nav-link" to="/">Accueil</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/admin">Administration</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
    <main class="flex-grow-1">
      <router-view></router-view>
    </main>
    <footer class="bg-primary text-white text-center py-3 mt-auto">
      <p>Made with 🧡 by Mame</p>
      <p>Copyright &copy; 2026 - Tous droits réservés</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex-grow: 1;
}

footer {
  background-color: #007bff;
  color: white;
  text-align: center;
  padding: 1rem 0;
  margin-top: auto;
}
</style>
