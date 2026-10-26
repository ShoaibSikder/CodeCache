import { lazy, Suspense } from 'react';
import { Routes, Route, Navigate, Outlet, useLocation } from 'react-router-dom';
import Layout from './components/Layout.jsx';
import { PageSkeleton } from './components/Skeleton.jsx';
import { useAuth } from './context/AuthContext.jsx';

const Home = lazy(() => import('./pages/Home.jsx'));
const LanguagePage = lazy(() => import('./pages/LanguagePage.jsx'));
const SearchResults = lazy(() => import('./pages/SearchResults.jsx'));
const Playground = lazy(() => import('./pages/Playground.jsx'));
const SavedItems = lazy(() => import('./pages/SavedItems.jsx'));
const LearningPath = lazy(() => import('./pages/LearningPath.jsx'));
const AuthPage = lazy(() => import('./pages/AuthPage.jsx'));
const Profile = lazy(() => import('./pages/Profile.jsx'));
const AdminDashboard = lazy(() => import('./pages/admin/AdminDashboard.jsx'));
const AdminLogin = lazy(() => import('./pages/admin/AdminLogin.jsx'));
const AdminLayout = lazy(() => import('./pages/admin/AdminLayout.jsx'));
const NotFound = lazy(() => import('./pages/NotFound.jsx'));

// UI guard only. The server is authoritative for permissions (per the project docs).
function Guard({ children, admin = false }) {
  const { user, ready, isAdmin } = useAuth();
  const loc = useLocation();
  if (!ready) return <PageSkeleton />;
  if (!user) return <Navigate to={admin ? '/admin/login' : '/login'} state={{ from: loc.pathname }} replace />;
  if (admin && !isAdmin) return <Navigate to="/" replace />;
  return children || <Outlet />;
}

export default function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin" element={<Guard admin />}>
          <Route element={<AdminLayout />}>
            <Route index element={<Navigate to="dashboard" replace />} />
            <Route path="dashboard" element={<AdminDashboard section="overview" />} />
            <Route path="languages" element={<AdminDashboard section="languages" />} />
            <Route path="sections" element={<AdminDashboard section="structure" />} />
            <Route path="content" element={<AdminDashboard section="content" />} />
            <Route path="users" element={<AdminDashboard section="users" />} />
            <Route path="*" element={<Navigate to="dashboard" replace />} />
          </Route>
        </Route>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/language/:slug" element={<LanguagePage />} />
          <Route path="/search" element={<SearchResults />} />
          <Route path="/playground" element={<Playground />} />
          <Route path="/login" element={<AuthPage mode="login" />} />
          <Route path="/register" element={<AuthPage mode="register" />} />
          <Route path="/saved" element={<Guard><SavedItems /></Guard>} />
          <Route path="/learn" element={<Guard><LearningPath /></Guard>} />
          <Route path="/profile" element={<Guard><Profile /></Guard>} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </Suspense>
  );
}
