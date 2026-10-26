import { useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext.jsx';
import { setPageTitle } from '../lib/site.js';

export default function Profile() {
  const { user, logout, isAdmin } = useAuth(); const nav = useNavigate();
  useEffect(() => { setPageTitle('Profile'); }, []);
  return (
    <div className="mx-auto max-w-xl px-4 py-10 sm:px-6">
      <h1 className="text-3xl font-bold">Profile</h1>
      <dl className="card mt-6 divide-y divide-line">{[['Username', user.username], ['Email', user.email], ['Role', user.role]].map(([k, v]) => <div key={k} className="flex justify-between gap-4 p-4 text-sm"><dt className="text-muted">{k}</dt><dd className="min-w-0 break-words font-medium">{v}</dd></div>)}</dl>
      <div className="mt-6 flex flex-wrap gap-3">
        {isAdmin && <Link to="/admin" className="btn-ghost">Admin dashboard</Link>}
        <button className="btn-ghost" onClick={async () => { await logout(); nav('/'); }}><LogOut size={16} aria-hidden="true" />Sign out</button>
      </div>
    </div>
  );
}
