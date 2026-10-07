import { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Shield,
  Users,
  BookOpen,
  Activity,
  BarChart3,
  Plus,
  Pencil,
  Trash2,
  Loader2,
  X,
  TrendingUp,
  Eye,
  Layers,
  ListTree,
  ChevronDown,
  ChevronRight,
  FileCode,
  FileText,
  LogOut,
} from "lucide-react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { Skeleton } from "../components/ui/skeleton";
import { AdminDashboardSkeleton } from "../components/LoadingSkeletons";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "../components/ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../components/ui/table";
import { AuthContext } from "../App";
import { adminAPI, languagesAPI } from "../services/api";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";
import { getLanguageColor } from "../lib/languageMeta";
import { contentTypes, emptyForm } from "./admin/adminConfig";
import { ActionBtns, StatusBadge } from "./admin/AdminDashboardParts";

const adminLoadKeys = [
  "languages",
  "sections",
  "subsections",
  "contentItems",
  "users",
  "analytics",
];

const createLoadState = (value) =>
  adminLoadKeys.reduce((state, key) => ({ ...state, [key]: value }), {});

export default function AdminDashboard() {
  const { user, setUser, isAdmin } = useContext(AuthContext);
  const navigate = useNavigate();
  const [languages, setLanguages] = useState([]);
  const [sections, setSections] = useState([]);
  const [subsections, setSubsections] = useState([]);
  const [contentItems, setContentItems] = useState([]);
  const [users, setUsers] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [stats, setStats] = useState({
    totalLanguages: 0,
    totalSections: 0,
    totalSubsections: 0,
    totalContent: 0,
    todayViews: 0,
  });
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [loadState, setLoadState] = useState(() => createLoadState(false));
  const [activeTab, setActiveTab] = useState("overview");

  // Expanded languages/sections
  const [expandedLangs, setExpandedLangs] = useState({});
  const [expandedSections, setExpandedSections] = useState({});

  // Form state
  const [showForm, setShowForm] = useState(false);
  const [formType, setFormType] = useState("language");
  const [editingItem, setEditingItem] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);
  const [deletingKey, setDeletingKey] = useState("");

  useEffect(() => {
    if (!isAdmin) {
      toast.error("Access denied. Admin only.");
      navigate("/admin/login", { replace: true });
      return;
    }
    fetchAll();
  }, [isAdmin]);

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setUser(null);
    toast.success("Logged out successfully");
    navigate("/admin/login", { replace: true });
  };

  const setDatasetLoading = (key, value) => {
    setLoadState((current) => ({ ...current, [key]: value }));
  };

  const loadDataset = async (key, request, applyData) => {
    setDatasetLoading(key, true);
    try {
      const response = await request();
      applyData(response.data.data || []);
    } catch (error) {
      console.error(`${key} error:`, error);
      toast.error(`Failed to load ${key.replace(/([A-Z])/g, " $1")}`);
    } finally {
      setDatasetLoading(key, false);
    }
  };

  const fetchAll = async ({ showShell = true } = {}) => {
    if (showShell) {
      setLoading(true);
    } else {
      setRefreshing(true);
    }
    setLoadState(createLoadState(true));

    try {
      const langRes = await languagesAPI.list();
      setLanguages(langRes.data.data || []);
    } catch (error) {
      console.error("Languages error:", error);
      toast.error("Failed to load languages");
    } finally {
      setDatasetLoading("languages", false);
      setLoading(false);
    }

    await Promise.allSettled([
      loadDataset("sections", adminAPI.sections.list, setSections),
      loadDataset("subsections", adminAPI.subsections.list, setSubsections),
      loadDataset("contentItems", adminAPI.contentItems.list, setContentItems),
      loadDataset("users", adminAPI.users, setUsers),
      loadDataset("analytics", adminAPI.analytics, setAnalytics),
    ]);

    setRefreshing(false);
  };

  useEffect(() => {
    setStats({
      totalLanguages: languages.length,
      totalSections: sections.length,
      totalSubsections: subsections.length,
      totalContent: contentItems.length,
      todayViews: analytics?.overview?.today_views || 0,
    });
  }, [
    languages.length,
    sections.length,
    subsections.length,
    contentItems.length,
    analytics,
  ]);

  // Data helpers - match on ID (serializer now returns parent FK fields)
  const getSecsForLang = (langId) =>
    sections.filter((s) => {
      const sLangId = s.language; // serializer now returns language FK field
      return String(sLangId) === String(langId);
    });
  const getSubsForSec = (secId) =>
    subsections.filter((s) => {
      const sSecId = s.section; // serializer now returns section FK field
      return String(sSecId) === String(secId);
    });
  const getContentForSub = (subId) =>
    contentItems.filter((ci) => {
      const ciSubId = ci.subsection; // serializer now returns subsection FK field
      return String(ciSubId) === String(subId);
    });

  const toggleExpand = (langId) => {
    setExpandedLangs((prev) => ({ ...prev, [langId]: !prev[langId] }));
  };
  const toggleSectionExpand = (secId) => {
    setExpandedSections((prev) => ({ ...prev, [secId]: !prev[secId] }));
  };

  // ─── Form handlers ───
  const contentTypeFields = {
    heading: { text: form.headingText || "" },
    paragraph: { text: form.paragraphText || "" },
    code: {
      title: form.name || "",
      code: form.codeData || "",
      language: "",
      analogy: "",
      gotcha: "",
    },
    table: {
      columns: (form.tableColumns || "")
        .split(",")
        .map((c) => c.trim())
        .filter(Boolean),
      rows: (form.tableRows || "")
        .split("\n")
        .map((r) =>
          r
            .split(",")
            .map((c) => c.trim())
            .filter(Boolean),
        )
        .filter((r) => r.length > 0),
    },
    note: { text: form.noteText || "" },
    warning: { text: form.warningText || "" },
    tip: { text: form.tipText || "" },
    output: { text: form.outputText || "" },
    divider: {},
    image: { url: form.imageUrl || "", alt: form.imageAlt || "" },
  };

  const openForm = (type, item = null, parentId = "") => {
    setFormType(type);
    setEditingItem(item);
    if (item) {
      const data = item.data || {};
      setForm({
        name: item.name || item.title || data.title || "",
        slug: item.slug || "",
        description: item.description || "",
        display_order: item.display_order || 0,
        status: item.status || "active",
        language: item.language || item.language_id || "",
        section: item.section || item.section_id || "",
        subsection: item.subsection || item.subsection_id || "",
        type: item.type || "code",
        data: data,
        codeData: data.code || "",
        headingText: data.text || "",
        paragraphText: data.text || "",
        noteText: data.text || "",
        warningText: data.text || "",
        tipText: data.text || "",
        outputText: data.text || "",
        tableColumns: (data.columns || []).join(", "),
        tableRows: (data.rows || []).map((r) => r.join(", ")).join("\n"),
        imageUrl: data.url || "",
        imageAlt: data.alt || "",
      });
    } else {
      setForm({
        ...emptyForm,
        language: parentId || "",
        section: parentId || "",
        subsection: "",
      });
    }
    setShowForm(true);
  };

  const closeForm = () => {
    setShowForm(false);
    setEditingItem(null);
  };

  const updateForm = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSave = async () => {
    if (!form.name?.trim() && formType !== "contentitem") {
      toast.error("Name / Title is required");
      return;
    }
    if (!form.slug?.trim() && formType !== "contentitem") {
      toast.error("Slug is required");
      return;
    }
    if (formType === "contentitem" && !form.subsection) {
      toast.error("Subsection is required");
      return;
    }
    if (formType === "contentitem" && !form.type) {
      toast.error("Content type is required");
      return;
    }

    try {
      setSaving(true);
      if (formType === "language") {
        const payload = {
          name: form.name,
          slug: form.slug,
          description: form.description,
          display_order: form.display_order,
          status: form.status,
        };
        if (editingItem) {
          await adminAPI.languages.update(editingItem.id, payload);
        } else {
          await adminAPI.languages.create(payload);
        }
      } else if (formType === "section") {
        const langId = editingItem ? editingItem.language : form.language;
        if (!langId) {
          toast.error("Language is required");
          setSaving(false);
          return;
        }
        const payload = {
          title: form.name,
          slug: form.slug,
          description: form.description,
          display_order: form.display_order,
          status: form.status,
          language: langId,
        };
        if (editingItem) {
          await adminAPI.sections.update(editingItem.id, payload);
        } else {
          await adminAPI.sections.create(payload);
        }
      } else if (formType === "subsection") {
        const secId = editingItem ? editingItem.section : form.section;
        if (!secId) {
          toast.error("Section is required");
          setSaving(false);
          return;
        }
        const payload = {
          title: form.name,
          slug: form.slug,
          description: form.description,
          display_order: form.display_order,
          status: form.status,
          section: secId,
        };
        if (editingItem) {
          await adminAPI.subsections.update(editingItem.id, payload);
        } else {
          await adminAPI.subsections.create(payload);
        }
      } else if (formType === "contentitem") {
        const data = contentTypeFields[form.type] || {};
        const payload = {
          subsection: editingItem ? editingItem.subsection : form.subsection,
          type: form.type,
          data,
          display_order: form.display_order,
          status: form.status,
        };
        if (editingItem) {
          await adminAPI.contentItems.update(editingItem.id, payload);
        } else {
          await adminAPI.contentItems.create(payload);
        }
      }
      toast.success(
        `${formType.charAt(0).toUpperCase() + formType.slice(1)} ${editingItem ? "updated" : "created"}`,
      );
      closeForm();
      await fetchAll({ showShell: false });
    } catch (error) {
      const msg =
        error.response?.data?.error?.message ||
        error.response?.data?.error?.details?.slug?.[0] ||
        "Failed to save";
      toast.error(msg);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (type, id) => {
    if (!confirm(`Delete this ${type}? All child items will also be removed.`))
      return;
    const nextDeletingKey = `${type}:${id}`;
    try {
      setDeletingKey(nextDeletingKey);
      if (type === "language") await adminAPI.languages.delete(id);
      else if (type === "section") await adminAPI.sections.delete(id);
      else if (type === "subsection") await adminAPI.subsections.delete(id);
      else if (type === "contentitem") await adminAPI.contentItems.delete(id);
      toast.success(`${type.charAt(0).toUpperCase() + type.slice(1)} deleted`);
      await fetchAll({ showShell: false });
    } catch (error) {
      toast.error(`Failed to delete ${type}`);
    } finally {
      setDeletingKey("");
    }
  };

  if (!isAdmin) return null;
  if (loading) {
    return <AdminDashboardSkeleton />;
  }

  const contentLabel = (type) => {
    const t = contentTypes.find((c) => c.value === type);
    return t ? t.label : type;
  };

  const contentTreeLoading =
    loadState.languages ||
    loadState.sections ||
    loadState.subsections ||
    loadState.contentItems;

  return (
    <div className="py-6 md:py-8">
      {/* Header */}
      <div className="mb-6 md:mb-8">
        <Link to="/">
          <Button variant="outline" className="mb-4 gap-2">
            <ArrowLeft className="h-4 w-4" /> Back to Home
          </Button>
        </Link>
        <div
          className="bg-card rounded-xl p-6 md:p-8"
          style={{
            border: "2px solid var(--line)",
            boxShadow: "var(--shadow-primary)",
          }}
        >
          <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-2">
            <div className="flex items-center gap-3 min-w-0">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center flex-shrink-0">
              <Shield className="h-5 w-5 text-primary-foreground" />
            </div>
            <div className="min-w-0">
              <h1 className="text-2xl md:text-3xl font-bold">
                Admin Control Panel
              </h1>
              <p className="text-sm text-ink-soft">
                Manage languages, sections, subsections, and all content.
              </p>
            </div>
            </div>
            <Button
              type="button"
              variant="outline"
              onClick={handleLogout}
              className="gap-2 self-start"
            >
              <LogOut className="h-4 w-4" />
              Logout
            </Button>
          </div>
          {user && (
            <div className="flex flex-wrap items-center gap-2 text-xs text-ink-soft mt-2">
              <span>
                Logged in as{" "}
                <span className="font-medium text-foreground">
                  {user.username}
                </span>{" "}
                ({user.role})
              </span>
              {refreshing && (
                <span className="inline-flex items-center gap-1 font-medium text-primary">
                  <Loader2 className="h-3 w-3 animate-spin" />
                  Updating data
                </span>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        {[
          {
            label: "Languages",
            value: stats.totalLanguages,
            loadingKey: "languages",
            icon: BookOpen,
            color: "text-blue-500",
            bg: "bg-blue-500/10",
          },
          {
            label: "Sections",
            value: sections.length,
            loadingKey: "sections",
            icon: Layers,
            color: "text-emerald-500",
            bg: "bg-emerald-500/10",
          },
          {
            label: "Subsections",
            value: subsections.length,
            loadingKey: "subsections",
            icon: ListTree,
            color: "text-cyan-500",
            bg: "bg-cyan-500/10",
          },
          {
            label: "Content Items",
            value: contentItems.length,
            loadingKey: "contentItems",
            icon: BarChart3,
            color: "text-violet-500",
            bg: "bg-violet-500/10",
          },
          {
            label: "Today Views",
            value: analytics?.overview?.today_views || 0,
            loadingKey: "analytics",
            icon: Activity,
            color: "text-orange-500",
            bg: "bg-orange-500/10",
          },
        ].map((stat, i) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="bg-card rounded-xl p-5"
            style={{
              border: "2px solid var(--border-card)",
              boxShadow: "var(--shadow-card)",
            }}
          >
            <div className="flex items-center gap-3">
              <div
                className={`w-10 h-10 rounded-lg ${stat.bg} flex items-center justify-center`}
              >
                <stat.icon className={`h-5 w-5 ${stat.color}`} />
              </div>
              <div>
                {loadState[stat.loadingKey] ? (
                  <Skeleton className="h-7 w-14 mb-1" />
                ) : (
                  <div className="text-2xl font-bold">{stat.value}</div>
                )}
                <div className="text-xs text-ink-soft uppercase tracking-wide">
                  {stat.label}
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList
          className="mb-6 bg-card border flex-wrap"
          style={{ boxShadow: "var(--shadow-primary)" }}
        >
          <TabsTrigger value="overview" className="gap-1.5">
            <BarChart3 className="h-3.5 w-3.5" /> Dashboard
          </TabsTrigger>
          <TabsTrigger value="languages" className="gap-1.5">
            <BookOpen className="h-3.5 w-3.5" /> Content Tree
          </TabsTrigger>
          <TabsTrigger value="users" className="gap-1.5">
            <Users className="h-3.5 w-3.5" /> Users
          </TabsTrigger>
          <TabsTrigger value="analytics" className="gap-1.5">
            <TrendingUp className="h-3.5 w-3.5" /> Analytics
          </TabsTrigger>
        </TabsList>

        {/* Dashboard / Overview */}
        <TabsContent value="overview" className="space-y-6">
          <div
            className="bg-card rounded-xl p-6"
            style={{
              border: "2px solid var(--line)",
              boxShadow: "var(--shadow-primary)",
            }}
          >
            <h3 className="text-lg font-bold mb-4">Quick Actions</h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <button
                onClick={() => {
                  openForm("language");
                  setActiveTab("languages");
                }}
                className="flex items-center gap-3 p-4 rounded-lg bg-muted hover:bg-primary hover:text-primary-foreground transition-all text-left group"
              >
                <Plus className="h-5 w-5 transition-transform" />
                <span className="font-medium text-sm">Add Language</span>
              </button>
              <button
                onClick={() => setActiveTab("languages")}
                className="flex items-center gap-3 p-4 rounded-lg bg-muted hover:bg-primary hover:text-primary-foreground transition-all text-left group"
              >
                <Layers className="h-5 w-5 transition-transform" />
                <span className="font-medium text-sm">Manage Content</span>
              </button>
              <button
                onClick={() => setActiveTab("users")}
                className="flex items-center gap-3 p-4 rounded-lg bg-muted hover:bg-primary hover:text-primary-foreground transition-all text-left group"
              >
                <Users className="h-5 w-5 transition-transform" />
                <span className="font-medium text-sm">View Users</span>
              </button>
              <button
                onClick={() => setActiveTab("analytics")}
                className="flex items-center gap-3 p-4 rounded-lg bg-muted hover:bg-primary hover:text-primary-foreground transition-all text-left group"
              >
                <TrendingUp className="h-5 w-5 transition-transform" />
                <span className="font-medium text-sm">View Analytics</span>
              </button>
            </div>
          </div>

          <div
            className="bg-card rounded-xl p-6"
            style={{
              border: "2px solid var(--line)",
              boxShadow: "var(--shadow-primary)",
            }}
          >
            <h3 className="text-lg font-bold mb-4">Languages Overview</h3>
            <div className="space-y-3">
              {languages.length === 0 && (
                <p className="text-ink-soft text-sm py-4">No languages yet.</p>
              )}
              {languages.slice(0, 10).map((lang) => (
                <div
                  key={lang.id}
                  className="flex items-center justify-between p-3 rounded-lg bg-muted/50"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className="language-accent-bar w-3 h-3 rounded-full"
                      style={{
                        "--language-accent": getLanguageColor(lang.slug),
                      }}
                    />
                    <span className="font-medium text-sm">{lang.name}</span>
                    <span className="text-xs text-ink-soft">
                      ({lang.section_count || getSecsForLang(lang.id).length}{" "}
                      sections)
                    </span>
                  </div>
                  <StatusBadge status={lang.status} />
                </div>
              ))}
            </div>
          </div>

          {analytics && (
            <div
              className="bg-card rounded-xl p-6"
              style={{
                border: "2px solid var(--border-card)",
                boxShadow: "var(--shadow-card)",
              }}
            >
              <h3 className="text-lg font-bold mb-4">
                Traffic Summary (30 days)
              </h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                {[
                  [
                    "Total Views",
                    analytics.overview?.total_month_views || 0,
                    "text-primary",
                  ],
                  [
                    "Unique Visitors",
                    analytics.overview?.unique_visitors_month || 0,
                    "text-emerald-500",
                  ],
                  [
                    "Searches",
                    analytics.overview?.total_month_searches || 0,
                    "text-violet-500",
                  ],
                  [
                    "Active Languages",
                    analytics.language_stats?.length || 0,
                    "text-orange-500",
                  ],
                ].map(([label, val, color]) => (
                  <div
                    key={label}
                    className="text-center p-3 rounded-lg bg-muted/50"
                  >
                    <div className={`text-2xl font-bold ${color}`}>{val}</div>
                    <div className="text-xs text-ink-soft mt-1">{label}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </TabsContent>

        {/* Content Tree — full hierarchy: Language > Section > Subsection > ContentItems */}
        <TabsContent value="languages" className="space-y-6">
          <div
            className="bg-card rounded-xl overflow-hidden"
            style={{
              border: "2px solid var(--border-card)",
              boxShadow: "var(--shadow-card)",
            }}
          >
            <div className="p-4 border-b border-border flex items-center justify-between">
              <h3 className="font-bold">
                Content Tree — Languages → Sections → Subsections → Content
                Items
              </h3>
              <Button
                size="sm"
                onClick={() => openForm("language")}
                className="gap-1"
              >
                <Plus className="h-3.5 w-3.5" /> Add Language
              </Button>
            </div>
            <div className="p-2">
              {contentTreeLoading && languages.length === 0 && (
                <div className="p-2 space-y-2">
                  {Array.from({ length: 6 }).map((_, index) => (
                    <Skeleton key={index} className="h-12 w-full rounded-lg" />
                  ))}
                </div>
              )}
              {contentTreeLoading && languages.length > 0 && (
                <div className="mb-2 flex items-center gap-2 rounded-lg bg-muted/50 px-3 py-2 text-xs font-medium text-ink-soft">
                  <Loader2 className="h-3.5 w-3.5 animate-spin" />
                  Loading content tree chunks
                </div>
              )}
              {!contentTreeLoading && languages.length === 0 && (
                <p className="text-center text-ink-soft py-8">
                  No languages yet. Click "Add Language" to create one.
                </p>
              )}

              {languages.map((lang) => {
                const langSections = getSecsForLang(lang.id);
                const isExpanded = expandedLangs[lang.id];
                return (
                  <div
                    key={lang.id}
                    className="border-b border-border last:border-b-0"
                  >
                    {/* Language row */}
                    <div
                      className="flex items-center justify-between p-3 hover:bg-muted/50 rounded-lg cursor-pointer group"
                      onClick={() => toggleExpand(lang.id)}
                    >
                      <div className="flex items-center gap-3 min-w-0">
                        <div
                          className={`transition-transform ${isExpanded ? "rotate-90" : ""}`}
                        >
                          <ChevronRight className="h-4 w-4 text-ink-faint" />
                        </div>
                        <div
                          className="language-accent-bar w-2.5 h-2.5 rounded-full flex-shrink-0"
                          style={{
                            "--language-accent": getLanguageColor(lang.slug),
                          }}
                        />
                        <span className="font-bold text-sm">{lang.name}</span>
                        <span className="text-xs text-ink-soft">
                          {lang.slug}
                        </span>
                        <StatusBadge status={lang.status} />
                        <span className="text-xs text-ink-soft">
                          {langSections.length} sections
                        </span>
                      </div>
                      <div
                        className="flex items-center gap-1 flex-shrink-0"
                        onClick={(e) => e.stopPropagation()}
                      >
                        <ActionBtns
                          onEdit={() => openForm("language", lang)}
                          onDelete={() => handleDelete("language", lang.id)}
                          deleting={deletingKey === `language:${lang.id}`}
                          disabled={Boolean(deletingKey)}
                        />
                      </div>
                    </div>

                    {/* Expandable sections */}
                    <AnimatePresence>
                      {isExpanded && (
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          className="overflow-hidden"
                        >
                          <div className="ml-8 pl-4 border-l-2 border-border pr-2 pb-2 space-y-1.5">
                            <div className="flex items-center justify-between py-1.5 mb-1">
                              <span className="text-xs font-semibold text-ink-soft uppercase tracking-wide">
                                Sections
                              </span>
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  openForm("section", null, lang.id);
                                }}
                                className="text-xs flex items-center gap-1 px-2 py-1 rounded-md bg-muted hover:bg-primary hover:text-primary-foreground transition-colors"
                              >
                                <Plus className="h-3 w-3" /> Add Section
                              </button>
                            </div>

                            {langSections.length === 0 && (
                              <p className="text-xs text-ink-soft py-2">
                                No sections yet.
                              </p>
                            )}

                            {langSections.map((sec) => {
                              const secSubs = getSubsForSec(sec.id);
                              const secExpanded = expandedSections[sec.id];
                              return (
                                <div
                                  key={sec.id}
                                  className="bg-muted/30 rounded-lg p-2 space-y-1"
                                >
                                  <div className="flex items-center justify-between">
                                    <div
                                      className="flex items-center gap-2 cursor-pointer"
                                      onClick={() =>
                                        toggleSectionExpand(sec.id)
                                      }
                                    >
                                      <div
                                        className={`transition-transform ${secExpanded ? "rotate-90" : ""}`}
                                      >
                                        <ChevronRight className="h-3 w-3 text-ink-faint" />
                                      </div>
                                      <ListTree className="h-3 w-3 text-ink-faint" />
                                      <span className="text-sm font-medium">
                                        {sec.title}
                                      </span>
                                      <span className="text-xs text-ink-soft">
                                        {sec.slug}
                                      </span>
                                      <StatusBadge status={sec.status} />
                                      <span className="text-xs text-ink-soft">
                                        {secSubs.length} subsections
                                      </span>
                                    </div>
                                    <div
                                      className="flex gap-1"
                                      onClick={(e) => e.stopPropagation()}
                                    >
                                      <ActionBtns
                                        onEdit={() => openForm("section", sec)}
                                        onDelete={() =>
                                          handleDelete("section", sec.id)
                                        }
                                        deleting={
                                          deletingKey === `section:${sec.id}`
                                        }
                                        disabled={Boolean(deletingKey)}
                                      />
                                    </div>
                                  </div>

                                  {/* Expandable subsections with content items */}
                                  <AnimatePresence>
                                    {secExpanded && (
                                      <motion.div
                                        initial={{ height: 0, opacity: 0 }}
                                        animate={{ height: "auto", opacity: 1 }}
                                        exit={{ height: 0, opacity: 0 }}
                                        className="overflow-hidden"
                                      >
                                        <div className="ml-4 pl-3 border-l border-border space-y-1">
                                          {secSubs.length === 0 && (
                                            <p className="text-xs text-ink-soft py-2">
                                              No subsections yet.
                                            </p>
                                          )}
                                          {secSubs.map((sub) => {
                                            const subContent = getContentForSub(
                                              sub.id,
                                            );
                                            return (
                                              <div
                                                key={sub.id}
                                                className="py-1.5 space-y-1.5"
                                              >
                                                <div className="flex items-center justify-between bg-background/50 rounded px-2 py-1">
                                                  <div className="flex items-center gap-2 min-w-0">
                                                    <FileText className="h-3 w-3 text-ink-faint/50 flex-shrink-0" />
                                                    <span className="text-xs font-medium">
                                                      {sub.title}
                                                    </span>
                                                    <span className="text-[10px] text-ink-faint">
                                                      {sub.slug}
                                                    </span>
                                                    <StatusBadge
                                                      status={sub.status}
                                                    />
                                                    <span className="text-[10px] text-ink-faint">
                                                      {sub.content_count ||
                                                        subContent.length}{" "}
                                                      items
                                                    </span>
                                                  </div>
                                                  <div className="flex gap-1 flex-shrink-0">
                                                    <ActionBtns
                                                      onEdit={() =>
                                                        openForm(
                                                          "subsection",
                                                          sub,
                                                        )
                                                      }
                                                      onDelete={() =>
                                                        handleDelete(
                                                          "subsection",
                                                          sub.id,
                                                        )
                                                      }
                                                      deleting={
                                                        deletingKey ===
                                                        `subsection:${sub.id}`
                                                      }
                                                      disabled={Boolean(
                                                        deletingKey,
                                                      )}
                                                    />
                                                  </div>
                                                </div>

                                                {/* Content Items */}
                                                <div className="ml-4 pl-3 border-l border-border space-y-0.5">
                                                  {subContent.map((ci) => (
                                                    <div
                                                      key={ci.id}
                                                      className="flex items-center justify-between py-0.5 px-1.5 rounded hover:bg-muted/50 text-[11px]"
                                                    >
                                                      <div className="flex items-center gap-2 min-w-0">
                                                        <FileCode className="h-2.5 w-2.5 text-ink-faint/60 flex-shrink-0" />
                                                        <span
                                                          className={`text-[10px] px-1.5 py-0.5 rounded-full font-medium ${
                                                            ci.type === "code"
                                                              ? "bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400"
                                                              : ci.type ===
                                                                  "heading"
                                                                ? "bg-slate-100 text-slate-700 dark:bg-slate-900/30 dark:text-slate-400"
                                                                : ci.type ===
                                                                    "paragraph"
                                                                  ? "bg-gray-100 text-gray-700 dark:bg-gray-900/30 dark:text-gray-400"
                                                                  : ci.type ===
                                                                      "note"
                                                                    ? "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
                                                                    : ci.type ===
                                                                        "warning"
                                                                      ? "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400"
                                                                      : ci.type ===
                                                                          "tip"
                                                                        ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400"
                                                                        : ci.type ===
                                                                            "table"
                                                                          ? "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400"
                                                                          : ci.type ===
                                                                              "output"
                                                                            ? "bg-gray-800 text-gray-300 dark:bg-gray-800 dark:text-gray-300"
                                                                            : ci.type ===
                                                                                "image"
                                                                              ? "bg-pink-100 text-pink-700 dark:bg-pink-900/30 dark:text-pink-400"
                                                                              : "bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400"
                                                          }`}
                                                        >
                                                          {contentLabel(
                                                            ci.type,
                                                          )}
                                                        </span>
                                                        <span className="truncate text-ink-soft">
                                                          {ci.data?.title ||
                                                            ci.data?.text ||
                                                            ci.type}
                                                        </span>
                                                        <StatusBadge
                                                          status={ci.status}
                                                        />
                                                      </div>
                                                      <div className="flex gap-1 flex-shrink-0">
                                                        <button
                                                          onClick={() =>
                                                            openForm(
                                                              "contentitem",
                                                              ci,
                                                            )
                                                          }
                                                          className="p-0.5 rounded hover:bg-muted transition-colors"
                                                          title="Edit"
                                                        >
                                                          <Pencil className="h-2.5 w-2.5" />
                                                        </button>
                                                         <button
                                                          onClick={() =>
                                                            handleDelete(
                                                              "contentitem",
                                                              ci.id,
                                                            )
                                                          }
                                                          disabled={Boolean(
                                                            deletingKey,
                                                          )}
                                                          className="p-0.5 rounded hover:bg-red-100 hover:text-red-600 transition-colors"
                                                          title="Delete"
                                                        >
                                                          {deletingKey ===
                                                          `contentitem:${ci.id}` ? (
                                                            <Loader2 className="h-2.5 w-2.5 animate-spin" />
                                                          ) : (
                                                            <Trash2 className="h-2.5 w-2.5" />
                                                          )}
                                                        </button>
                                                      </div>
                                                    </div>
                                                  ))}
                                                  <button
                                                    onClick={() =>
                                                      openForm(
                                                        "contentitem",
                                                        null,
                                                        sub.id,
                                                      )
                                                    }
                                                    className="text-[10px] flex items-center gap-1 px-2 py-0.5 rounded hover:bg-muted transition-colors w-full text-ink-soft"
                                                  >
                                                    <Plus className="h-2.5 w-2.5" />{" "}
                                                    Add Content Item
                                                  </button>
                                                </div>
                                              </div>
                                            );
                                          })}
                                        </div>
                                      </motion.div>
                                    )}
                                  </AnimatePresence>

                                  <button
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      openForm("subsection", null, sec.id);
                                    }}
                                    className="text-xs flex items-center gap-1 px-2 py-1 rounded hover:bg-muted transition-colors w-full text-ink-soft"
                                  >
                                    <Plus className="h-3 w-3" /> Add Subsection
                                  </button>
                                </div>
                              );
                            })}
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                );
              })}
            </div>
          </div>
        </TabsContent>

        {/* Users */}
        <TabsContent value="users" className="space-y-6">
          <div
            className="bg-card rounded-xl overflow-hidden"
            style={{
              border: "2px solid var(--border-card)",
              boxShadow: "var(--shadow-card)",
            }}
          >
            <div className="p-4 border-b border-border">
              <h3 className="font-bold">Users</h3>
            </div>
            {loadState.users ? (
              <div className="p-4 space-y-3">
                {Array.from({ length: 5 }).map((_, index) => (
                  <Skeleton key={index} className="h-11 w-full rounded-lg" />
                ))}
              </div>
            ) : users.length > 0 ? (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Username</TableHead>
                      <TableHead>Email</TableHead>
                      <TableHead>Role</TableHead>
                      <TableHead>Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {users.map((u) => (
                      <TableRow key={u.id}>
                        <TableCell className="font-medium">
                          {u.username}
                        </TableCell>
                        <TableCell className="text-ink-soft">
                          {u.email}
                        </TableCell>
                        <TableCell>
                          <span
                            className={`text-xs px-2 py-0.5 rounded-full font-medium ${u.role === "super_admin" ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400" : u.role === "admin" ? "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400" : u.role === "editor" ? "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400" : "bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400"}`}
                          >
                            {u.role}
                          </span>
                        </TableCell>
                        <TableCell>
                          <span
                            className={`text-xs px-2 py-0.5 rounded-full font-medium ${u.is_active ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400" : "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400"}`}
                          >
                            {u.is_active ? "active" : "inactive"}
                          </span>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            ) : (
              <div className="p-8 text-center text-ink-soft">
                <Users className="h-8 w-8 mx-auto mb-2 opacity-50" />
                <p>No users found</p>
              </div>
            )}
          </div>
        </TabsContent>

        {/* Analytics */}
        <TabsContent value="analytics" className="space-y-6">
          {loadState.analytics ? (
            <div className="space-y-6">
              {Array.from({ length: 2 }).map((_, index) => (
                <div
                  key={index}
                  className="bg-card rounded-xl overflow-hidden"
                  style={{
                    border: "2px solid var(--border-card)",
                    boxShadow: "var(--shadow-card)",
                  }}
                >
                  <div className="p-4 border-b border-border">
                    <Skeleton className="h-5 w-48" />
                  </div>
                  <div className="p-4 space-y-3">
                    {Array.from({ length: 4 }).map((_, rowIndex) => (
                      <Skeleton
                        key={rowIndex}
                        className="h-10 w-full rounded-lg"
                      />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ) : analytics ? (
            <>
              <div
                className="bg-card rounded-xl overflow-hidden"
                style={{
                  border: "2px solid var(--border-card)",
                  boxShadow: "var(--shadow-card)",
                }}
              >
                <div className="p-4 border-b border-border">
                  <h3 className="font-bold">Per-Language Visitors (30 days)</h3>
                </div>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Language</TableHead>
                        <TableHead>Slug</TableHead>
                        <TableHead>Views</TableHead>
                        <TableHead>Unique</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {(analytics.language_stats || []).map((lang) => (
                        <TableRow key={lang.language__slug}>
                          <TableCell className="font-medium">
                            <div className="flex items-center gap-2">
                              <div
                                className="language-accent-bar w-2.5 h-2.5 rounded-full"
                                style={{
                                  "--language-accent": getLanguageColor(
                                    lang.language__slug,
                                  ),
                                }}
                              />
                              {lang.language__name}
                            </div>
                          </TableCell>
                          <TableCell className="text-ink-soft">
                            {lang.language__slug}
                          </TableCell>
                          <TableCell>{lang.view_count}</TableCell>
                          <TableCell>{lang.unique_visitors}</TableCell>
                        </TableRow>
                      ))}
                      {(!analytics.language_stats ||
                        analytics.language_stats.length === 0) && (
                        <TableRow>
                          <TableCell colSpan={4} className="text-center py-8">
                            No data yet.
                          </TableCell>
                        </TableRow>
                      )}
                    </TableBody>
                  </Table>
                </div>
              </div>
              <div
                className="bg-card rounded-xl overflow-hidden"
                style={{
                  border: "2px solid var(--border-card)",
                  boxShadow: "var(--shadow-card)",
                }}
              >
                <div className="p-4 border-b border-border">
                  <h3 className="font-bold">Top Sections (7 days)</h3>
                </div>
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Section</TableHead>
                        <TableHead>Language</TableHead>
                        <TableHead>Views</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {(analytics.top_sections || []).map((sec, idx) => (
                        <TableRow key={idx}>
                          <TableCell className="font-medium">
                            {sec.section__title}
                          </TableCell>
                          <TableCell className="text-ink-soft">
                            {sec.section__language__name}
                          </TableCell>
                          <TableCell>{sec.view_count}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </div>
            </>
          ) : (
            <div
              className="bg-card rounded-xl p-12 text-center"
              style={{
                border: "2px solid var(--border-card)",
                boxShadow: "var(--shadow-card)",
              }}
            >
              <TrendingUp className="h-12 w-12 text-ink-faint mx-auto mb-4 opacity-30" />
              <h3 className="text-lg font-bold mb-2">No Analytics Data Yet</h3>
              <p className="text-sm text-ink-soft">
                Analytics will appear once users start visiting pages.
              </p>
            </div>
          )}
        </TabsContent>
      </Tabs>

      {/* Universal Form Modal */}
      <AnimatePresence>
        {showForm && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 overflow-y-auto"
            onClick={closeForm}
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="bg-card rounded-xl w-full max-w-lg p-6 my-4"
              style={{
                border: "2px solid var(--border-card)",
                boxShadow: "var(--shadow-card-hover)",
              }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold">
                  {editingItem ? "Edit" : "Add"}{" "}
                  {formType === "contentitem"
                    ? "Content Item"
                    : formType.charAt(0).toUpperCase() + formType.slice(1)}
                </h2>
                <button
                  onClick={closeForm}
                  className="p-1 rounded-md hover:bg-muted"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>

              {/* Content Item Form */}
              {formType === "contentitem" && (
                <div className="space-y-4 max-h-[70vh] overflow-y-auto pr-1">
                  {!editingItem && (
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        Subsection *
                      </label>
                      <select
                        value={form.subsection}
                        onChange={(e) =>
                          updateForm("subsection", e.target.value)
                        }
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                      >
                        <option value="">Select subsection...</option>
                        {subsections.map((s) => (
                          <option key={s.id} value={s.id}>
                            {s.title} ({s.section_name})
                          </option>
                        ))}
                      </select>
                    </div>
                  )}
                  <div>
                    <label className="text-xs font-medium text-ink-faint block mb-1">
                      Content Type *
                    </label>
                    <select
                      value={form.type}
                      onChange={(e) => updateForm("type", e.target.value)}
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                    >
                      {contentTypes
                        .filter(
                          (t) =>
                            ![
                              "heading",
                              "paragraph",
                              "note",
                              "warning",
                              "tip",
                              "output",
                            ].includes(t.value) || true,
                        )
                        .map((t) => (
                          <option key={t.value} value={t.value}>
                            {t.label}
                          </option>
                        ))}
                    </select>
                  </div>

                  {/* Dynamic fields based on type */}
                  {["code", "heading"].includes(form.type) && (
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        {form.type === "code" ? "Title" : "Heading Text"}
                      </label>
                      <Input
                        value={form.name}
                        onChange={(e) => updateForm("name", e.target.value)}
                        placeholder={
                          form.type === "code"
                            ? "e.g. Array Map Method"
                            : "e.g. Getting Started"
                        }
                      />
                    </div>
                  )}

                  {form.type === "code" && (
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        Code
                      </label>
                      <Textarea
                        value={form.codeData}
                        onChange={(e) => updateForm("codeData", e.target.value)}
                        placeholder="Paste your code here..."
                        rows={6}
                        className="font-mono text-xs"
                      />
                    </div>
                  )}

                  {["paragraph", "heading"].includes(form.type) && (
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        {form.type === "paragraph"
                          ? "Paragraph Text"
                          : "Heading Text"}
                      </label>
                      <Textarea
                        value={
                          form.type === "paragraph"
                            ? form.paragraphText
                            : form.headingText
                        }
                        onChange={(e) =>
                          updateForm(
                            form.type === "paragraph"
                              ? "paragraphText"
                              : "headingText",
                            e.target.value,
                          )
                        }
                        placeholder="Enter text content..."
                        rows={form.type === "paragraph" ? 3 : 1}
                      />
                    </div>
                  )}

                  {form.type === "note" && (
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        Note Text
                      </label>
                      <Textarea
                        value={form.noteText}
                        onChange={(e) => updateForm("noteText", e.target.value)}
                        placeholder="Informational note..."
                        rows={3}
                      />
                    </div>
                  )}

                  {form.type === "warning" && (
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        Warning Text
                      </label>
                      <Textarea
                        value={form.warningText}
                        onChange={(e) =>
                          updateForm("warningText", e.target.value)
                        }
                        placeholder="Warning message..."
                        rows={3}
                      />
                    </div>
                  )}

                  {form.type === "tip" && (
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        Tip Text
                      </label>
                      <Textarea
                        value={form.tipText}
                        onChange={(e) => updateForm("tipText", e.target.value)}
                        placeholder="Pro tip or best practice..."
                        rows={3}
                      />
                    </div>
                  )}

                  {form.type === "output" && (
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        Output Text
                      </label>
                      <Textarea
                        value={form.outputText}
                        onChange={(e) =>
                          updateForm("outputText", e.target.value)
                        }
                        placeholder="Terminal output / expected result..."
                        rows={4}
                        className="font-mono text-xs"
                      />
                    </div>
                  )}

                  {form.type === "table" && (
                    <>
                      <div>
                        <label className="text-xs font-medium text-ink-faint block mb-1">
                          Columns (comma-separated)
                        </label>
                        <Input
                          value={form.tableColumns}
                          onChange={(e) =>
                            updateForm("tableColumns", e.target.value)
                          }
                          placeholder="Name, Syntax, Example"
                        />
                      </div>
                      <div>
                        <label className="text-xs font-medium text-ink-faint block mb-1">
                          Rows (one per line, comma-separated cells)
                        </label>
                        <Textarea
                          value={form.tableRows}
                          onChange={(e) =>
                            updateForm("tableRows", e.target.value)
                          }
                          placeholder={`var, var x=5, var name="John"`}
                          rows={4}
                        />
                      </div>
                    </>
                  )}

                  {form.type === "image" && (
                    <>
                      <div>
                        <label className="text-xs font-medium text-ink-faint block mb-1">
                          Image URL
                        </label>
                        <Input
                          value={form.imageUrl}
                          onChange={(e) =>
                            updateForm("imageUrl", e.target.value)
                          }
                          placeholder="https://example.com/image.png"
                        />
                      </div>
                      <div>
                        <label className="text-xs font-medium text-ink-faint block mb-1">
                          Alt Text
                        </label>
                        <Input
                          value={form.imageAlt}
                          onChange={(e) =>
                            updateForm("imageAlt", e.target.value)
                          }
                          placeholder="Description of image"
                        />
                      </div>
                    </>
                  )}

                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        Display Order
                      </label>
                      <Input
                        type="number"
                        value={form.display_order}
                        onChange={(e) =>
                          updateForm(
                            "display_order",
                            parseInt(e.target.value) || 0,
                          )
                        }
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        Status
                      </label>
                      <select
                        value={form.status}
                        onChange={(e) => updateForm("status", e.target.value)}
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                      >
                        <option value="active">Active</option>
                        <option value="draft">Draft</option>
                        <option value="inactive">Inactive</option>
                        <option value="archived">Archived</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {/* Language / Section / Subsection Form */}
              {formType !== "contentitem" && (
                <div className="space-y-4">
                  <div>
                    <label className="text-xs font-medium text-ink-faint block mb-1">
                      Name / Title
                    </label>
                    <Input
                      value={form.name}
                      onChange={(e) => updateForm("name", e.target.value)}
                      placeholder="e.g. Variables"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-medium text-ink-faint block mb-1">
                      Slug
                    </label>
                    <Input
                      value={form.slug}
                      onChange={(e) => updateForm("slug", e.target.value)}
                      placeholder="url-friendly-slug"
                    />
                  </div>
                  <div>
                    <label className="text-xs font-medium text-ink-faint block mb-1">
                      Description
                    </label>
                    <Textarea
                      value={form.description}
                      onChange={(e) =>
                        updateForm("description", e.target.value)
                      }
                      placeholder="Brief description..."
                      rows={2}
                    />
                  </div>
                  {formType === "section" && !editingItem && !form.language && (
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        Language
                      </label>
                      <select
                        value={form.language}
                        onChange={(e) => updateForm("language", e.target.value)}
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                      >
                        <option value="">Select language...</option>
                        {languages.map((l) => (
                          <option key={l.id} value={l.id}>
                            {l.name}
                          </option>
                        ))}
                      </select>
                    </div>
                  )}
                  {formType === "subsection" &&
                    !editingItem &&
                    !form.section && (
                      <div>
                        <label className="text-xs font-medium text-ink-faint block mb-1">
                          Section
                        </label>
                        <select
                          value={form.section}
                          onChange={(e) =>
                            updateForm("section", e.target.value)
                          }
                          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                        >
                          <option value="">Select section...</option>
                          {sections.map((s) => (
                            <option key={s.id} value={s.id}>
                              {s.title} ({s.language_name})
                            </option>
                          ))}
                        </select>
                      </div>
                    )}
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        Display Order
                      </label>
                      <Input
                        type="number"
                        value={form.display_order}
                        onChange={(e) =>
                          updateForm(
                            "display_order",
                            parseInt(e.target.value) || 0,
                          )
                        }
                      />
                    </div>
                    <div>
                      <label className="text-xs font-medium text-ink-faint block mb-1">
                        Status
                      </label>
                      <select
                        value={form.status}
                        onChange={(e) => updateForm("status", e.target.value)}
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                      >
                        <option value="active">Active</option>
                        <option value="draft">Draft</option>
                        <option value="inactive">Inactive</option>
                        <option value="archived">Archived</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}

              <div className="flex gap-2 justify-end mt-6">
                <Button variant="outline" onClick={closeForm} disabled={saving}>
                  Cancel
                </Button>
                <Button
                  onClick={handleSave}
                  disabled={saving}
                  className="gap-1.5"
                >
                  {saving ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
                  {editingItem ? "Update" : "Create"}{" "}
                  {formType === "contentitem"
                    ? "Content Item"
                    : formType.charAt(0).toUpperCase() + formType.slice(1)}
                </Button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
