export default {
  saveUser(user) {
    window.localStorage.setItem("user", JSON.stringify(user));
  },
  getUser() {
    const u = window.localStorage.getItem("user");
    return u ? JSON.parse(u) : null;
  },
  isLoggedIn() {
    return !!this.getUser();
  },
  logout() {
    window.localStorage.removeItem("user");
  },
};