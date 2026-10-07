import { useState } from "react";
import {
  ArrowRight,
  Loader2,
  Stethoscope,
  Wand2,
  Sparkles,
  X,
} from "lucide-react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";
import { aiAPI } from "../services/api";
import { toast } from "sonner";
import { motion, AnimatePresence } from "framer-motion";

export default function AICodeDoctor() {
  const [code, setCode] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState("javascript");

  const languages = [
    "javascript",
    "python",
    "typescript",
    "css",
    "html",
    "sql",
    "java",
    "cpp",
    "go",
    "rust",
  ];

  const handleFix = async () => {
    if (!code.trim()) return;
    setLoading(true);
    setResult("");
    try {
      const response = await aiAPI.codeDoctor(code, language);
      setResult(response.data.data?.result || "No result returned.");
      toast.success("AI analysis complete!");
    } catch (error) {
      console.error("AI Code Doctor error:", error);
      const fallbackResult = analyzeCodeLocally(code, language);
      setResult(fallbackResult);
      toast.info("Using offline analysis - AI service unavailable");
    } finally {
      setLoading(false);
    }
  };

  const analyzeCodeLocally = (inputCode, lang) => {
    let analysis = `## Local Code Analysis (${lang})\n\n`;
    const lines = inputCode.split("\n");
    const issues = [];

    if (!inputCode.includes(";") && lang === "javascript") {
      issues.push("- Consider adding semicolons for consistency");
    }
    if (
      inputCode.includes("var ") &&
      (lang === "javascript" || lang === "typescript")
    ) {
      issues.push("- Replace `var` with `let` or `const` for better scoping");
    }
    if (inputCode.includes("console.log")) {
      issues.push("- Remove `console.log` statements before production");
    }
    if (
      inputCode.includes("==") &&
      !inputCode.includes("===") &&
      lang === "javascript"
    ) {
      issues.push("- Use `===` instead of `==` for strict equality checks");
    }
    if (!inputCode.includes("try") && inputCode.includes("await")) {
      issues.push("- Wrap async operations in try/catch blocks");
    }
    if (
      lang === "python" &&
      inputCode.includes("except:") &&
      !inputCode.includes("except Exception")
    ) {
      issues.push("- Catch specific exceptions instead of bare `except:`");
    }
    if (lines.some((l) => l.length > 120)) {
      issues.push("- Some lines exceed 120 characters, consider breaking them");
    }
    if (inputCode.includes("TODO") || inputCode.includes("FIXME")) {
      issues.push("- Address TODO/FIXME comments before committing");
    }

    if (issues.length === 0) {
      analysis += "### No obvious issues found!\n\n";
      analysis += "Your code looks clean. Consider:\n";
      analysis += "- Adding comments for complex logic\n";
      analysis += "- Writing unit tests if not already present\n";
      analysis += "- Checking for edge cases\n";
    } else {
      analysis += "### Potential Issues Found:\n\n";
      analysis += issues.join("\n") + "\n\n";
      analysis += "### Suggestions:\n";
      analysis += "- Review each issue above\n";
      analysis += "- Run a linter for more detailed analysis\n";
      analysis += "- Test with edge cases\n";
    }

    return analysis;
  };

  return (
    <div
      className="ai-doctor-card bg-card overflow-hidden flex flex-col relative h-[650px]"
      style={{
        border: "2px solid var(--line)",
      }}
    >
      <div className="px-4 py-3 bg-rose-50 dark:bg-rose-900/20 border-b border-border flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Stethoscope className="h-3.5 w-3.5 text-rose-500" />
          <h3 className="text-sm font-semibold text-rose-700 dark:text-rose-400 tracking-tight uppercase text-ink">
            AI Code Doctor
          </h3>
        </div>
        <Sparkles className="h-3.5 w-3.5 text-rose-400 animate-pulse" />
      </div>

      <div className="p-4 flex min-h-0 flex-1 flex-col space-y-3">
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="w-full rounded-lg border bg-background px-3 py-1.5 text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        >
          {languages.map((lang) => (
            <option key={lang} value={lang}>
              {lang.charAt(0).toUpperCase() + lang.slice(1)}
            </option>
          ))}
        </select>

        <p className="text-xs text-ink-soft leading-relaxed">
          Paste broken code for AI-powered analysis and fixes
        </p>

        <Textarea
          placeholder="// Paste your code here..."
          value={code}
          onChange={(e) => setCode(e.target.value)}
          className="rounded-lg font-mono text-xs min-h-[180px] flex-1 resize-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-0 placeholder:text-ink-faint"
        />

        <Button
          onClick={handleFix}
          disabled={!code.trim() || loading}
          className="w-full rounded-lg bg-indigo-600 text-white text-xs font-medium disabled:opacity-50"
        >
          {loading ? (
            <>
              <Loader2 className="h-3 w-3 mr-1.5 animate-spin" />
              Analyzing with AI...
            </>
          ) : (
            <>
              <Wand2 className="h-3 w-3 mr-1.5" />
              Fix My Code
              <ArrowRight className="h-3 w-3 ml-1.5" />
            </>
          )}
        </Button>
      </div>

      {/* Result Overlay — covers the box without expanding it */}
      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 z-10 bg-card flex flex-col rounded-xl"
            style={{ border: "2px solid var(--line)" }}
          >
            <div className="px-4 py-3 bg-emerald-50 dark:bg-emerald-900/20 border-b border-border flex items-center justify-between flex-shrink-0">
              <div className="flex items-center gap-2">
                <Sparkles className="h-3.5 w-3.5 text-emerald-500" />
                <h3 className="text-sm font-semibold text-emerald-700 dark:text-emerald-400 tracking-tight uppercase text-ink">
                  Analysis Result
                </h3>
              </div>
              <button onClick={() => setResult("")} className="p-1 rounded-md">
                <X className="h-4 w-4 text-emerald-600 dark:text-emerald-400" />
              </button>
            </div>
            <div className="p-4 overflow-y-auto flex-1">
              <pre className="font-mono text-xs whitespace-pre-wrap text-foreground leading-relaxed">
                {result}
              </pre>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
