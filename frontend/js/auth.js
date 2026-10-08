/* Auth JavaScript Module */
const authService = {
  async register(email, password, fullName) {
    const data = await apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, full_name: fullName })
    });
    return data;
  },

  async login(email, password) {
    const data = await apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    });
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
  },

  getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  checkAuth() {
    const token = localStorage.getItem('token');
    if (!token && !window.location.pathname.endsWith('login.html') && !window.location.pathname.endsWith('register.html')) {
      window.location.href = 'login.html';
    }
  }
};
