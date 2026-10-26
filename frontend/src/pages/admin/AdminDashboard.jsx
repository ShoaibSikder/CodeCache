import { useEffect, useMemo, useState } from 'react';
import { BarChart3, Pencil, Plus, RefreshCw, Trash2, X } from 'lucide-react';
import { toast } from 'sonner';
import { useAuth } from '../../context/AuthContext.jsx';
import { ErrorNote, PageSkeleton } from '../../components/Skeleton.jsx';
import { adminAPI, contentAPI, errorMessage } from '../../services/api.js';
import { setPageTitle } from '../../lib/site.js';

const sections = {
  overview: { title: 'Overview', description: 'Site activity and learning content at a glance.' },
  languages: { title: 'Languages', description: 'Create, edit, and organize programming languages.' },
  structure: { title: 'Sections & topics', description: 'Organize the learning path for each language.' },
  content: { title: 'Content items', description: 'Manage lessons, examples, notes, and references.' },
  users: { title: 'Users & roles', description: 'Review accounts and manage access.' },
};
const TYPES = ['heading', 'paragraph', 'code', 'table', 'note', 'warning', 'tip', 'output', 'divider', 'image'];
const DEFAULTS = { heading: { text: '' }, paragraph: { text: '' }, code: { title: '', language: 'python', code: '' }, table: { headers: ['A', 'B'], rows: [['', '']] }, note: { text: '' }, warning: { text: '' }, tip: { text: '' }, output: { text: '' }, divider: {}, image: { url: '', alt: '' } };
const blankLanguage = { name: '', slug: '', description: '', status: 'active', display_order: 0 };
const field = 'input';
const slugify = value => value.toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

function Overview() {
  const [stats, setStats] = useState(null); const [error, setError] = useState(''); const [reload, setReload] = useState(0);
  useEffect(() => { setError(''); adminAPI.analytics().then(setStats).catch(err => setError(errorMessage(err))); }, [reload]);
  if (error) return <ErrorNote message={error} onRetry={() => setReload(value => value + 1)} />;
  if (!stats) return <PageSkeleton />;
  const max = Math.max(1, ...(stats.daily || []));
  const cards = [['Views today', stats.views_today], ['Visitors today', stats.visitors], ['Views, 30 days', stats.views_30d], ['Searches, 30 days', stats.searches_30d]];
  return <div className="space-y-6">
    <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">{cards.map(([label, value]) => <div key={label} className="card p-4"><p className="text-sm text-muted">{label}</p><p className="mt-1 font-display text-2xl font-bold">{value ?? 0}</p></div>)}</div>
    <section className="card p-5"><h2 className="mb-4 flex items-center gap-2 font-semibold"><BarChart3 size={18} className="text-brand" />Daily views, last 7 days</h2><div className="flex h-40 items-end gap-2" role="img" aria-label={`Daily views: ${(stats.daily || []).join(', ')}`}>{(stats.daily || []).map((value, index) => <div key={index} className="flex h-full flex-1 flex-col items-center justify-end gap-1"><span className="text-xs text-muted">{value}</span><div className="w-full rounded-t bg-brand" style={{ height: `${Math.max(2, value / max * 100)}%` }} /></div>)}</div></section>
    <div className="grid gap-4 md:grid-cols-2"><Ranked title="Top languages" rows={(stats.top_languages || []).map(item => [item.name, item.views])} /><Ranked title="Top searches" rows={(stats.top_searches || []).map(item => [item.q, item.n])} /></div>
  </div>;
}

function Ranked({ title, rows }) {
  return <section className="card p-5"><h2 className="mb-3 font-semibold">{title}</h2>{rows.length ? <ol className="space-y-2 text-sm">{rows.map(([label, value], index) => <li key={`${label}-${index}`} className="flex justify-between gap-4"><span className="min-w-0 truncate">{label}</span><span className="shrink-0 text-muted">{value}</span></li>)}</ol> : <p className="text-sm text-muted">No activity yet.</p>}</section>;
}

function Languages() {
  const [rows, setRows] = useState(null); const [form, setForm] = useState(blankLanguage); const [editing, setEditing] = useState(''); const [error, setError] = useState(''); const [busy, setBusy] = useState(false);
  const load = () => adminAPI.languages().then(setRows).catch(err => setError(errorMessage(err)));
  useEffect(() => { load(); }, []);
  const update = (key, value) => setForm(current => ({ ...current, [key]: value }));
  async function submit(event) {
    event.preventDefault(); setError(''); setBusy(true);
    try {
      const payload = { ...form, display_order: Number(form.display_order) || 0 };
      if (editing) await adminAPI.updateLanguage(editing, payload); else await adminAPI.createLanguage(payload);
      toast.success(editing ? 'Language updated' : 'Language created'); setForm(blankLanguage); setEditing(''); await load();
    } catch (err) { setError(errorMessage(err)); } finally { setBusy(false); }
  }
  async function remove(language) {
    if (!window.confirm(`Delete ${language.name} and all of its sections, topics, and content? This cannot be undone.`)) return;
    try { await adminAPI.deleteLanguage(language.id); toast.success('Language deleted'); if (editing === language.id) { setEditing(''); setForm(blankLanguage); } await load(); }
    catch (err) { setError(errorMessage(err)); }
  }
  return <div className="grid items-start gap-6 xl:grid-cols-[minmax(0,1fr)_360px]">
    <section className="card overflow-hidden"><div className="flex items-center justify-between border-b border-line p-4"><h2 className="font-semibold">Languages ({rows?.length ?? '...'})</h2><button className="btn-icon" onClick={load} aria-label="Refresh languages"><RefreshCw size={17} /></button></div>
      {error && <p role="alert" className="m-4 rounded-lg bg-danger/5 p-3 text-sm text-danger">{error}</p>}
      {!rows ? <div className="p-5"><PageSkeleton /></div> : rows.length ? <ul className="divide-y divide-line">{rows.map(language => <li key={language.id} className="flex flex-wrap items-center justify-between gap-3 p-4"><div className="min-w-0"><p className="font-semibold">{language.name}<span className="ml-2 rounded bg-bg px-2 py-0.5 text-xs font-normal text-muted">{language.status}</span></p><p className="text-sm text-muted">/{language.slug} · {language.section_count ?? 0} sections</p></div><div className="flex gap-1"><button className="btn-icon" aria-label={`Edit ${language.name}`} onClick={() => { setEditing(language.id); setForm({ name: language.name, slug: language.slug, description: language.description || '', status: language.status || 'active', display_order: language.display_order || 0 }); }}><Pencil size={16} /></button><button className="btn-icon text-danger" aria-label={`Delete ${language.name}`} onClick={() => remove(language)}><Trash2 size={16} /></button></div></li>)}</ul> : <p className="p-5 text-sm text-muted">No languages yet. Add one to begin structuring content.</p>}
    </section>
    <form onSubmit={submit} className="card space-y-3 p-5"><h2 className="font-semibold">{editing ? 'Edit language' : 'Add language'}</h2>
      <div><label htmlFor="language-name" className="mb-1 block text-sm font-medium">Name</label><input id="language-name" className={field} required value={form.name} onChange={event => { update('name', event.target.value); if (!editing) update('slug', slugify(event.target.value)); }} /></div>
      <div><label htmlFor="language-slug" className="mb-1 block text-sm font-medium">Slug</label><input id="language-slug" className={field} required value={form.slug} onChange={event => update('slug', slugify(event.target.value))} /></div>
      <div><label htmlFor="language-description" className="mb-1 block text-sm font-medium">Description</label><textarea id="language-description" className={`${field} py-2`} rows="3" value={form.description} onChange={event => update('description', event.target.value)} /></div>
      <div className="grid grid-cols-2 gap-3"><div><label htmlFor="language-status" className="mb-1 block text-sm font-medium">Status</label><select id="language-status" className={field} value={form.status} onChange={event => update('status', event.target.value)}><option value="active">Active</option><option value="draft">Draft</option><option value="inactive">Inactive</option><option value="archived">Archived</option></select></div><div><label htmlFor="language-order" className="mb-1 block text-sm font-medium">Order</label><input id="language-order" type="number" min="0" className={field} value={form.display_order} onChange={event => update('display_order', event.target.value)} /></div></div>
      <div className="flex gap-2">{editing && <button type="button" className="btn-ghost" onClick={() => { setEditing(''); setForm(blankLanguage); }}><X size={16} />Cancel</button>}<button className="btn-primary flex-1" disabled={busy}><Plus size={16} />{busy ? 'Saving...' : editing ? 'Save changes' : 'Create language'}</button></div>
    </form>
  </div>;
}

function Structure() {
  const [languages, setLanguages] = useState([]); const [sections, setSections] = useState([]); const [subsections, setSubsections] = useState([]);
  const [language, setLanguage] = useState(''); const [section, setSection] = useState(''); const [sectionForm, setSectionForm] = useState({ title: '', slug: '' }); const [subForm, setSubForm] = useState({ title: '', slug: '' }); const [editingSection, setEditingSection] = useState(''); const [editingSub, setEditingSub] = useState(''); const [error, setError] = useState('');
  const load = async () => { try { const [ls, ss, subs] = await Promise.all([adminAPI.languages(), adminAPI.sections(), adminAPI.subsections()]); setLanguages(ls); setSections(ss); setSubsections(subs); setLanguage(current => current || String(ls[0]?.id || '')); } catch (err) { setError(errorMessage(err)); } };
  useEffect(() => { load(); }, []);
  const languageSections = sections.filter(item => String(item.language) === language);
  const sectionSubsections = subsections.filter(item => String(item.section) === section);
  useEffect(() => { if (!languageSections.some(item => String(item.id) === section)) setSection(String(languageSections[0]?.id || '')); }, [language, sections]);
  async function addSection(event) { event.preventDefault(); try { if (editingSection) await adminAPI.updateSection(editingSection, sectionForm); else await adminAPI.createSection({ language, ...sectionForm, display_order: languageSections.length }); toast.success(editingSection ? 'Section updated' : 'Section created'); setEditingSection(''); setSectionForm({ title: '', slug: '' }); await load(); } catch (err) { setError(errorMessage(err)); } }
  async function addSubsection(event) { event.preventDefault(); try { if (editingSub) await adminAPI.updateSubsection(editingSub, subForm); else await adminAPI.createSubsection({ section, ...subForm, display_order: sectionSubsections.length }); toast.success(editingSub ? 'Topic updated' : 'Topic created'); setEditingSub(''); setSubForm({ title: '', slug: '' }); await load(); } catch (err) { setError(errorMessage(err)); } }
  async function removeSection(item) { if (!window.confirm(`Delete ${item.title} and all child topics/content?`)) return; try { await adminAPI.deleteSection(item.id); toast.success('Section deleted'); await load(); } catch (err) { setError(errorMessage(err)); } }
  async function removeSubsection(item) { if (!window.confirm(`Delete topic “${item.title}” and its content?`)) return; try { await adminAPI.deleteSubsection(item.id); toast.success('Topic deleted'); await load(); } catch (err) { setError(errorMessage(err)); } }
  return <div className="space-y-5">
    {error && <p role="alert" className="rounded-lg border border-danger/30 bg-danger/5 p-3 text-sm text-danger">{error}</p>}
    <div className="card grid gap-4 p-4 sm:grid-cols-2"><div><label htmlFor="structure-language" className="mb-1 block text-sm font-medium">Language</label><select id="structure-language" className={field} value={language} onChange={event => { setLanguage(event.target.value); setEditingSection(''); setEditingSub(''); setSectionForm({ title: '', slug: '' }); setSubForm({ title: '', slug: '' }); }}>{languages.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</select></div><div><label htmlFor="structure-section" className="mb-1 block text-sm font-medium">Selected section</label><select id="structure-section" className={field} value={section} onChange={event => { setSection(event.target.value); setEditingSub(''); setSubForm({ title: '', slug: '' }); }}>{languageSections.map(item => <option key={item.id} value={item.id}>{item.title}</option>)}</select></div></div>
    <div className="grid items-start gap-5 lg:grid-cols-2">
      <section className="card p-5"><h2 className="font-semibold">Sections in {languages.find(item => String(item.id) === language)?.name || 'language'}</h2><ul className="my-4 divide-y divide-line">{languageSections.map(item => <li key={item.id} className="flex items-center justify-between gap-2 py-2"><button className={`min-w-0 flex-1 truncate text-left text-sm ${String(item.id) === section ? 'font-semibold text-brand' : 'text-ink'}`} onClick={() => setSection(String(item.id))}>{item.title} <span className="text-muted">/{item.slug}</span></button><button className="btn-icon" aria-label={`Edit ${item.title}`} onClick={() => { setSection(String(item.id)); setEditingSection(item.id); setSectionForm({ title: item.title, slug: item.slug }); }}><Pencil size={15} /></button><button className="btn-icon text-danger" aria-label={`Delete ${item.title}`} onClick={() => removeSection(item)}><Trash2 size={16} /></button></li>)}</ul>
        <form onSubmit={addSection} className="space-y-3 border-t border-line pt-4"><h3 className="text-sm font-semibold">{editingSection ? 'Edit section' : 'Add section'}</h3><input className={field} required aria-label="Section title" placeholder="Section title" value={sectionForm.title} onChange={event => { setSectionForm(current => ({ ...current, title: event.target.value, slug: slugify(event.target.value) })); }} /><input className={field} required aria-label="Section slug" placeholder="section-slug" value={sectionForm.slug} onChange={event => setSectionForm(current => ({ ...current, slug: slugify(event.target.value) }))} /><div className="flex gap-2">{editingSection && <button type="button" className="btn-ghost" onClick={() => { setEditingSection(''); setSectionForm({ title: '', slug: '' }); }}><X size={16} />Cancel</button>}<button className="btn-primary" disabled={!language}><Plus size={16} />{editingSection ? 'Save section' : 'Add section'}</button></div></form>
      </section>
      <section className="card p-5"><h2 className="font-semibold">Topics in selected section</h2><ul className="my-4 divide-y divide-line">{sectionSubsections.map(item => <li key={item.id} className="flex items-center justify-between gap-2 py-2"><span className="min-w-0 flex-1 truncate text-sm">{item.title} <span className="text-muted">/{item.slug}</span></span><button className="btn-icon" aria-label={`Edit ${item.title}`} onClick={() => { setEditingSub(item.id); setSubForm({ title: item.title, slug: item.slug }); }}><Pencil size={15} /></button><button className="btn-icon text-danger" aria-label={`Delete ${item.title}`} onClick={() => removeSubsection(item)}><Trash2 size={16} /></button></li>)}</ul>
        <form onSubmit={addSubsection} className="space-y-3 border-t border-line pt-4"><h3 className="text-sm font-semibold">{editingSub ? 'Edit topic' : 'Add topic'}</h3><input className={field} required aria-label="Topic title" placeholder="Topic title" value={subForm.title} onChange={event => setSubForm(current => ({ ...current, title: event.target.value, slug: slugify(event.target.value) }))} /><input className={field} required aria-label="Topic slug" placeholder="topic-slug" value={subForm.slug} onChange={event => setSubForm(current => ({ ...current, slug: slugify(event.target.value) }))} /><div className="flex gap-2">{editingSub && <button type="button" className="btn-ghost" onClick={() => { setEditingSub(''); setSubForm({ title: '', slug: '' }); }}><X size={16} />Cancel</button>}<button className="btn-primary" disabled={!section}><Plus size={16} />{editingSub ? 'Save topic' : 'Add topic'}</button></div></form>
      </section>
    </div>
  </div>;
}

function Content() {
  const [languages, setLanguages] = useState([]); const [slug, setSlug] = useState(''); const [tree, setTree] = useState(null); const [sub, setSub] = useState('');
  const [type, setType] = useState('paragraph'); const [json, setJson] = useState(JSON.stringify(DEFAULTS.paragraph, null, 2)); const [jsonError, setJsonError] = useState(''); const [loadError, setLoadError] = useState(''); const [editing, setEditing] = useState(null); const [busy, setBusy] = useState(false);
  useEffect(() => { adminAPI.languages().then(items => { const active = items.filter(item => item.status === 'active'); setLanguages(active); setSlug(current => current || active[0]?.slug || ''); }).catch(err => setLoadError(errorMessage(err))); }, []);
  const load = async () => { if (!slug) return; setLoadError(''); try { const value = await contentAPI.language(slug); setTree(value); setSub(current => current || value.sections[0]?.subsections[0]?.id || ''); } catch (err) { setLoadError(errorMessage(err)); setTree(null); } };
  useEffect(() => { setTree(null); setSub(''); setEditing(null); load(); }, [slug]);
  const topics = tree?.sections.flatMap(section => section.subsections.map(topic => ({ ...topic, label: `${section.title} / ${topic.title}` }))) || [];
  const selectedTopic = topics.find(topic => String(topic.id) === String(sub));
  function startEdit(item) { setEditing(item); setType(item.type); setJson(JSON.stringify(item.data || {}, null, 2)); setJsonError(''); }
  function resetEditor() { setEditing(null); setType('paragraph'); setJson(JSON.stringify(DEFAULTS.paragraph, null, 2)); setJsonError(''); }
  async function submit(event) {
    event.preventDefault(); let data;
    try { data = JSON.parse(json); if (!data || typeof data !== 'object' || Array.isArray(data)) throw new Error(); } catch { setJsonError('Content data must be a valid JSON object.'); return; }
    setJsonError(''); setBusy(true);
    try { if (editing) await adminAPI.updateItem(editing.id, { type, data }); else await adminAPI.createItem(sub, { type, data }); toast.success(editing ? 'Content item updated' : 'Content item added'); resetEditor(); await load(); }
    catch (err) { setLoadError(errorMessage(err)); } finally { setBusy(false); }
  }
  async function remove(item) { if (!window.confirm('Delete this content item? This cannot be undone.')) return; try { await adminAPI.deleteItem(item.id); toast.success('Content item deleted'); if (editing?.id === item.id) resetEditor(); await load(); } catch (err) { setLoadError(errorMessage(err)); } }
  return <div className="grid items-start gap-6 xl:grid-cols-2">
    <section className="space-y-4"><div className="grid gap-3 sm:grid-cols-2"><div><label htmlFor="content-language" className="mb-1 block text-sm font-medium">Language</label><select id="content-language" className={field} value={slug} onChange={event => setSlug(event.target.value)}>{languages.map(item => <option key={item.slug} value={item.slug}>{item.name}</option>)}</select></div><div><label htmlFor="content-topic" className="mb-1 block text-sm font-medium">Topic</label><select id="content-topic" className={field} value={sub} onChange={event => setSub(event.target.value)}>{topics.map(item => <option key={item.id} value={item.id}>{item.label}</option>)}</select></div></div>
      {loadError && <ErrorNote message={loadError} onRetry={load} />}
      <div className="flex items-center justify-between"><h2 className="font-semibold">Content items ({selectedTopic?.items.length || 0})</h2><button className="btn-icon" onClick={load} aria-label="Refresh content"><RefreshCw size={16} /></button></div>
      <ul className="space-y-2">{selectedTopic?.items.map(item => <li key={item.id} className="card flex items-center justify-between gap-3 p-3 text-sm"><span className="min-w-0"><span className="mr-2 rounded bg-bg px-1.5 py-0.5 font-mono text-xs">{item.type}</span><span className="truncate">{item.data?.title || item.data?.text || item.data?.code?.slice(0, 60) || '(content item)'}</span></span><span className="flex shrink-0"><button className="btn-icon" aria-label={`Edit ${item.type} item`} onClick={() => startEdit(item)}><Pencil size={16} /></button><button className="btn-icon text-danger" aria-label={`Delete ${item.type} item`} onClick={() => remove(item)}><Trash2 size={16} /></button></span></li>)}</ul>
    </section>
    <form onSubmit={submit} className="card space-y-3 p-5"><div className="flex items-center justify-between gap-3"><h2 className="font-semibold">{editing ? 'Edit content item' : 'Add content item'}</h2>{editing && <button type="button" className="btn-icon" onClick={resetEditor} aria-label="Cancel edit"><X size={17} /></button>}</div>
      <div><label htmlFor="content-type" className="mb-1 block text-sm font-medium">Type</label><select id="content-type" className={field} value={type} onChange={event => { setType(event.target.value); setJson(JSON.stringify(DEFAULTS[event.target.value], null, 2)); }}>{TYPES.map(item => <option key={item}>{item}</option>)}</select></div>
      <div><label htmlFor="content-json" className="mb-1 block text-sm font-medium">Data (JSON)</label><textarea id="content-json" rows="11" value={json} onChange={event => setJson(event.target.value)} spellCheck={false} aria-invalid={!!jsonError} className={`${field} py-2 font-mono`} />{jsonError && <p role="alert" className="mt-1 text-xs text-danger">{jsonError}</p>}</div>
      <button className="btn-primary" disabled={!sub || busy}>{busy ? 'Saving...' : editing ? 'Save changes' : 'Add item'}</button>
    </form>
  </div>;
}

function Users() {
  const { user: currentUser } = useAuth();
  const [users, setUsers] = useState(null); const [error, setError] = useState(''); const [query, setQuery] = useState(''); const [saving, setSaving] = useState('');
  useEffect(() => { adminAPI.users().then(setUsers).catch(err => setError(errorMessage(err))); }, []);
  const filtered = useMemo(() => (users || []).filter(user => `${user.username} ${user.email} ${user.role}`.toLowerCase().includes(query.toLowerCase())), [users, query]);
  const canManageRoles = currentUser?.role === 'super_admin';
  async function update(user, changes) {
    setError(''); setSaving(String(user.id));
    try { const updated = await adminAPI.updateUser(user.id, changes); setUsers(rows => rows.map(row => row.id === user.id ? updated : row)); toast.success('Account updated'); }
    catch (err) { setError(errorMessage(err)); }
    finally { setSaving(''); }
  }
  if (error) return <ErrorNote message={error} />; if (!users) return <PageSkeleton />;
  return <section className="card overflow-hidden"><div className="flex flex-col justify-between gap-3 border-b border-line p-4 sm:flex-row sm:items-center"><div><h2 className="font-semibold">Accounts</h2><p className="text-sm text-muted">{canManageRoles ? 'Super-admin role and access controls.' : 'Only super-admins can change roles and account access.'}</p></div><input className={`${field} sm:max-w-xs`} type="search" aria-label="Search accounts" placeholder="Search username, email, role" value={query} onChange={event => setQuery(event.target.value)} /></div>{error && <p role="alert" className="m-4 rounded-lg bg-danger/5 p-3 text-sm text-danger">{error}</p>}<div className="overflow-x-auto"><table className="w-full min-w-[760px] text-left text-sm"><caption className="sr-only">Registered accounts</caption><thead className="bg-bg"><tr>{['Username', 'Email', 'Role', 'Status'].map(label => <th key={label} scope="col" className="px-4 py-3">{label}</th>)}</tr></thead><tbody>{filtered.map(account => { const self = String(account.id) === String(currentUser?.id); const busy = saving === String(account.id); return <tr key={account.id} className="border-t border-line"><td className="px-4 py-3 font-medium">{account.username}{self && <span className="ml-2 text-xs text-muted">You</span>}</td><td className="px-4 py-3">{account.email}</td><td className="px-4 py-3">{canManageRoles ? <select aria-label={`Role for ${account.username}`} className="input min-h-9 max-w-40 py-1 text-xs" value={account.role} disabled={busy || self} onChange={event => update(account, { role: event.target.value })}>{['user', 'editor', 'admin', 'super_admin'].map(role => <option key={role} value={role}>{role}</option>)}</select> : <span className="rounded bg-brand/10 px-2 py-1 text-xs font-semibold text-brand">{account.role}</span>}</td><td className="px-4 py-3">{canManageRoles ? <label className="inline-flex items-center gap-2"><input type="checkbox" className="h-4 w-4 accent-brand" checked={account.is_active} disabled={busy || self} onChange={event => update(account, { is_active: event.target.checked })} /><span>{account.is_active ? 'Active' : 'Inactive'}</span></label> : account.is_active ? 'Active' : 'Inactive'}</td></tr>; })}{!filtered.length && <tr><td colSpan="4" className="px-4 py-8 text-center text-muted">No matching accounts.</td></tr>}</tbody></table></div></section>;
}

export default function AdminDashboard({ section = 'overview' }) {
  useEffect(() => { setPageTitle(sections[section]?.title ?? 'Admin'); }, [section]);
  const panel = section === 'overview' ? <Overview /> : section === 'languages' ? <Languages /> : section === 'structure' ? <Structure /> : section === 'content' ? <Content /> : <Users />;
  const current = sections[section] || sections.overview;
  return <div>
    <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
      <div><p className="text-sm font-semibold text-brand">CODECACHE CONTROL PANEL</p><h1 className="mt-1 text-3xl font-bold">{current.title}</h1></div>
      <p className="text-sm text-muted">{current.description}</p>
    </div>
    {panel}
  </div>;
}
