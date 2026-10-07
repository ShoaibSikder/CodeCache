import { useState, useEffect } from "react";
import { lazy, Suspense } from "react";
import { useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import {
  Copy,
  Check,
  Lightbulb,
  Play,
  AlertTriangle,
  Pencil,
  Eye,
  Maximize2,
  Minimize2,
  Heart,
  Bookmark,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { playgroundAPI, learningAPI } from "../services/api";
import { AuthContext } from "../App";
import { toast } from "sonner";

const CodeHighlighter = lazy(() => import("./CodeHighlighter"));

const springTransition = {
  type: "spring",
  stiffness: 380,
  damping: 30,
  mass: 0.8,
};

const fadeSlide = {
  initial: { opacity: 0, y: -6, height: 0 },
  animate: { opacity: 1, y: 0, height: "auto" },
  exit: { opacity: 0, y: -6, height: 0 },
  transition: {
    height: { ...springTransition },
    opacity: { duration: 0.18, ease: "easeOut" },
    y: { ...springTransition },
  },
};

export default function CodeSnippetCard({ snippet }) {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();
  const [isDark, setIsDark] = useState(false);
  const [copied, setCopied] = useState(false);
  const [showAnalogy, setShowAnalogy] = useState(false);
  const [showTryIt, setShowTryIt] = useState(false);
  const [showGotcha, setShowGotcha] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editableCode, setEditableCode] = useState(snippet?.code || "");
  const [output, setOutput] = useState("");
  const [outputType, setOutputType] = useState("success");
  const [isRunning, setIsRunning] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    setIsDark(document.documentElement.classList.contains("dark"));
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.attributeName === "class") {
          setIsDark(document.documentElement.classList.contains("dark"));
        }
      });
    });
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"],
    });
    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!user || !snippet?.id) {
      setIsFavorite(false);
      return;
    }
    learningAPI.saved()
      .then((response) => setIsFavorite(response.data.data.some((item) => item.id === String(snippet.id))))
      .catch(() => setIsFavorite(false));
  }, [user, snippet?.id]);

  const handleCopy = () => {
    navigator.clipboard.writeText(editableCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleFavorite = () => {
    if (!user) {
      toast.info("Login to save snippets to your CodeCache library");
      navigate("/login", { state: { from: `${location.pathname}${location.search}${location.hash}` } });
      return;
    }
    if (!snippet?.id) return;
    learningAPI.toggleSaved(snippet.id)
      .then((response) => setIsFavorite(response.data.data.saved))
      .catch(() => toast.error("Could not update saved snippets"));
  };

  const handleRunCode = async () => {
    if (isRunning) return;
    setShowTryIt(true);
    setOutput("");
    setIsRunning(true);
    try {
      const response = await playgroundAPI.run({
        language,
        code: editableCode,
      });
      const result = response.data.data;
      const errorOutput = result?.error;
      const standardOutput = result?.output || "// Executed with no output";

      setOutput(errorOutput || standardOutput);
      setOutputType(errorOutput ? "error" : "success");
    } catch (err) {
      const message =
        err?.response?.data?.error?.message ||
        err?.response?.data?.error?.details ||
        err?.message ||
        "Failed to run code.";
      setOutput(message);
      setOutputType("error");
    } finally {
      setIsRunning(false);
    }
  };

  const data = snippet?.data || {};
  const title = data.title || snippet?.title || "Untitled";
  const category = data.category || snippet?.category || "Code";
  const language = snippet?.language || data.language || "javascript";
  const analogy = data.analogy || snippet?.analogy;
  const gotcha = data.gotcha || snippet?.gotcha;
  const code = editableCode || data.code || "";

  const displayCode = expanded
    ? code
    : code.split("\n").slice(0, 15).join("\n") +
      (code.split("\n").length > 15 ? "\n// ..." : "");
  const isLongCode = code.split("\n").length > 15;

  return (
    <div
      className="code-snippet-card bg-card rounded-xl overflow-hidden"
      style={{
        border: "2px solid var(--line)",
        boxShadow: "var(--shadow-primary)",
      }}
    >
      {/* Header */}
      <div className="code-card-header px-4 py-3 bg-muted flex items-center justify-between gap-2 border-b border-border">
        <div className="flex items-center gap-2 min-w-0">
          <div className="w-2 h-2 rounded-full bg-primary flex-shrink-0" />
          <h3 className="font-semibold text-sm tracking-tight truncate">
            {category}
          </h3>
          <span className="text-xs text-ink-faint flex-shrink-0">
            ({language})
          </span>
        </div>
        <div className="flex items-center gap-1 flex-shrink-0">
          <button
            onClick={() => setIsEditing(!isEditing)}
            title={isEditing ? "View highlighted" : "Edit code"}
            className="action-pill action-pill-neutral flex items-center gap-1 px-2.5 py-1.5 rounded-md text-xs text-ink-soft hover:text-foreground transition-all dark:hover:bg-muted"
          >
            {isEditing ? (
              <Eye className="h-3 w-3" />
            ) : (
              <Pencil className="h-3 w-3" />
            )}
            <span className="hidden sm:inline">
              {isEditing ? "View" : "Edit"}
            </span>
          </button>
          <button
            onClick={handleCopy}
            className="action-pill action-pill-neutral flex items-center gap-1 px-2.5 py-1.5 rounded-md text-xs text-ink-soft hover:text-foreground transition-all dark:hover:bg-muted"
          >
            {copied ? (
              <>
                <Check className="h-3 w-3 text-green-500" />
                <span className="text-green-500 hidden sm:inline">Copied</span>
              </>
            ) : (
              <>
                <Copy className="h-3 w-3" />
                <span className="hidden sm:inline">Copy</span>
              </>
            )}
          </button>
          <button
            onClick={handleFavorite}
            className={`action-pill action-pill-blue flex items-center gap-1 px-2.5 py-1.5 rounded-md text-xs transition-all ${
              isFavorite ? "text-primary" : "text-ink-soft hover:text-foreground"
            }`}
            title={isFavorite ? "Remove from saved snippets" : "Save snippet"}
          >
            {isFavorite ? <Heart className="h-3 w-3 fill-current" /> : <Bookmark className="h-3 w-3" />}
            <span className="hidden sm:inline">{isFavorite ? "Saved" : "Save"}</span>
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <p className="text-sm text-ink-soft mb-3 leading-relaxed">{title}</p>

        {/* Code Block */}
        <div className="rounded-lg overflow-hidden mb-4 border">
          <AnimatePresence mode="wait" initial={false}>
            {isEditing ? (
              <motion.div
                key="editor"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.15 }}
              >
                <textarea
                  value={editableCode}
                  onChange={(e) => setEditableCode(e.target.value)}
                  spellCheck={false}
                  rows={Math.min(editableCode.split("\n").length + 1, 20)}
                  className="w-full p-4 font-mono text-sm bg-[#f8fafc] dark:bg-[#1e1e1e] text-[#1e293b] dark:text-[#d4d4d4] focus:outline-none resize-none leading-relaxed"
                  style={{
                    minHeight: "80px",
                    fontFamily: "'Fira Code', 'Cascadia Code', monospace",
                  }}
                />
              </motion.div>
            ) : (
              <motion.div
                key="highlighter"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.15 }}
              >
                <Suspense
                  fallback={
                    <pre className="m-0 min-h-24 bg-[#f8fafc] p-4 font-mono text-xs leading-relaxed text-[#1e293b] dark:bg-[#0d1117] dark:text-[#d4d4d4]">
                      {displayCode}
                    </pre>
                  }
                >
                  <CodeHighlighter
                    code={code}
                    displayCode={displayCode}
                    language={language}
                    isDark={isDark}
                  />
                </Suspense>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Expand/Collapse for long code */}
          {!isEditing && isLongCode && (
            <button
              onClick={() => setExpanded(!expanded)}
              className="code-expand-button w-full py-1.5 text-xs text-center text-ink-soft hover:text-primary bg-muted/50 hover:bg-muted transition-colors flex items-center justify-center gap-1"
            >
              {expanded ? (
                <>
                  <Minimize2 className="h-3 w-3" /> Show Less
                </>
              ) : (
                <>
                  <Maximize2 className="h-3 w-3" /> Show Full Code (
                  {code.split("\n").length} lines)
                </>
              )}
            </button>
          )}
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap gap-2 mb-1">
          {analogy && (
            <button
              onClick={() => setShowAnalogy(!showAnalogy)}
              className={`action-pill action-pill-amber flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-all duration-200 ${
                showAnalogy
                  ? "bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-300 ring-1 ring-amber-300 dark:ring-amber-700"
                  : "bg-amber-50 text-ink-soft hover:bg-amber-100 dark:bg-muted dark:hover:bg-amber-900/20 hover:text-amber-700 dark:hover:text-amber-400"
              }`}
            >
              <Lightbulb className="h-3 w-3" />
              Analogy
            </button>
          )}
          <button
            onClick={handleRunCode}
            disabled={isRunning}
            className={`action-pill action-pill-green flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-all duration-200 ${
              showTryIt
                ? "bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300 ring-1 ring-emerald-300 dark:ring-emerald-700"
                : "bg-emerald-50 text-ink-soft hover:bg-emerald-100 dark:bg-muted dark:hover:bg-emerald-900/20 hover:text-emerald-700 dark:hover:text-emerald-400"
            }`}
          >
            <Play className={`h-3 w-3 ${isRunning ? "animate-pulse" : ""}`} />
            {isRunning ? "Running..." : "Run It"}
          </button>
          {gotcha && (
            <button
              onClick={() => setShowGotcha(!showGotcha)}
              className={`action-pill action-pill-red flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs transition-all duration-200 ${
                showGotcha
                  ? "bg-rose-100 dark:bg-rose-900/40 text-rose-700 dark:text-rose-300 ring-1 ring-rose-300 dark:ring-rose-700"
                  : "bg-rose-50 text-ink-soft hover:bg-rose-100 dark:bg-muted dark:hover:bg-rose-900/20 hover:text-rose-700 dark:hover:text-rose-400"
              }`}
            >
              <AlertTriangle className="h-3 w-3" />
              Gotcha
            </button>
          )}
        </div>

        {/* Expandable Sections */}
        <AnimatePresence initial={false}>
          {showAnalogy && analogy && (
            <motion.div
              key="analogy"
              style={{ overflow: "hidden" }}
              {...fadeSlide}
            >
              <div className="snippet-info-panel snippet-info-panel-amber mt-3 p-3 rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800/50 flex items-start gap-2.5">
                <Lightbulb className="h-3.5 w-3.5 flex-shrink-0 mt-0.5 text-amber-500" />
                <p className="text-xs text-amber-800 dark:text-amber-200 leading-relaxed">
                  {analogy}
                </p>
              </div>
            </motion.div>
          )}

          {showTryIt && (
            <motion.div
              key="try-it"
              style={{ overflow: "hidden" }}
              {...fadeSlide}
            >
              <div className="snippet-info-panel snippet-info-panel-green mt-3 p-3 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800/50 space-y-2.5">
                {isRunning && (
                  <div className="flex items-center gap-2 text-xs font-semibold text-emerald-700 dark:text-emerald-300">
                    <Play className="h-3 w-3 animate-pulse" />
                    Running code...
                  </div>
                )}
                <AnimatePresence>
                  {output && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      style={{ overflow: "hidden" }}
                      transition={{ duration: 0.2, ease: "easeOut" }}
                      className={`rounded-lg p-3 font-mono text-xs leading-relaxed ${
                        outputType === "error"
                          ? "bg-red-50 dark:bg-red-950 text-red-800 dark:text-red-300 border border-red-200 dark:border-red-800"
                          : "bg-[#f1f5f9] dark:bg-[#0d1117] text-emerald-700 dark:text-emerald-400 border border-border"
                      }`}
                    >
                      <pre className="whitespace-pre-wrap">{output}</pre>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          )}

          {showGotcha && gotcha && (
            <motion.div
              key="gotcha"
              style={{ overflow: "hidden" }}
              {...fadeSlide}
            >
              <div className="snippet-info-panel snippet-info-panel-red mt-3 p-3 rounded-lg bg-rose-50 dark:bg-rose-900/20 border border-rose-200 dark:border-rose-800/50 flex items-start gap-2.5">
                <AlertTriangle className="h-3.5 w-3.5 flex-shrink-0 mt-0.5 text-rose-500" />
                <p className="text-xs text-rose-800 dark:text-rose-200 leading-relaxed">
                  {gotcha}
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}




