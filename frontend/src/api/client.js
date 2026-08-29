/**
 * Axios API Client
 *
 * Centralized HTTP client with:
 * - Base URL configuration
 * - Request interceptors (attach JWT token)
 * - Response interceptors (handle 401 errors)
 */
import axios from "axios";

let baseURL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";
if (!baseURL.endsWith('/api')) {
  baseURL = baseURL.replace(/\/$/, '') + '/api';
}

const apiClient = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000, // 30 seconds
});

// Automatically attach JWT token to authenticated requests (excluding public auth routes)
apiClient.interceptors.request.use(
  (config) => {
    const publicEndpoints = ['/auth/login', '/auth/register'];
    const isPublicEndpoint = publicEndpoints.some((endpoint) =>
      config.url?.endsWith(endpoint) || config.url?.includes(endpoint)
    );

    if (!isPublicEndpoint) {
      const token = localStorage.getItem("access_token");
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle authentication errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      if (window.location.pathname !== "/login" && window.location.pathname !== "/register") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
