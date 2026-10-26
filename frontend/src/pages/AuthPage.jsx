import { useEffect, useState } from 'react';
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { useAuth } from '../context/AuthContext.jsx';
import { errorMessage } from '../services/api.js';
import { setPageTitle } from '../lib/site.js';

function Field({ id, label, hint, error, ...p }) {
  return (
    <div><label htmlFor={id} className="mb-1 block text-sm font-medium">{label}</label>
      <input id={id} className="input" aria-invalid={!!error} aria-describedby={`${id}-d`} {...p} />
      <p id={`${id}-d`} className={`mt-1 text-xs ${error ? 'text-danger' : 'text-muted'}`}>{error || hint}</p></div>
  );
}

export default function AuthPage({ mode }) {
  const reg = mode === 'register';
  const { user, login, register } = useAuth(); const nav = useNavigate(); const loc = useLocation();
  useEffect(() => { setPageTitle(reg ? 'Register' : 'Sign in'); }, [reg]);
  const [f, setF] = useState({ username: '', email: '', password: '', password2: '' }); const [errs, setErrs] = useState({}); const [busy, setBusy] = useState(false); const [formErr, setFormErr] = useState('');
  const set = (k) => (e) => setF(v => ({ ...v, [k]: e.target.value }));
  if (user) return <Navigate to={loc.state?.from || '/'} replace />;

  const submit = async (e) => {
    e.preventDefault(); setFormErr('');
    const er = {};
    if (reg && f.username.trim().length < 3) er.username = 'Use at least 3 characters.';
    if (!/^\S+@\S+\.\S+$/.test(f.email)) er.email = 'Enter a valid email, like you@example.com.';
    if (f.password.length < 8) er.password = 'Use at least 8 characters.';
    if (reg && f.password !== f.password2) er.password2 = 'Passwords do not match.';
    setErrs(er); if (Object.keys(er).length) return;
    setBusy(true);
    try { await (reg ? register(f) : login(f)); toast.success(reg ? 'Account created. Welcome!' : 'Signed in'); nav(loc.state?.from || '/', { replace: true }); }
    catch (x) { setFormErr(errorMessage(x)); } finally { setBusy(false); }
  };

  return (
    <div className="mx-auto max-w-md px-4 py-14">
      <h1 className="text-3xl font-bold">{reg ? 'Create your account' : 'Welcome back'}</h1>
      <p className="mt-1 text-muted">{reg ? 'Free. Takes a minute.' : 'Sign in to continue.'}</p>
      <form onSubmit={submit} noValidate className="card mt-6 space-y-4 p-6">
        {formErr && <p role="alert" className="rounded-lg border border-danger/40 bg-danger/5 p-3 text-sm text-danger">{formErr}</p>}
        {reg && <Field id="username" label="Username" value={f.username} onChange={set('username')} error={errs.username} autoComplete="username" />}
        <Field id="email" type="email" label="Email" value={f.email} onChange={set('email')} error={errs.email} autoComplete="email" />
        <Field id="password" type="password" label="Password" value={f.password} onChange={set('password')} error={errs.password} autoComplete={reg ? 'new-password' : 'current-password'} hint={reg ? 'At least 8 characters.' : ''} />
        {reg && <Field id="password2" type="password" label="Confirm password" value={f.password2} onChange={set('password2')} error={errs.password2} autoComplete="new-password" />}
        <button className="btn-primary w-full" disabled={busy}>{busy ? 'Please wait…' : reg ? 'Create account' : 'Sign in'}</button>
      </form>
      <p className="mt-4 text-center text-sm text-muted">{reg ? 'Already have an account?' : 'New to CodeCache?'} <Link className="font-semibold text-brand underline" to={reg ? '/login' : '/register'}>{reg ? 'Sign in' : 'Create an account'}</Link></p>
    </div>
  );
}
