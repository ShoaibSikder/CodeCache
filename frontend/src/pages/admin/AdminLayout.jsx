import { useState } from 'react';
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import { ArrowLeft, BarChart3, Code2, FileCode2, LayoutDashboard, ListTree, LogOut, Menu, ShieldCheck, UsersRound, X } from 'lucide-react';
import { useAuth } from '../../context/AuthContext.jsx';
import Logo from '../../components/Logo.jsx';

const adminLinks = [
  { to: '/admin/dashboard', label: 'Overview', icon: LayoutDashboard, end: true },
  { to: '/admin/languages', label: 'Languages', icon: Code2 },
  { to: '/admin/sections', label: 'Sections & topics', icon: ListTree },
  { to: '/admin/content', label: 'Content items', icon: FileCode2 },
  { to: '/admin/users', label: 'Users & roles', icon: UsersRound },
];

function AdminNavigation({ onSelect }) {
  return <nav aria-label="Admin navigation" className="space-y-1">
    {adminLinks.map(({ to, label, icon: Icon, end }) => <NavLink key={to} to={to} end={end} onClick={onSelect} className={({ isActive }) => `flex min-h-11 items-center gap-3 rounded-lg px-3 text-sm font-medium transition-colors ${isActive ? 'bg-brand/10 text-brand' : 'text-muted hover:bg-bg hover:text-ink'}`}>
      <Icon size={18} aria-hidden="true" />{label}
    </NavLink>)}
  </nav>;
}

export default function AdminLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  async function signOut() {
    await logout();
    navigate('/admin/login', { replace: true });
  }

  return (
    <div className="flex min-h-screen flex-col bg-bg text-ink">
      <header className="sticky top-0 z-30 border-b border-line bg-surface/95 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-7xl items-center gap-3 px-4 sm:px-6">
          <button type="button" onClick={() => setMenuOpen(true)} className="btn-icon xl:hidden" aria-label="Open admin navigation" aria-expanded={menuOpen}>
            <Menu size={19} aria-hidden="true" />
          </button>
          <Link to="/admin/dashboard" aria-label="Admin overview"><Logo sub={null} /></Link>
          <span className="hidden h-8 border-l border-line sm:block" aria-hidden="true" />
          <span className="hidden items-center gap-1.5 rounded-md bg-brand/10 px-2.5 py-1 text-xs font-semibold text-brand sm:inline-flex"><ShieldCheck size={14} aria-hidden="true" />Admin panel</span>
          <div className="ml-auto flex items-center gap-2">
            <span className="hidden max-w-52 truncate text-sm text-muted sm:block">{user?.email}</span>
            <Link to="/" className="btn-ghost hidden sm:inline-flex"><ArrowLeft size={16} aria-hidden="true" />Public site</Link>
            <button type="button" onClick={signOut} className="btn-icon" aria-label="Sign out of admin"><LogOut size={18} aria-hidden="true" /></button>
          </div>
        </div>
      </header>

      <div className="mx-auto flex w-full max-w-7xl flex-1 items-start gap-6 px-4 py-6 sm:px-6 lg:py-8">
        <aside className="sticky top-24 hidden w-60 shrink-0 rounded-xl border border-line bg-surface p-3 xl:block">
          <p className="mb-3 px-3 pt-1 text-xs font-semibold uppercase text-muted">Workspace</p>
          <AdminNavigation />
          <div className="mt-4 border-t border-line pt-3">
            <Link to="/" className="flex min-h-11 items-center gap-3 rounded-lg px-3 text-sm font-medium text-muted hover:bg-bg hover:text-ink"><ArrowLeft size={18} aria-hidden="true" />Public site</Link>
          </div>
        </aside>
        <main className="min-w-0 w-full flex-1"><Outlet /></main>
      </div>

      <footer className="border-t border-line bg-surface px-4 py-4 text-center text-xs text-muted">CodeCache administration</footer>

      {menuOpen && <div className="fixed inset-0 z-50 bg-black/40 xl:hidden" onClick={() => setMenuOpen(false)}>
        <aside aria-label="Admin menu" className="h-full w-[min(20rem,88vw)] overflow-y-auto border-r border-line bg-surface p-4 shadow-xl" onClick={event => event.stopPropagation()}>
          <div className="mb-6 flex items-center justify-between">
            <Link to="/admin/dashboard" onClick={() => setMenuOpen(false)} aria-label="Admin overview"><Logo sub={null} /></Link>
            <button type="button" className="btn-icon" onClick={() => setMenuOpen(false)} aria-label="Close admin navigation"><X size={19} /></button>
          </div>
          <p className="mb-3 px-3 text-xs font-semibold uppercase text-muted">Workspace</p>
          <AdminNavigation onSelect={() => setMenuOpen(false)} />
          <div className="mt-4 border-t border-line pt-3">
            <Link to="/" onClick={() => setMenuOpen(false)} className="flex min-h-11 items-center gap-3 rounded-lg px-3 text-sm font-medium text-muted hover:bg-bg hover:text-ink"><ArrowLeft size={18} aria-hidden="true" />Public site</Link>
          </div>
          <div className="mt-4 flex items-center gap-2 px-3 text-xs text-muted"><BarChart3 size={15} aria-hidden="true" />{user?.email}</div>
        </aside>
      </div>}
    </div>
  );
}
