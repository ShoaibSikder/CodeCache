import axios from 'axios';
import { mock, mockUserCleanup } from '../lib/mock.js';
import { cached, invalidate } from './cache.js';

export const MOCK = import.meta.env.VITE_USE_MOCK === 'true';
const configuredApiUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '');
const apiBaseUrl = configuredApiUrl.endsWith('/api/v1') ? configuredApiUrl : `${configuredApiUrl}/api/v1`;
const http = axios.create({ baseURL: apiBaseUrl, timeout: 35000 });

export const tokens = {
  get access() { return localStorage.getItem('cc_access') || localStorage.getItem('accessToken'); },
  get refresh() { return localStorage.getItem('cc_refresh') || localStorage.getItem('refreshToken'); },
  set({ access, refresh }) {
    if (access) { localStorage.setItem('cc_access', access); localStorage.setItem('accessToken', access); }
    if (refresh) { localStorage.setItem('cc_refresh', refresh); localStorage.setItem('refreshToken', refresh); }
  },
  clear() { ['cc_access', 'cc_refresh', 'accessToken', 'refreshToken'].forEach(key => localStorage.removeItem(key)); mockUserCleanup(); },
};

http.interceptors.request.use(cfg => { if (tokens.access) cfg.headers.Authorization = `Bearer ${tokens.access}`; return cfg; });
let refreshing = null;
http.interceptors.response.use(r => r, async err => {
  const req = err.config;
  if (err.response?.status === 401 && !req._retry && tokens.refresh && !req.url.includes('/auth/')) {
    req._retry = true; // one refresh attempt only (Scenario-1)
    try {
      refreshing ||= axios.post(`${http.defaults.baseURL}/auth/refresh/`, { refresh: tokens.refresh }).finally(() => { refreshing = null; });
      const { data } = await refreshing;
      const refreshed = data.data || data;
      tokens.set({ access: refreshed.access, refresh: refreshed.refresh });
      return http(req);
    } catch { tokens.clear(); window.location.assign('/'); }
  }
  return Promise.reject(err);
});

export const errorMessage = (e, fallback = 'Something went wrong. Please try again.') =>
  e?.response?.data?.error?.message || e?.response?.data?.detail || Object.values(e?.response?.data?.error?.details || {}).flat()[0] || Object.values(e?.response?.data || {}).flat()[0] || (e?.code === 'ERR_NETWORK' ? 'Cannot reach the server. Check your connection.' : fallback);

const d = (p) => p.then(r => r.data?.data ?? r.data);
const pick = (m, real) => (MOCK ? m() : real());

const normalizeLanguage = (language) => ({
  ...language,
  sections: (language.sections || []).map(section => ({
    ...section,
    subsections: (section.subsections || []).map(subsection => ({
      ...subsection,
      items: subsection.items || subsection.content_items || [],
    })),
  })),
});

const normalizeLanguages = (languages) => languages.map(language => ({
  ...language,
  topic_count: language.topic_count ?? language.section_count ?? 0,
}));

const normalizeOverview = (overview) => ({
  ...overview,
  completed: overview.completed_subsection_ids || overview.completed || [],
  saved: overview.saved_content_item_ids || overview.saved || [],
});

const normalizeRun = (result) => ({
  ...result,
  status: result.status || (result.error ? 'Error' : 'Finished'),
  stdout: result.output || result.stdout || '',
  stderr: result.error || result.stderr || '',
  time: result.execution_time ?? result.time,
  memory: result.memory_used ?? result.memory,
});

export const authAPI = {
  login: (p) => pick(() => mock.auth('login', p), async () => {
    const result = await d(http.post('/auth/login/', p));
    return { user: result.user, ...result.tokens };
  }),
  register: (p) => pick(() => mock.auth('register', p), async () => {
    const result = await d(http.post('/auth/register/', { ...p, password_confirm: p.password2 }));
    return { user: result.user, ...result.tokens };
  }),
  profile: () => pick(() => mock.profile(), () => d(http.get('/auth/profile/'))),
  changePassword: () => pick(() => Promise.resolve({}), () => Promise.resolve({})),
  logout: () => pick(() => Promise.resolve(), () => http.post('/auth/logout/', { refresh: tokens.refresh }).catch(() => {})),
};
export const contentAPI = {
  languages: () => cached('languages', () => pick(() => mock.languages(), async () => normalizeLanguages(await d(http.get('/languages/'))))),
  language: (slug) => cached(`language:${slug}`, () => pick(() => mock.language(slug), async () => normalizeLanguage(await d(http.get(`/languages/${slug}/`))))),
  search: (q) => cached(`search:${q.toLowerCase()}`, () => pick(() => mock.search(q), async () => {
    const result = await d(http.get('/search/', { params: { q } }));
    const grouped = result.grouped || {};
    return {
      languages: grouped.languages || [],
      topics: (grouped.subsections || []).map(item => ({ ...item, title: item.title, language: item.language?.name, slug: item.language?.slug, section: item.section?.title })),
      snippets: (grouped.content_items || []).map(item => ({ ...item, title: item.subsection?.title || item.preview, preview: item.preview || '', slug: item.language?.slug, language: item.language?.name, topic: item.subsection?.title })),
    };
  })),
  suggestions: (q) => pick(() => mock.suggestions(q), async () => {
    const results = await d(http.get('/search/suggestions/', { params: { q } }));
    return (results || []).slice(0, 6).map(item => ({
      label: item.text || item.name || item.title || item.data?.title || item.subsection_name || item.slug,
      kind: item.type || 'topic',
      to: item.url?.replace(/^\/languages\//, '/language/').replace(/\/$/, '').replace(/#.*$/, '') || `/search?q=${encodeURIComponent(q)}`,
    }));
  }),
  track: (path) => { if (!MOCK) http.post('/analytics/view/', { path }).catch(() => {}); },
};
export const learnAPI = {
  overview: () => pick(() => mock.overview(), async () => normalizeOverview(await d(http.get('/learning/overview/')))),
  complete: (id) => pick(() => mock.complete(id), async () => { const result = await d(http.post(`/learning/topics/${id}/complete/`)); return { ...result, xp_awarded: result.awarded_xp }; }),
  saved: () => pick(() => mock.saved(), async () => (await d(http.get('/learning/saved/'))).map(item => ({ ...item, slug: item.language }))),
  toggleSaved: (id) => pick(() => mock.toggleSaved(id), async () => { const result = await d(http.post('/learning/saved/', { content_item_id: id })); return { ...result, id: result.content_item_id }; }),
  note: (slug) => pick(() => mock.note(slug), async () => { const result = await d(http.get(`/learning/notes/${slug}/`)); return { ...result, content: result.body }; }),
  saveNote: (slug, content) => pick(() => mock.saveNote(slug, content), async () => { const result = await d(http.put(`/learning/notes/${slug}/`, { body: content })); return { ...result, content: result.body }; }),
  activity: (kind, key, language) => pick(() => mock.activity(kind, key), () => d(http.post('/learning/activities/', { kind: kind === 'daily' ? 'daily_challenge' : kind, action_key: key, language_slug: language }))),
  lastLanguage: (slug) => pick(() => mock.lastLanguage(slug), () => d(http.put('/learning/last-language/', { language_slug: slug }))),
};
export const toolsAPI = {
  runtimes: () => pick(() => mock.runtimes(), async () => (await d(http.get('/playground/languages/'))).map(item => {
    if (typeof item === 'string') return item;
    const name = (item.name || '').toLowerCase();
    return ({ 'c++': 'cpp', 'node.js': 'javascript', 'python 3': 'python' })[name] || name || item.slug || item.id;
  })),
  run: (language, code, stdin = '') => pick(() => mock.run(language, code), async () => normalizeRun(await d(http.post('/playground/run/', { language, code, stdin })))),
  doctor: (language, code) => pick(() => mock.doctor(language, code), async () => { const result = await d(http.post('/ai/code-doctor/', { language, code })); return { ...result, result: result.result }; }),
  quiz: (language, topic) => (MOCK ? Promise.reject(new Error('mock')) : d(http.post('/ai/generate-quiz/', { language, topic }))),
};
export const adminAPI = {
  analytics: () => pick(() => mock.analytics(), async () => {
    const data = await d(http.get('/analytics/'));
    return {
      views_today: data.overview.today_views,
      views_yesterday: data.overview.yesterday_views,
      visitors: data.overview.unique_visitors_today,
      views_30d: data.overview.total_month_views,
      searches_30d: data.overview.total_month_searches,
      daily: (data.daily_views || []).map(day => day.views),
      top_languages: (data.top_languages || []).map(row => ({ name: row.language__name, views: row.view_count })),
      top_searches: (data.top_searches || []).map(row => ({ q: row.query, n: row.count })),
    };
  }),
  users: () => pick(() => mock.users(), () => d(http.get('/auth/users/'))),
  updateUser: (id, changes) => pick(() => mock.updateUser(id, changes), () => d(http.patch(`/auth/users/${id}/`, changes))),
  languages: () => pick(() => mock.adminLanguages(), () => d(http.get('/admin/languages/'))),
  createLanguage: (data) => pick(() => mock.createLanguage(data), () => d(http.post('/admin/languages/', data))).finally(() => invalidate('languages')),
  updateLanguage: (id, data) => pick(() => mock.updateLanguage(id, data), () => d(http.put(`/admin/languages/${id}/`, data))).finally(() => invalidate('languages')),
  deleteLanguage: (id) => pick(() => mock.deleteLanguage(id), () => d(http.delete(`/admin/languages/${id}/`))).finally(() => invalidate('languages')),
  sections: () => pick(() => mock.adminSections(), () => d(http.get('/admin/sections/'))),
  createSection: (data) => pick(() => mock.createSection(data), () => d(http.post('/admin/sections/', data))).finally(() => invalidate('language')),
  updateSection: (id, data) => pick(() => mock.updateSection(id, data), () => d(http.put(`/admin/sections/${id}/`, data))).finally(() => invalidate('language')),
  deleteSection: (id) => pick(() => mock.deleteSection(id), () => d(http.delete(`/admin/sections/${id}/`))).finally(() => invalidate('language')),
  subsections: () => pick(() => mock.adminSubsections(), () => d(http.get('/admin/subsections/'))),
  createSubsection: (data) => pick(() => mock.createSubsection(data), () => d(http.post('/admin/subsections/', data))).finally(() => invalidate('language')),
  updateSubsection: (id, data) => pick(() => mock.updateSubsection(id, data), () => d(http.put(`/admin/subsections/${id}/`, data))).finally(() => invalidate('language')),
  deleteSubsection: (id) => pick(() => mock.deleteSubsection(id), () => d(http.delete(`/admin/subsections/${id}/`))).finally(() => invalidate('language')),
  createItem: (sub, item) => pick(() => mock.createItem(sub, item), () => d(http.post('/admin/content-items/', { subsection: sub, ...item }))).finally(() => invalidate('language')),
  updateItem: (id, item) => pick(() => mock.updateItem(id, item), () => d(http.put(`/admin/content-items/${id}/`, item))).finally(() => invalidate('language')),
  deleteItem: (id) => pick(() => mock.deleteItem(id), () => d(http.delete(`/admin/content-items/${id}/`))).finally(() => invalidate('language')),
};
