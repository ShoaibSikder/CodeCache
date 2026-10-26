import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { authAPI, tokens } from '../services/api.js';

const Ctx = createContext(null);
export const useAuth = () => useContext(Ctx);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    if (!tokens.access) { setReady(true); return; }
    authAPI.profile().then(setUser).catch(() => tokens.clear()).finally(() => setReady(true));
  }, []);

  const finish = useCallback((res) => { tokens.set(res); setUser(res.user); return res.user; }, []);
  const value = useMemo(() => ({
    user, ready, setUser,
    isAdmin: ['admin', 'super_admin'].includes(user?.role),
    login: (p) => authAPI.login(p).then(finish),
    register: (p) => authAPI.register(p).then(finish),
    logout: async () => { await authAPI.logout(); tokens.clear(); setUser(null); },
  }), [user, ready, finish]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}
