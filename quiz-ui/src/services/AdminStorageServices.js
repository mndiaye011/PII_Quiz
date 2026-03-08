export default {
  // FIX 6: supprime vraiment le token du localStorage
  clear() {
    window.localStorage.removeItem("token");
  },
  saveToken(token) {
    window.localStorage.setItem("token", token);
  },
  getToken() {
    return window.localStorage.getItem("token");
  },
};
