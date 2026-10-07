import {
  createBrowserRouter,
  RouterProvider,
  Navigate,
  useParams,
  useLocation,
} from "react-router-dom";
import {
  useState,
  useEffect,
  createContext,
  useContext,
  lazy,
  Suspense,
} from "react";
import Layout from "./components/Layout";
import AdminLayout from "./components/AdminLayout";
import { PageSkeleton } from "./components/LoadingSkeletons";
import { authAPI } from "./services/api";

const Home = lazy(() => import("./pages/Home"));
const LanguagePage = lazy(() => import("./pages/LanguagePage"));
const AdminDashboard = lazy(() => import("./pages/AdminDashboard"));
const AdminLogin = lazy(() => import("./pages/AdminLogin"));
const SearchResults = lazy(() => import("./pages/SearchResults"));
const SavedItems = lazy(() => import("./pages/SavedItems"));
const LearningPath = lazy(() => import("./pages/LearningPath"));

export const AuthContext = createContext(null);

function AdminLoginWrapper() {
  const { isAdmin, loading } = useContext(AuthContext);
  if (loading) return <PageSkeleton />;
  if (!loading && isAdmin) return <Navigate to="/admin" replace />;
  return <AdminLogin adminOnly />;
}

function LoginWrapper() {
  const { user, loading } = useContext(AuthContext);
  const location = useLocation();
  if (loading) return <PageSkeleton />;
  if (!loading && user) {
    const next = location.state?.from || "/";
    return <Navigate to={next} replace />;
  }
  return <AdminLogin />;
}

function AdminDashboardWrapper() {
  const { isAdmin, loading } = useContext(AuthContext);
  if (loading) return <PageSkeleton />;
  if (!loading && !isAdmin) return <Navigate to="/admin/login" replace />;
  return <AdminDashboard />;
}

function LearningPathWrapper() {
  const { user, loading } = useContext(AuthContext);
  const location = useLocation();
  if (loading) return <PageSkeleton />;
  if (!user) return <Navigate to="/login" state={{ from: location.pathname }} replace />;
  return <LearningPath />;
}

// Redirect helper to normalize /languages/ -> /language/
function PluralRedirect() {
  const { slug } = useParams();
  const { hash } = useLocation();
  return <Navigate to={`/language/${slug}${hash || ""}`} replace />;
}

// Created once outside the component to prevent router recreation on every render
const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { index: true, element: <RouteChunk><Home /></RouteChunk> },
      { path: "language/:slug", element: <RouteChunk><LanguagePage /></RouteChunk> },
      { path: "languages/:slug", element: <PluralRedirect /> },
      { path: "languages/:slug/*", element: <PluralRedirect /> },
      { path: "search", element: <RouteChunk><SearchResults /></RouteChunk> },
      { path: "saved", element: <RouteChunk><SavedItems /></RouteChunk> },
      { path: "learning-path", element: <RouteChunk><LearningPathWrapper /></RouteChunk> },
    ],
  },
  { path: "/login", element: <RouteChunk><LoginWrapper /></RouteChunk> },
  { path: "/admin/login", element: <RouteChunk><AdminLoginWrapper /></RouteChunk> },
  {
    path: "/admin",
    element: <AdminLayout />,
    children: [
      { index: true, element: <RouteChunk><AdminDashboardWrapper /></RouteChunk> },
      { path: "*", element: <RouteChunk><AdminDashboardWrapper /></RouteChunk> },
    ],
  },
]);

function RouteChunk({ children }) {
  return <Suspense fallback={<PageSkeleton />}>{children}</Suspense>;
}

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      authAPI
        .profile()
        .then((res) => {
          setUser(res.data.data);
        })
        .catch(() => {
          localStorage.removeItem("accessToken");
          localStorage.removeItem("refreshToken");
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const isAdmin = user?.role === "admin" || user?.role === "super_admin";

  return (
    <AuthContext.Provider value={{ user, setUser, isAdmin, loading }}>
      <RouterProvider
        router={router}
        future={{ v7_startTransition: true, v7_relativeSplatPath: true }}
      />
    </AuthContext.Provider>
  );
}

export default App;
