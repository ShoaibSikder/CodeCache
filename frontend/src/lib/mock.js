// Built-in mock API so the UI runs without the Django backend (VITE_USE_MOCK=true).
// Shapes mirror the endpoints in the project documentation (section 6.1.2).
const C = (id, title, code, language) => ({ id, type: 'code', data: { title, code, language } });
const P = (id, text) => ({ id, type: 'paragraph', data: { text } });
const N = (id, type, text) => ({ id, type, data: { text } });

export const XP = { topic: 20, quiz: 75, daily: 90, bug_fix: 60, note: 15 };

const langs = [
  { id: 'py', slug: 'python', name: 'Python', description: 'Readable syntax for scripting, data and automation.', sections: [
    { id: 'py-1', title: 'Basics', subsections: [
      { id: 'py-1-1', title: 'Variables and types', items: [
        P('a1', 'Python infers types at runtime. Assign with = and check with type().'),
        C('a2', 'Declare values', 'name = "Ada"\nage = 36\nprint(type(name), type(age))', 'python'),
        N('a3', 'tip', 'Use snake_case for variable names. It is the community convention (PEP 8).') ] },
      { id: 'py-1-2', title: 'Lists and loops', items: [
        P('b1', 'Lists are ordered and mutable. A list comprehension builds one in a single line.'),
        C('b2', 'List comprehension', 'squares = [n * n for n in range(5)]\nprint(squares)', 'python'),
        { id: 'b3', type: 'output', data: { text: '[0, 1, 4, 9, 16]' } },
        N('b4', 'warning', 'Do not modify a list while looping over it. Build a new list instead.') ] } ] },
    { id: 'py-2', title: 'Functions', subsections: [
      { id: 'py-2-1', title: 'Defining functions', items: [
        C('c1', 'Default arguments', 'def greet(name="world"):\n    return "Hello, {}".format(name)\n\nprint(greet())', 'python'),
        { id: 'c2', type: 'table', data: { headers: ['Syntax', 'Meaning'], rows: [['*args', 'extra positional arguments'], ['**kwargs', 'extra keyword arguments']] } } ] } ] } ] },
  { id: 'js', slug: 'javascript', name: 'JavaScript', description: 'The language of the browser, now everywhere.', sections: [
    { id: 'js-1', title: 'Basics', subsections: [
      { id: 'js-1-1', title: 'let, const and var', items: [
        P('d1', 'Prefer const. Use let only when you reassign. Avoid var because it is function scoped.'),
        C('d2', 'Block scope', 'const total = 3;\nlet count = 0;\ncount += total;\nconsole.log(count);', 'javascript') ] },
      { id: 'js-1-2', title: 'Array methods', items: [
        C('e1', 'map and filter', 'const nums = [1, 2, 3, 4];\nconst even = nums.filter(n => n % 2 === 0).map(n => n * 10);\nconsole.log(even);', 'javascript'),
        N('e2', 'note', 'map, filter and reduce return new values and do not change the original array.') ] } ] } ] },
  { id: 'cpp', slug: 'cpp', name: 'C++', description: 'Fast, low-level control with modern abstractions.', sections: [
    { id: 'cpp-1', title: 'Basics', subsections: [
      { id: 'cpp-1-1', title: 'Input and output', items: [
        C('f1', 'Hello, streams', '#include <iostream>\nint main() {\n  std::cout << "Hello" << std::endl;\n  return 0;\n}', 'cpp'),
        N('f2', 'tip', 'Compile with g++ -std=c++20 -Wall main.cpp to catch common mistakes early.') ] } ] } ] },
];

const tree = langs;
const flat = () => tree.flatMap(l => l.sections.flatMap(s => s.subsections.map(ss => ({ l, s, ss }))));
const wait = (v, ms = 250) => new Promise(r => setTimeout(() => r(structuredClone(v)), ms));
const reject = (message, status = 400) => Promise.reject({ response: { status, data: { detail: message } } });

const read = () => { try { return JSON.parse(localStorage.getItem('cc_db') || '{}'); } catch { return {}; } };
const write = (x) => localStorage.setItem('cc_db', JSON.stringify(x));
const db = () => ({ xp: 0, streak: 0, last: null, last_language: null, completed: [], saved: [], notes: {}, acts: [], users: [], searches: [], ...read() });
const today = () => new Date().toISOString().slice(0, 10);
const dayDiff = (a, b) => Math.round((new Date(a) - new Date(b)) / 864e5);
const award = (x, xp) => {
  x.xp += xp;
  if (x.last !== today()) { x.streak = x.last && dayDiff(today(), x.last) === 1 ? x.streak + 1 : 1; x.last = today(); }
};

export const mock = {
  languages: () => wait(tree.map(({ sections, ...l }) => ({ ...l, topic_count: sections.reduce((n, s) => n + s.subsections.length, 0) }))),
  language: (slug) => { const l = tree.find(x => x.slug === slug); return l ? wait(l) : reject('Language not found', 404); },
  search(q) {
    if (q.trim().length < 2) return reject('Enter at least 2 characters.');
    const k = q.toLowerCase(); const out = { languages: [], topics: [], snippets: [] };
    tree.forEach(l => (l.name + l.description).toLowerCase().includes(k) && out.languages.push({ slug: l.slug, name: l.name, description: l.description }));
    flat().forEach(({ l, s, ss }) => {
      if ((ss.title + s.title).toLowerCase().includes(k)) out.topics.push({ id: ss.id, title: ss.title, section: s.title, language: l.name, slug: l.slug });
      ss.items.filter(i => JSON.stringify(i.data).toLowerCase().includes(k)).forEach(i => out.snippets.push({ id: i.id, title: i.data.title || ss.title, preview: (i.data.code || i.data.text || '').slice(0, 90), language: l.name, slug: l.slug, topic: ss.title }));
    });
    return wait(out, 200);
  },
  suggestions(q) { const k = q.toLowerCase(); return wait(q.length < 2 ? [] : [...tree.map(l => ({ label: l.name, kind: 'Language', to: `/language/${l.slug}` })), ...flat().map(({ l, ss }) => ({ label: ss.title, kind: l.name, to: `/language/${l.slug}#${ss.id}` }))].filter(x => x.label.toLowerCase().includes(k)).slice(0, 6), 120); },
  auth(kind, p) {
    const x = db();
    if (kind === 'register') {
      if (p.password !== p.password2) return reject('Passwords do not match.');
      if (p.password.length < 8) return reject('Password must be at least 8 characters.');
      if (x.users.some(u => u.email === p.email)) return reject('An account with this email already exists.');
      x.users.push({ id: x.users.length + 1, username: p.username, email: p.email, role: 'user' }); write(x);
    }
    let u = x.users.find(v => v.email === p.email);
    if (!u && kind === 'login' && p.password.length >= 8) { u = { id: x.users.length + 1, username: p.email.split('@')[0], email: p.email, role: /super.?admin/i.test(p.email) ? 'super_admin' : /admin/i.test(p.email) ? 'admin' : 'user' }; x.users.push(u); write(x); }
    if (!u) return reject('Email or password is incorrect.', 401);
    localStorage.setItem('cc_mock_user', JSON.stringify(u));
    return wait({ user: u, access: 'mock-access', refresh: 'mock-refresh' });
  },
  profile: () => { const u = JSON.parse(localStorage.getItem('cc_mock_user') || 'null'); return u ? wait(u, 80) : reject('Not signed in', 401); },
  overview() { const x = db(); return wait({ xp: x.xp, streak: x.streak, last_language: x.last_language, completed: x.completed, saved: x.saved }, 150); },
  complete(id) { const x = db(); const isNew = !x.completed.includes(id); if (isNew) { x.completed.push(id); award(x, XP.topic); write(x); } return wait({ completed: true, xp_awarded: isNew ? XP.topic : 0 }, 150); },
  saved() { const x = db(); return wait(flat().flatMap(({ l, ss }) => ss.items.filter(i => x.saved.includes(i.id)).map(i => ({ id: i.id, title: i.data.title || ss.title, category: ss.title, language: l.name, slug: l.slug, code: i.data.code || i.data.text }))), 150); },
  toggleSaved(id) { const x = db(); const was = x.saved.includes(id); x.saved = was ? x.saved.filter(v => v !== id) : [...x.saved, id]; write(x); return wait({ saved: !was }, 100); },
  note: (slug) => wait({ content: db().notes[slug] || '' }, 100),
  saveNote(slug, content) { const x = db(); const first = !x.notes[slug] && content.trim() && !x.acts.includes(`note:${slug}`); x.notes[slug] = content; if (first) { x.acts.push(`note:${slug}`); award(x, XP.note); } write(x); return wait({ saved: true, xp_awarded: first ? XP.note : 0 }, 80); },
  activity(kind, key) { const x = db(); const k = `${kind}:${key}`; if (x.acts.includes(k)) return wait({ xp_awarded: 0, duplicate: true }, 100); x.acts.push(k); award(x, XP[kind] || 0); write(x); return wait({ xp_awarded: XP[kind] || 0 }, 100); },
  lastLanguage(slug) { const x = db(); x.last_language = slug; write(x); return wait({ ok: true }, 30); },
  runtimes: () => wait(['python', 'javascript', 'cpp', 'java', 'c', 'go'], 100),
  run: (lang, code) => wait({ status: code.trim() ? 'Accepted' : 'No source code', stdout: code.trim() ? '(mock runner) Configure JDoodle in the backend to execute real code.\n' : '', stderr: '', time: '0.02', memory: 3200 }, 700),
  doctor: (lang, code) => wait({ result: `Mock review for ${lang} (${code.split('\n').length} lines)\n\n1. Bugs: none detected in mock mode.\n2. Tip: validate input before using it.\n3. Optimization: prefer built-in helpers over manual loops.\n\nSet VITE_USE_MOCK=false to use the Groq-backed endpoint.` }, 900),
  analytics: () => wait({ views_today: 128, views_yesterday: 104, visitors: 61, searches_30d: 342, views_30d: 3810,
    daily: [42, 58, 51, 77, 90, 104, 128], top_languages: [{ name: 'Python', views: 1420 }, { name: 'JavaScript', views: 1180 }, { name: 'C++', views: 610 }],
    top_searches: [{ q: 'list comprehension', n: 48 }, { q: 'const', n: 31 }, { q: 'pointers', n: 22 }] }),
  users: () => wait(db().users.map(u => ({ ...u, is_active: true }))),
  updateUser(id, changes) { const x = db(); const user = x.users.find(item => String(item.id) === String(id)); if (user) Object.assign(user, changes); write(x); return wait({ ...user, is_active: user?.is_active ?? true }, 120); },
  createItem(subId, item) { flat().find(v => v.ss.id === subId)?.ss.items.push({ id: 'n' + Date.now(), ...item }); return wait({ ok: true }, 150); },
  updateItem(id, item) { flat().forEach(({ ss }) => { ss.items = ss.items.map(current => current.id === id ? { ...current, ...item } : current); }); return wait({ ok: true }, 120); },
  deleteItem(id) { flat().forEach(({ ss }) => { ss.items = ss.items.filter(i => i.id !== id); }); return wait({ ok: true }, 150); },
  adminLanguages: () => wait(tree.map(language => ({ ...language, status: 'active', display_order: 0, section_count: language.sections.length })), 120),
  createLanguage(data) { tree.push({ id: `lang-${Date.now()}`, ...data, sections: [] }); return wait({ ok: true }, 120); },
  updateLanguage(id, data) { Object.assign(tree.find(language => language.id === id) || {}, data); return wait({ ok: true }, 120); },
  deleteLanguage(id) { const index = tree.findIndex(language => language.id === id); if (index >= 0) tree.splice(index, 1); return wait({ ok: true }, 120); },
  adminSections: () => wait(tree.flatMap(language => language.sections.map(section => ({ ...section, language: language.id, language_name: language.name }))), 120),
  createSection(data) { const language = tree.find(item => item.id === data.language); language?.sections.push({ id: `section-${Date.now()}`, ...data, subsections: [] }); return wait({ ok: true }, 120); },
  updateSection(id, data) { const item = tree.flatMap(language => language.sections).find(section => section.id === id); if (item) Object.assign(item, data); return wait({ ok: true }, 120); },
  deleteSection(id) { tree.forEach(language => { language.sections = language.sections.filter(section => section.id !== id); }); return wait({ ok: true }, 120); },
  adminSubsections: () => wait(flat().map(({ l, s, ss }) => ({ ...ss, section: s.id, section_name: s.title, language_name: l.name })), 120),
  createSubsection(data) { const section = tree.flatMap(language => language.sections).find(item => item.id === data.section); section?.subsections.push({ id: `sub-${Date.now()}`, ...data, items: [] }); return wait({ ok: true }, 120); },
  updateSubsection(id, data) { const item = flat().map(row => row.ss).find(subsection => subsection.id === id); if (item) Object.assign(item, data); return wait({ ok: true }, 120); },
  deleteSubsection(id) { tree.forEach(language => language.sections.forEach(section => { section.subsections = section.subsections.filter(subsection => subsection.id !== id); })); return wait({ ok: true }, 120); },
};
export const mockUserCleanup = () => localStorage.removeItem('cc_mock_user');
