<template>
  <div id="app">
    <header>
      <nav>
          <div class="nav-links">
            <router-link to="/" class="nav-item">
              <span class="nav-icon">🏠</span><span>Home</span>
            </router-link>
            <router-link to="/admin" class="nav-item">
              <span class="nav-icon">✏️</span><span>Admin</span>
            </router-link>
            <router-link to="/about" class="nav-item">
              <span class="nav-icon">💡</span><span>About</span>
            </router-link>
            <!-- Nouveau : login ou profil -->
            <router-link v-if="!currentUser" to="/login" class="nav-item">
              <span class="nav-icon">👤</span><span>Connexion</span>
            </router-link>
            <router-link v-else to="/profile" class="nav-item nav-user">
              <span class="user-avatar">{{ currentUser.username.charAt(0).toUpperCase() }}</span>
              <span>{{ currentUser.username }}</span>
            </router-link>
          </div>
      </nav>
    </header>
    <main>
        <router-view :key="$route.fullPath"></router-view>
    </main>
  </div>
</template>

<script>
import userStorageService from '@/services/UserStorageService';

export default {
  name: 'App',
  data() {
    return {
      currentUser: userStorageService.getUser(), 
    };
  },
  watch: {
    $route() {
      this.currentUser = userStorageService.getUser();
    }
  }
};
</script>

<style>
@import './assets/main.css';

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
main { flex: 1; }

header {
  padding: 18px 24px;
  border-bottom: 1px solid var(--border);
}

nav {
  display: flex;
  justify-content: center;
}

.nav-links {
  display: flex;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 9px 18px;
  border-radius: 99px;
  text-decoration: none;
  color: var(--text-mid);
  font-weight: 700;
  font-size: 15px;
  transition: all 0.18s;
}
.nav-item:hover {
  background: var(--off-white);
  color: var(--text-dark);
}
.nav-item.router-link-active {
  background: var(--navy);
  color: white;
}
.nav-item.router-link-active .nav-icon { filter: grayscale(0); }
.nav-icon { font-size: 17px; }
.nav-user { background: var(--off-white); }
.user-avatar {
  width: 24px; height: 24px; border-radius: 50%;
  background: var(--navy); color: white;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 900;
}
</style>
