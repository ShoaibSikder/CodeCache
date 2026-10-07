import axios from 'axios';
import { cachedRequest, clearCacheByPrefix, revalidateCached } from './cache';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const res = await axios.post(`${API_BASE_URL}/api/v1/auth/refresh/`, {
            refresh: refreshToken,
          });
          const newAccess = res.data.data?.access;
          if (newAccess) {
            localStorage.setItem('accessToken', newAccess);
            originalRequest.headers.Authorization = `Bearer ${newAccess}`;
            return api(originalRequest);
          }
        } catch {
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          window.location.href = '/';
        }
      }
    }
    return Promise.reject(error);
  }
);

// ─── Auth API ───
export const authAPI = {
  register: (data) => api.post('/auth/register/', data),
  login: (data) => api.post('/auth/login/', data),
  logout: () => {
    const refresh = localStorage.getItem('refreshToken');
    return api.post('/auth/logout/', { refresh });
  },
  profile: () => api.get('/auth/profile/'),
  refresh: (refreshToken) => api.post('/auth/refresh/', { refresh: refreshToken }),
};

// ─── Languages API ───
export const languagesAPI = {
  list: () => api.get('/languages/'),
  detail: (slug) => api.get(`/languages/${slug}/`),
  cachedList: () =>
    cachedRequest('languages:list', () => api.get('/languages/')),
  cachedDetail: (slug) =>
    cachedRequest(`languages:detail:${slug}`, () => api.get(`/languages/${slug}/`)),
  revalidateList: (onData) =>
    revalidateCached('languages:list', () => api.get('/languages/'), onData),
  revalidateDetail: (slug, onData) =>
    revalidateCached(
      `languages:detail:${slug}`,
      () => api.get(`/languages/${slug}/`),
      onData,
    ),
};

const invalidateContentCache = () => {
  clearCacheByPrefix('languages:');
  clearCacheByPrefix('search:');
};

// ─── Admin API ───
export const adminAPI = {
  languages: {
    list: () => api.get('/admin/languages/'),
    create: (data) => api.post('/admin/languages/', data).finally(invalidateContentCache),
    update: (id, data) => api.put(`/admin/languages/${id}/`, data).finally(invalidateContentCache),
    delete: (id) => api.delete(`/admin/languages/${id}/`).finally(invalidateContentCache),
  },
  sections: {
    list: () => api.get('/admin/sections/'),
    create: (data) => api.post('/admin/sections/', data).finally(invalidateContentCache),
    update: (id, data) => api.put(`/admin/sections/${id}/`, data).finally(invalidateContentCache),
    delete: (id) => api.delete(`/admin/sections/${id}/`).finally(invalidateContentCache),
  },
  subsections: {
    list: () => api.get('/admin/subsections/'),
    create: (data) => api.post('/admin/subsections/', data).finally(invalidateContentCache),
    update: (id, data) => api.put(`/admin/subsections/${id}/`, data).finally(invalidateContentCache),
    delete: (id) => api.delete(`/admin/subsections/${id}/`).finally(invalidateContentCache),
  },
  contentItems: {
    list: () => api.get('/admin/content-items/'),
    create: (data) => api.post('/admin/content-items/', data).finally(invalidateContentCache),
    update: (id, data) => api.put(`/admin/content-items/${id}/`, data).finally(invalidateContentCache),
    delete: (id) => api.delete(`/admin/content-items/${id}/`).finally(invalidateContentCache),
  },
  users: () => api.get('/auth/users/'),
  analytics: () => api.get('/analytics/'),
};

// ─── Search API ───
export const searchAPI = {
  search: (query) => api.get('/search/', { params: { q: query } }),
  suggestions: (query) => api.get('/search/suggestions/', { params: { q: query } }),
  cachedSearch: (query) =>
    cachedRequest(`search:${query}`, () => api.get('/search/', { params: { q: query } })),
};

// ─── Analytics API ───
export const analyticsAPI = {
  trackView: (data) => api.post('/analytics/view/', data),
  trackSearch: (data) => api.post('/analytics/search/', data),
  popular: () => api.get('/analytics/popular/'),
};

// ─── Playground API ───
export const playgroundAPI = {
  run: (data) => api.post('/playground/run/', data),
  languages: () => api.get('/playground/languages/'),
  status: (token) => api.get(`/playground/status/${token}/`),
};

// ─── AI Code Doctor API ───
export const aiAPI = {
  codeDoctor: (code, language = 'javascript') =>
    api.post('/ai/code-doctor/', { code, language }),
  generateQuiz: (language = 'javascript', topic = '') =>
    api.post('/ai/generate-quiz/', { language, topic }),
};

export const learningAPI = {
  overview: () => api.get('/learning/overview/'),
  completeTopic: (subsectionId) => api.post(`/learning/topics/${subsectionId}/complete/`),
  saved: () => api.get('/learning/saved/'),
  toggleSaved: (contentItemId) => api.post('/learning/saved/', { content_item_id: contentItemId }),
  note: (languageSlug) => api.get(`/learning/notes/${languageSlug}/`),
  saveNote: (languageSlug, body) => api.put(`/learning/notes/${languageSlug}/`, { body }),
  recordActivity: (kind, actionKey, languageSlug) =>
    api.post('/learning/activities/', { kind, action_key: actionKey, language_slug: languageSlug }),
  setLastLanguage: (languageSlug) =>
    api.put('/learning/last-language/', { language_slug: languageSlug }),
};

export default api;
