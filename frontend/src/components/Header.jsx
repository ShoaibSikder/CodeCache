import { useState, useContext, useEffect, useRef } from "react";
import { searchAPI, analyticsAPI } from "../services/api";
import { Link, useNavigate } from "react-router-dom";
import {
  Search,
  Moon,
  Sun,
  Code2,
  Menu,
  X,
  LogOut,
  Shield,
  User,
  LogIn,
  Route,
  Bookmark,
  ChevronDown,
} from "lucide-react";
import { Input } from "./ui/input";
import { AuthContext } from "../App";
import { toast } from "sonner";
import { getLanguageColor } from "../lib/languageMeta";

const getLangSlug = (item) => {
  // Try URL first: /language/javascript -> javascript
  const urlMatch = (item.url || "").match(/^\/language\/([^/#?]+)/);
  if (urlMatch) return urlMatch[1];

  // Try nested language object from backend search response
  const raw = item.raw || item;
  if (raw?.language?.slug) return raw.language.slug;

  // Try direct slug field (language results)
  if (raw?.slug) return raw.slug;

  return "";
};

export default function Header() {
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window === "undefined") return true;
    return localStorage.getItem("darkMode") !== "false";
  });
  const [searchQuery, setSearchQuery] = useState("");
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [paletteResults, setPaletteResults] = useState([]);
  const [paletteLoading, setPaletteLoading] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const searchWrapperRef = useRef(null);
  const profileRef = useRef(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [mobileSearchOpen, setMobileSearchOpen] = useState(false);
  const [profileOpen, setProfileOpen] = useState(false);
  const { user, setUser, isAdmin } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
  }, [darkMode]);

  const toggleDarkMode = (checked) => {
    setDarkMode(checked);
    document.documentElement.classList.toggle("dark", checked);
    localStorage.setItem("darkMode", checked);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      const query = searchQuery.trim();
      navigate(`/search?q=${encodeURIComponent(query)}`);
      setSearchQuery("");
      setMobileSearchOpen(false);
      setPaletteOpen(false);
    }
  };

  const normalizeURL = (url) => {
    if (!url) return url;
    // Ensure URL starts with /
    let normalized = url.startsWith("/") ? url : `/${url}`;
    // Replace /languages/ with /language/
    normalized = normalized.replace(/^\/languages\//, "/language/");
    return normalized;
  };

  const normalizePaletteItems = (items) => {
    if (!Array.isArray(items)) return [];

    return items.map((item) => {
      if (item && item.type && item.text) {
        return {
          type: item.type,
          title: item.text,
          subtitle: item.subtitle || item.description || "",
          url: normalizeURL(
            item.url || `/search?q=${encodeURIComponent(item.text)}`,
          ),
          raw: item,
        };
      }

      const title =
        item.title || item.name || item.heading || item.text || "Result";
      const subtitle =
        item.description || item.excerpt || item.snippet || item.summary || "";
      const url = normalizeURL(item.url || `/search?q=${encodeURIComponent(title)}`);

      return {
        type: item.type || "result",
        title,
        subtitle,
        url,
        raw: item,
      };
    });
  };

  const navigateToPaletteItem = async (item) => {
    if (!item?.url) return;
    analyticsAPI
      .trackView({
        path: item.url,
        referrer: window.location.pathname,
      })
      .catch(() => {});
    navigate(item.url);
    setPaletteOpen(false);
  };

  const handleInputKeyDown = (e) => {
    if (!paletteOpen || paletteResults.length === 0) return;

    if (e.key === "ArrowDown") {
      e.preventDefault();
      setHighlightedIndex((current) =>
        Math.min(current + 1, paletteResults.length - 1),
      );
    }

    if (e.key === "ArrowUp") {
      e.preventDefault();
      setHighlightedIndex((current) => Math.max(current - 1, 0));
    }

    if (e.key === "Enter") {
      if (highlightedIndex >= 0 && highlightedIndex < paletteResults.length) {
        e.preventDefault();
        navigateToPaletteItem(paletteResults[highlightedIndex]);
      }
    }

    if (e.key === "Escape") {
      setPaletteOpen(false);
    }
  };

  // Debounced suggestions / quick search for palette
  useEffect(() => {
    if (!searchQuery || searchQuery.trim().length < 1) {
      setPaletteResults([]);
      setPaletteLoading(false);
      setHighlightedIndex(-1);
      return;
    }

    let cancelled = false;
    const t = setTimeout(async () => {
      try {
        setPaletteLoading(true);
        const res = await searchAPI
          .suggestions(searchQuery.trim())
          .catch(() => null);
        let items = res?.data?.data ?? res?.data ?? null;

        if (!Array.isArray(items) || items.length === 0) {
          const full = await searchAPI.search(searchQuery.trim());
          items = full?.data?.results ?? full?.data?.data ?? full?.data ?? [];
        }

        if (!Array.isArray(items)) {
          if (items && typeof items === "object") {
            items = items.results ?? items.items ?? [];
          } else {
            items = [];
          }
        }

        const normalized = normalizePaletteItems(items).slice(0, 8);
        if (!cancelled) {
          setPaletteResults(normalized);
          setHighlightedIndex(normalized.length ? 0 : -1);
          setPaletteOpen(normalized.length > 0);
          analyticsAPI
            .trackSearch({
              query: searchQuery.trim(),
              results_count: normalized.length,
              source: "palette",
            })
            .catch(() => {});
        }
      } catch (err) {
        console.error("Palette search error:", err);
        if (!cancelled) setPaletteResults([]);
      } finally {
        if (!cancelled) setPaletteLoading(false);
      }
    }, 220);

    return () => {
      cancelled = true;
      clearTimeout(t);
    };
  }, [searchQuery]);

  // Close when clicking outside
  useEffect(() => {
    function onDoc(e) {
      if (
        searchWrapperRef.current &&
        !searchWrapperRef.current.contains(e.target)
      ) {
        setPaletteOpen(false);
      }
      if (profileRef.current && !profileRef.current.contains(e.target)) {
        setProfileOpen(false);
      }
    }
    document.addEventListener("click", onDoc);
    return () => document.removeEventListener("click", onDoc);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setUser(null);
    setProfileOpen(false);
    toast.success("Logged out successfully");
    navigate("/");
  };


  return (
    <header className="sticky top-0 z-50 bg-background/80 backdrop-blur-xl border-b border-border">
      <div className="w-full max-w-[1800px] mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14 md:h-16 gap-3">
          {/* Logo */}
          <Link
            to="/"
            className="flex-shrink-0 flex items-center gap-2.5 group"
          >
            <div className="brand-mark w-9 h-9 bg-primary rounded-lg flex items-center justify-center shadow-sm transition-transform">
              <Code2 className="h-4.5 w-4.5 text-primary-foreground" />
            </div>
            <div className="hidden sm:block">
              <div className="text-base font-bold leading-tight tracking-tight">
                <span>Code</span>
                <span className="text-primary dark:text-red-400">Cache</span>
              </div>
              <div className="text-[10px] text-ink-faint leading-none font-medium">
                Recall Code Faster
              </div>
            </div>
          </Link>

          {/* Desktop Search */}
          <form
            onSubmit={handleSearch}
            className="hidden md:flex flex-1 max-w-xl mx-4"
          >
            <div ref={searchWrapperRef} className="relative w-full">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-ink-faint" />
              <Input
                type="text"
                placeholder="Search snippets..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={handleInputKeyDown}
                onFocus={() => setPaletteOpen(paletteResults.length > 0)}
                className="w-full pl-9 pr-4 rounded-md"
              />

              {/* Search Palette */}
              {paletteOpen && (
                <div className="absolute left-0 right-0 mt-2 bg-popover border-[3px] border-border rounded-lg shadow-lg z-50 max-h-80 overflow-auto">
                  {paletteLoading ? (
                    <div className="p-3 text-sm text-ink-faint">Searching…</div>
                  ) : paletteResults.length === 0 ? (
                    <div className="p-3 text-sm text-ink-faint">No results</div>
                  ) : (
                    <div className="divide-y divide-border">
                      {paletteResults.map((r, index) => {
                        const langSlug = getLangSlug(r);
                        const paletteColor = langSlug
                          ? getLanguageColor(langSlug)
                          : null;

                        return (
                          <Link
                            key={`${r.type}-${r.title}-${index}`}
                            to={r.url}
                            className={`block transition-colors overflow-hidden ${
                              index === highlightedIndex
                                ? "bg-muted/80"
                                : "hover:bg-muted/80"
                            }`}
                            onClick={() => {
                              setPaletteOpen(false);
                              analyticsAPI
                                .trackView({
                                  path: r.url,
                                  referrer: window.location.pathname,
                                })
                                .catch(() => {});
                            }}
                            onMouseEnter={() => setHighlightedIndex(index)}
                          >
                            {paletteColor && (
                              <div
                                className="language-accent-bar h-0.5 w-full"
                                style={{ "--language-accent": paletteColor }}
                              />
                            )}
                            <div className="px-3 py-2">
                              <div className="flex items-center justify-between gap-3">
                                <div className="text-sm font-medium text-ink">
                                  {r.title}
                                </div>
                                <div className="text-xs text-ink-faint">
                                  {r.type || "search"}
                                </div>
                              </div>
                              {r.subtitle ? (
                                <div className="text-xs text-ink-soft mt-1 line-clamp-2">
                                  {r.subtitle}
                                </div>
                              ) : null}
                            </div>
                          </Link>
                        );
                      })}
                    </div>
                  )}
                </div>
              )}
            </div>
          </form>

          {/* Right Section */}
          <div className="flex items-center gap-2 md:gap-3">
            {/* Mobile Search Toggle */}
            <button
              onClick={() => setMobileSearchOpen(!mobileSearchOpen)}
              className="md:hidden p-2 rounded-lg hover:bg-muted transition-colors"
            >
              {mobileSearchOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Search className="h-5 w-5 text-ink-faint" />
              )}
            </button>

            {/* Theme Toggle */}
            <button
              type="button"
              onClick={() => toggleDarkMode(!darkMode)}
              className="cursor-pointer p-2 rounded-md bg-muted hover:bg-muted transition-all duration-200"
              aria-label={darkMode ? "Switch to light theme" : "Switch to dark theme"}
              aria-pressed={darkMode}
              title={darkMode ? "Switch to light theme" : "Switch to GitHub dark"}
            >
              {darkMode ? (
                <Moon className="h-4 w-4 text-primary" />
              ) : (
                <Sun className="h-4 w-4 text-amber-400" />
              )}
            </button>

            {user ? (
              <div ref={profileRef} className="relative">
                <button
                  type="button"
                  onClick={() => setProfileOpen((open) => !open)}
                  className="flex items-center gap-1.5 rounded-md bg-muted px-2.5 py-2 transition-colors hover:bg-muted/80"
                  title="Profile menu"
                >
                  <User className="h-4 w-4" />
                  <span className="hidden md:inline max-w-28 truncate text-sm font-bold">
                    {user.username}
                  </span>
                  <ChevronDown className="h-3.5 w-3.5" />
                </button>
                {profileOpen ? (
                  <div className="absolute right-0 mt-2 w-56 rounded-lg border-[3px] border-border bg-popover p-2 shadow-lg z-50">
                    <Link
                      to="/learning-path"
                      onClick={() => setProfileOpen(false)}
                      className="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-bold hover:bg-muted"
                    >
                      <Route className="h-4 w-4" />
                      Learning Path
                    </Link>
                    <Link
                      to="/saved"
                      onClick={() => setProfileOpen(false)}
                      className="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-bold hover:bg-muted"
                    >
                      <Bookmark className="h-4 w-4" />
                      Saved Items
                    </Link>
                    {isAdmin ? (
                      <Link
                        to="/admin"
                        onClick={() => setProfileOpen(false)}
                        className="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-bold hover:bg-muted"
                      >
                        <Shield className="h-4 w-4" />
                        Admin
                      </Link>
                    ) : null}
                    <button
                      onClick={handleLogout}
                      className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-left text-sm font-bold hover:bg-destructive/10 hover:text-destructive"
                    >
                      <LogOut className="h-4 w-4" />
                      Logout
                    </button>
                  </div>
                ) : null}
              </div>
            ) : (
              <Link
                to="/login"
                className="auth-login-button inline-flex items-center gap-1.5 rounded-md bg-muted px-2 py-2 text-sm font-bold transition-all duration-200 hover:bg-muted"
              >
                <LogIn className="h-4 w-4" />
                <span className="hidden sm:inline">Login</span>
              </Link>
            )}

            {/* Admin Link */}
            {false && isAdmin && (
              <Link
                to="/admin"
                className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-muted hover:bg-primary hover:text-primary-foreground transition-colors text-sm font-bold"
              >
                <Shield className="h-3.5 w-3.5" />
                <span className="hidden lg:inline">Admin</span>
              </Link>
            )}

            {/* User / Auth — only shown when logged in */}
            {false && user && (
              <div className="flex items-center gap-2">
                <span className="hidden md:flex items-center gap-1.5 text-sm font-medium">
                  <User className="h-4 w-4" />
                  {user.username}
                </span>
                <button
                  onClick={handleLogout}
                className="p-2 rounded-md hover:bg-destructive/10 hover:text-destructive transition-colors"
                  title="Logout"
                >
                  <LogOut className="h-4 w-4" />
                </button>
              </div>
            )}

            {/* Mobile Menu Toggle */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="sm:hidden p-2 rounded-lg hover:bg-muted transition-colors"
            >
              {mobileMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Search */}
        {mobileSearchOpen && (
          <form onSubmit={handleSearch} className="md:hidden pb-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-ink-faint" />
              <Input
                type="text"
                placeholder="Search snippets..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-4 rounded-md"
                autoFocus
              />
            </div>
          </form>
        )}

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="sm:hidden py-3 border-t space-y-2">
            {isAdmin && (
              <Link
                to="/admin"
                onClick={() => setMobileMenuOpen(false)}
                className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-muted transition-colors"
              >
                <Shield className="h-4 w-4" />
                <span className="text-sm font-medium">Admin Dashboard</span>
              </Link>
            )}
            {user ? (
              <>
                <div className="flex items-center gap-2 px-3 py-2 text-sm font-medium">
                  <User className="h-4 w-4" />
                  {user.username}
                </div>
                <button
                  onClick={() => {
                    handleLogout();
                    setMobileMenuOpen(false);
                  }}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-destructive/10 hover:text-destructive transition-colors w-full text-left"
                >
                  <LogOut className="h-4 w-4" />
                  <span className="text-sm font-medium">Logout</span>
                </button>
              </>
            ) : null}
          </div>
        )}
      </div>
    </header>
  );
}
