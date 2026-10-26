import { useEffect, useState } from 'react';
import { ArrowLeft, LockKeyhole, ShieldCheck } from 'lucide-react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.jsx';
import { errorMessage } from '../../services/api.js';
import Logo from '../../components/Logo.jsx';
import { setPageTitle } from '../../lib/site.js';

export default function AdminLogin() {
  useEffect(() => { setPageTitle('Admin sign in'); }, []);
  const { user, ready, isAdmin, login, logout } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  if (!ready) return <div className="grid min-h-screen place-items-center text-sm text-muted">Checking your session...</div>;
  if (user && isAdmin) return <Navigate to="/admin/dashboard" replace />;

  async function submit(event) {
    event.preventDefault();
    setError('');
    setBusy(true);
    try {
      const account = await login({ email: email.trim(), password });
      if (!['admin', 'super_admin'].includes(account?.role)) {
        await logout();
        setError('This account does not have administrator access.');
        return;
      }
      navigate('/admin/dashboard', { replace: true });
    } catch (err) {
      setError(errorMessage(err, 'Sign in failed. Check your credentials and try again.'));
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="grid min-h-screen place-items-center bg-bg px-4 py-10 text-ink">
      <div className="w-full max-w-md">
        <Link to="/" className="mb-8 inline-flex items-center gap-2 text-sm font-medium text-muted transition-colors hover:text-brand">
          <ArrowLeft size={16} aria-hidden="true" /> Public site
        </Link>
        <section className="card p-6 sm:p-8">
          <Logo sub="Administrator access" />
          <div className="mt-8 flex items-center gap-3">
            <span className="grid h-11 w-11 shrink-0 place-items-center rounded-lg bg-brand/10 text-brand"><ShieldCheck size={22} aria-hidden="true" /></span>
            <div><h1 className="text-xl font-bold">Admin sign in</h1><p className="text-sm text-muted">Use an administrator account to continue.</p></div>
          </div>
          <form onSubmit={submit} className="mt-6 space-y-4">
            {error && <p role="alert" className="rounded-lg border border-danger/30 bg-danger/5 p-3 text-sm text-danger">{error}</p>}
            <div><label htmlFor="admin-email" className="mb-1 block text-sm font-medium">Email</label><input id="admin-email" className="input" type="email" autoComplete="username" required value={email} onChange={event => setEmail(event.target.value)} /></div>
            <div><label htmlFor="admin-password" className="mb-1 block text-sm font-medium">Password</label><input id="admin-password" className="input" type="password" autoComplete="current-password" required value={password} onChange={event => setPassword(event.target.value)} /></div>
            <button className="btn-primary w-full" disabled={busy}><LockKeyhole size={16} aria-hidden="true" />{busy ? 'Signing in...' : 'Sign in to admin'}</button>
          </form>
        </section>
      </div>
    </main>
  );
}
