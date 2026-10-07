import { lazy, Suspense, useState, useEffect, useContext } from "react";
import { useParams, Link, useLocation } from "react-router-dom";
import {
  ArrowLeft,
  AlertCircle,
  Info,
  Lightbulb,
  AlertTriangle,
  Terminal,
  Minus,
  BookOpen,
  Stethoscope,
  X,
  Layers,
  Code2,
} from "lucide-react";
import { languagesAPI } from "../services/api";
import { learningAPI } from "../services/api";
import { AuthContext } from "../App";
import { Button } from "../components/ui/button";
import { getLanguageColor } from "../lib/languageMeta";
import TopicIndex from "../components/TopicIndex";
import {
  SnippetCardSkeleton,
  SidebarSkeleton,
  AICodeDoctorSkeleton,
} from "../components/LoadingSkeletons";
import { toast } from "sonner";

const SECTION_BATCH_SIZE = 3;
const CodeSnippetCard = lazy(() => import("../components/CodeSnippetCard"));
const AICodeDoctor = lazy(() => import("../components/AICodeDoctor"));
const QuizSection = lazy(() => import("../components/QuizSection"));
const DailyChallenge = lazy(() => import("../components/DailyChallenge"));
const VisualLearningLab = lazy(() => import("../components/VisualLearningLab"));
const BugFixChallenge = lazy(() => import("../components/BugFixChallenge"));
const SmartNotes = lazy(() => import("../components/SmartNotes"));
const CommunitySolutions = lazy(() => import("../components/CommunitySolutions"));

function ContentRenderer({
  item,
  sectionTitle,
  subsectionTitle,
  languageSlug,
}) {
  const type = item.type;
  const data = item.data || {};

  switch (type) {
    case "heading":
      return (
        <h3 className="text-base font-bold mt-6 mb-2 flex items-center gap-2">
          {data.text || ""}
        </h3>
      );

    case "paragraph":
      return (
        <p className="text-sm text-ink-soft leading-relaxed mb-3">
          {data.text || ""}
        </p>
      );

    case "code":
      return (
        <div className="mb-4">
          <Suspense fallback={<SnippetCardSkeleton />}>
            <CodeSnippetCard
              snippet={{
                id: item.id,
                title: data.title || subsectionTitle,
                category: sectionTitle,
                language: languageSlug,
                code: data.code || "",
                analogy: data.analogy,
                gotcha: data.gotcha,
                data: data,
              }}
            />
          </Suspense>
        </div>
      );

    case "table":
      return (
        <div className="mb-4 overflow-x-auto rounded-lg border">
          <table className="w-full text-sm">
            {data.columns && (
              <thead className="bg-muted">
                <tr>
                  {data.columns.map((col, i) => (
                    <th
                      key={i}
                      className="px-3 py-2 text-left font-semibold text-xs uppercase tracking-wide"
                    >
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
            )}
            <tbody>
              {(data.rows || []).map((row, ri) => (
                <tr key={ri} className="border-t border-border">
                  {row.map((cell, ci) => (
                    <td key={ci} className="px-3 py-2">
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );

    case "note":
      return (
        <div className="mb-4 p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800/50 flex items-start gap-2.5">
          <Info className="h-4 w-4 flex-shrink-0 mt-0.5 text-blue-500" />
          <p className="text-xs text-blue-800 dark:text-blue-200 leading-relaxed">
            {data.text || ""}
          </p>
        </div>
      );

    case "warning":
      return (
        <div className="mb-4 p-3 rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800/50 flex items-start gap-2.5">
          <AlertTriangle className="h-4 w-4 flex-shrink-0 mt-0.5 text-amber-500" />
          <p className="text-xs text-amber-800 dark:text-amber-200 leading-relaxed">
            {data.text || ""}
          </p>
        </div>
      );

    case "tip":
      return (
        <div className="mb-4 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800/50 flex items-start gap-2.5">
          <Lightbulb className="h-4 w-4 flex-shrink-0 mt-0.5 text-emerald-500" />
          <p className="text-xs text-emerald-800 dark:text-emerald-200 leading-relaxed">
            {data.text || ""}
          </p>
        </div>
      );

    case "output":
      return (
        <div className="mb-4 p-3 rounded-lg bg-[#f1f5f9] dark:bg-[#0d1117] border border-border font-mono text-xs text-emerald-700 dark:text-emerald-400 leading-relaxed">
          <div className="flex items-center gap-1.5 mb-1.5 text-ink-faint">
            <Terminal className="h-3 w-3" />
            <span className="text-[10px] uppercase tracking-wide">Output</span>
          </div>
          <pre className="whitespace-pre-wrap">{data.text || ""}</pre>
        </div>
      );

    case "image":
      if (!data.url) return null;
      return (
        <figure className="mb-4 overflow-hidden rounded-lg border border-border bg-card">
          <img
            src={data.url}
            alt={data.alt || ""}
            className="h-auto w-full object-contain"
            loading="lazy"
            decoding="async"
          />
          {data.alt ? (
            <figcaption className="border-t border-border px-3 py-2 text-xs text-ink-faint">
              {data.alt}
            </figcaption>
          ) : null}
        </figure>
      );

    case "divider":
      return (
        <div className="mb-4 flex items-center gap-3">
          <Minus className="h-4 w-4 text-ink-faint/40" />
          <div className="flex-1 border-t border-border" />
        </div>
      );

    default:
      return null;
  }
}

export default function LanguagePage() {
  const { slug } = useParams();
  const { hash } = useLocation();
  const { user } = useContext(AuthContext);
  const [language, setLanguage] = useState(null);
  const [sections, setSections] = useState([]);
  const [visibleSectionCount, setVisibleSectionCount] =
    useState(SECTION_BATCH_SIZE);
  const [loading, setLoading] = useState(true);
  const [activeSection, setActiveSection] = useState(null);
  const [activeSubsection, setActiveSubsection] = useState(null);
  const [mobilePanel, setMobilePanel] = useState(null);

  useEffect(() => {
    if (user) learningAPI.setLastLanguage(slug).catch(() => {});
    fetchLanguageDetail();
    window.scrollTo(0, 0);
  }, [slug, user]);

  const fetchLanguageDetail = async () => {
    try {
      setLoading(true);
      setVisibleSectionCount(SECTION_BATCH_SIZE);
      const response = await languagesAPI.cachedDetail(slug);
      applyLanguageDetail(response.data.data);
      setLoading(false);

      if (response.fromCache) {
        languagesAPI.revalidateDetail(slug, (fresh) => {
          applyLanguageDetail(fresh.data);
        });
      }
    } catch (error) {
      console.error("Failed to fetch language:", error);
      toast.error("Failed to load language data");
      setLoading(false);
    }
  };

  const applyLanguageDetail = (data) => {
    setLanguage(data);
    const nextSections = data?.sections || [];
    setSections(nextSections);
    setVisibleSectionCount(nextSections.length);
  };

  useEffect(() => {
    if (!hash.startsWith("#subsection-") || !sections.length) return;
    const subsectionId = decodeURIComponent(hash.replace("#subsection-", ""));
    window.setTimeout(() => {
      document
        .getElementById(`subsection-${subsectionId}`)
        ?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 0);
  }, [hash, sections]);

  const handleSectionClick = (secId) => {
    setActiveSection(secId);
    setActiveSubsection(null);
    setMobilePanel(null);
    const targetIndex = sections.findIndex(
      (section) => String(section.id) === String(secId),
    );
    if (targetIndex >= visibleSectionCount) {
      setVisibleSectionCount(targetIndex + 1);
    }
    window.setTimeout(() => {
      const element = document.getElementById(`section-${secId}`);
      if (element) {
        element.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }, 0);
  };

  const handleSubsectionClick = (subId) => {
    setActiveSubsection(subId);
    setMobilePanel(null);
    const sectionIndex = sections.findIndex((section) =>
      (section.subsections || []).some(
        (sub) => String(sub.id) === String(subId),
      ),
    );
    if (sectionIndex >= visibleSectionCount) {
      setVisibleSectionCount(sectionIndex + 1);
    }
    window.setTimeout(() => {
      const element = document.getElementById(`subsection-${subId}`);
      if (element) {
        element.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }, 0);
  };

  const color = getLanguageColor(slug);
  const totalItems = sections.reduce(
    (sum, s) =>
      sum +
      (s.subsections || []).reduce(
        (ss, sub) => ss + (sub.content_items || []).length,
        0,
      ),
    0,
  );
  const totalTopics = sections.reduce(
    (sum, section) => sum + (section.subsections || []).length,
    0,
  );

  if (loading) {
    return (
      <div className="py-6 md:py-8">
        <div className="mb-6">
          <div className="h-4 w-32 bg-muted rounded animate-pulse mb-4 no-hover" />
          <div className="h-24 bg-card rounded-xl animate-pulse no-hover" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-3">
            <SidebarSkeleton />
          </div>
          <div className="lg:col-span-6 space-y-5">
            {Array.from({ length: 3 }).map((_, i) => (
              <SnippetCardSkeleton key={i} />
            ))}
          </div>
          <div className="lg:col-span-3">
            <AICodeDoctorSkeleton />
          </div>
        </div>
      </div>
    );
  }

  if (!language) {
    return (
      <div className="py-12 text-center">
        <AlertCircle className="h-12 w-12 text-ink-faint mx-auto mb-4" />
        <h2 className="text-2xl font-bold mb-4">Language Not Found</h2>
        <Link
          to="/"
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Home
        </Link>
      </div>
    );
  }

  return (
    <div className="language-page mx-auto max-w-[1600px] py-6 md:py-8">
      {/* Back + Header */}
      <div className="mb-6 md:mb-8">
        <Link
          to="/"
          className="inline-flex items-center gap-1.5 text-sm text-ink-soft hover:text-primary transition-colors mb-4"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          All languages
        </Link>
        <div
          className="language-head-card bg-card rounded-2xl p-5 md:p-7 no-hover"
          style={{
            border: "2px solid var(--line)",
            boxShadow: "var(--shadow-primary)",
          }}
        >
          <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
            <div className="flex min-w-0 items-center gap-4">
              <div
                className="language-accent-bar h-12 w-1.5 flex-shrink-0 rounded-full md:h-14"
                style={{ "--language-accent": color }}
              />
              <div className="min-w-0">
                <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold tracking-tight text-ink">
                  {language.name}
                </h1>
                {language.description && (
                  <p className="mt-2 max-w-2xl text-sm leading-relaxed text-ink-soft">
                    {language.description}
                  </p>
                )}
              </div>
            </div>
            <dl className="grid grid-cols-3 gap-2 md:min-w-[18rem]">
              {[
                { label: "Sections", value: sections.length, Icon: Layers },
                { label: "Topics", value: totalTopics, Icon: BookOpen },
                { label: "Items", value: totalItems, Icon: Code2 },
              ].map(({ label, value, Icon }) => (
                <div
                  key={label}
                  className="rounded-xl border border-border bg-background/60 px-3 py-3 text-center"
                >
                  <dt className="flex items-center justify-center gap-1.5 text-xs text-ink-faint">
                    <Icon className="h-3.5 w-3.5" />
                    {label}
                  </dt>
                  <dd className="mt-1 text-lg font-semibold text-ink">{value}</dd>
                </div>
              ))}
            </dl>
          </div>
          <p className="mt-5 border-t border-border pt-4 text-sm leading-relaxed text-ink-soft">
            Start with a topic from the index, then explore explanations,
            examples, and practice activities as you go.
          </p>
        </div>
      </div>

      <div className="mb-5 grid grid-cols-2 gap-3 xl:hidden">
        <Button
          type="button"
          variant="outline"
          onClick={() => setMobilePanel("index")}
          className="min-h-11 cursor-pointer justify-center gap-2"
        >
          <BookOpen className="h-4 w-4" />
          Browse topics
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={() => setMobilePanel("doctor")}
          className="min-h-11 cursor-pointer justify-center gap-2"
        >
          <Stethoscope className="h-4 w-4" />
          Ask AI Code Doctor
        </Button>
      </div>

      {/* Main Layout — 3 columns: Index | Content | AI Doctor */}
      <div className="language-workspace grid grid-cols-1 items-start gap-6 xl:grid-cols-[minmax(240px,280px)_minmax(0,1fr)_minmax(260px,300px)]">
        {/* Left Column — Sections Index, sticky */}
        <aside id="topic-index" aria-label="Browse learning topics" className="desktop-side-rail sticky top-20 hidden xl:block">
          <TopicIndex
            sections={sections}
            onSectionClick={handleSectionClick}
            onSubsectionClick={handleSubsectionClick}
            activeSection={activeSection}
            activeSubsection={activeSubsection}
          />
        </aside>

        {/* Middle Column — Main Content */}
        <main aria-label={`${language.name} learning content`} className="language-content-stream min-w-0 space-y-6">
          <div className="flex items-end justify-between gap-4 border-b border-border pb-4">
            <div>
              <h2 className="text-lg font-semibold tracking-tight text-ink">
                Learning guide
              </h2>
              <p className="mt-1 text-sm text-ink-soft">
                Follow the topics in order or jump to anything you need.
              </p>
            </div>
            <span className="shrink-0 rounded-full border border-border bg-card px-3 py-1 text-xs text-ink-faint">
              {sections.length} {sections.length === 1 ? "section" : "sections"}
            </span>
          </div>
          {sections.length > 0 ? (
            sections.slice(0, visibleSectionCount).map((section) => (
              <section key={section.id} id={`section-${section.id}`} className="language-section scroll-mt-24">
                <h2 className="mb-3 flex items-center gap-2 text-xl font-semibold tracking-tight text-ink">
                  <span
                    className="language-accent-bar h-2.5 w-2.5 flex-shrink-0 rounded-full"
                    style={{ "--language-accent": color }}
                  />
                  {section.title}
                </h2>
                {section.description && (
                  <p className="mb-4 ml-5 text-sm leading-relaxed text-ink-soft">
                    {section.description}
                  </p>
                )}

                {(section.subsections || []).map((sub) => (
                  <section
                    key={sub.id}
                    id={`subsection-${sub.id}`}
                    className="language-topic mb-4 scroll-mt-24 rounded-xl border border-border bg-card/60 p-4 sm:p-5"
                  >
                    <h3 className="mb-2 text-base font-semibold tracking-tight text-ink">
                      {sub.title}
                    </h3>
                    {sub.description && (
                      <p className="mb-4 text-sm leading-relaxed text-ink-soft">
                        {sub.description}
                      </p>
                    )}
                    <div className="space-y-4">
                      {(sub.content_items || []).map((item) => (
                        <ContentRenderer
                          key={item.id}
                          item={item}
                          sectionTitle={section.title}
                          subsectionTitle={sub.title}
                          languageSlug={slug}
                        />
                      ))}
                    </div>
                  </section>
                ))}
              </section>
            ))
          ) : (
            <div
              className="content-box rounded-2xl border border-border bg-card p-8 text-center sm:p-12"
              style={{
                boxShadow: "var(--shadow-secondary)",
              }}
            >
              <BookOpen className="mx-auto mb-4 h-9 w-9 text-ink-faint" />
              <h3 className="text-lg font-semibold text-ink">
                No lessons available yet
              </h3>
              <p className="mx-auto mt-2 max-w-md text-sm leading-relaxed text-ink-soft">
                There isn’t any learning content for {language.name} yet. Try
                another language or check back later.
              </p>
              <Link
                to="/"
                className="mt-5 inline-flex min-h-10 cursor-pointer items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              >
                <ArrowLeft className="h-4 w-4" />
                Explore languages
              </Link>
            </div>
          )}
          {visibleSectionCount < sections.length ? (
            <div className="space-y-5">
              {Array.from({ length: 2 }).map((_, i) => (
                <SnippetCardSkeleton key={i} />
              ))}
            </div>
          ) : null}
          <div id="quiz" className="scroll-mt-24">
            <Suspense fallback={<SnippetCardSkeleton />}>
              <QuizSection language={slug} />
            </Suspense>
          </div>
          <div id="challenges" className="scroll-mt-24 space-y-5">
            <Suspense fallback={<SnippetCardSkeleton />}>
              <DailyChallenge language={slug} />
              <VisualLearningLab language={slug} />
              <BugFixChallenge language={slug} />
              <CommunitySolutions />
              <SmartNotes language={slug} />
            </Suspense>
          </div>
        </main>

        {/* Right Column — AI Code Doctor, sticky */}
        <aside id="ai-code-doctor-panel" aria-label="AI Code Doctor" className="desktop-side-rail sticky top-20 hidden xl:block">
          <Suspense fallback={<AICodeDoctorSkeleton />}>
            <AICodeDoctor />
          </Suspense>
        </aside>
      </div>
      {mobilePanel ? (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="language-mobile-panel-title"
          className="fixed inset-0 z-50 bg-black/60 p-3 backdrop-blur-sm xl:hidden"
        >
          <div className="h-full rounded-xl bg-card overflow-hidden flex flex-col">
            <div className="flex items-center justify-between border-b border-border px-4 py-3">
            <h3
              id="language-mobile-panel-title"
              className="text-sm font-semibold tracking-tight"
            >
                {mobilePanel === "index" ? "Sections Index" : "AI Code Doctor"}
              </h3>
              <button
                type="button"
                onClick={() => setMobilePanel(null)}
                className="cursor-pointer rounded-md p-2 hover:bg-muted"
                aria-label="Close panel"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="min-h-0 flex-1 overflow-y-auto p-3">
              {mobilePanel === "index" ? (
                <div>
                  <TopicIndex
                    sections={sections}
                    onSectionClick={handleSectionClick}
                    onSubsectionClick={handleSubsectionClick}
                    activeSection={activeSection}
                    activeSubsection={activeSubsection}
                  />
                </div>
              ) : (
                <Suspense fallback={<AICodeDoctorSkeleton />}>
                  <AICodeDoctor />
                </Suspense>
              )}
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
