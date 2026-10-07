import { useContext, useState } from "react";
import { AuthContext } from "../App";
import { Link, useLocation } from "react-router-dom";
import { Bug, CheckCircle2 } from "lucide-react";
import { getBugFixChallenge } from "../lib/learningData";
import { learningAPI } from "../services/api";

export default function BugFixChallenge({ language }) {
  const { user } = useContext(AuthContext);
  const location = useLocation();
  const challenge = getBugFixChallenge(language);
  const [selected, setSelected] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const correct = selected === challenge.answer;

  if (!user) {
    return (
      <section className="learning-card bg-card rounded-xl overflow-hidden">
        <div className="px-4 py-3 bg-muted border-b border-border flex items-center gap-2">
          <Bug className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-bold uppercase tracking-tight">Learn By Fixing Bugs</h3>
        </div>
        <div className="p-5 text-center">
          <p className="text-sm font-bold">Login to unlock bug-fixing challenges.</p>
          <Link to="/login" state={{ from: `${location.pathname}${location.search}${location.hash}` }} className="mt-3 inline-flex rounded-md bg-primary px-4 py-2 text-sm font-bold text-primary-foreground">Login</Link>
        </div>
      </section>
    );
  }

  const submit = (choice) => {
    setSelected(choice);
    setSubmitted(true);
    if (choice === challenge.answer) {
      learningAPI.recordActivity("bug_fix", `${language}:${challenge.title}`, language).catch(() => {});
    }
  };

  return (
    <section className="learning-card bg-card rounded-xl overflow-hidden">
      <div className="px-4 py-3 bg-muted border-b border-border flex items-center gap-2">
        <Bug className="h-4 w-4 text-primary" />
        <h3 className="text-sm font-bold uppercase tracking-tight">Learn By Fixing Bugs</h3>
      </div>
      <div className="p-4 space-y-3">
        <h4 className="font-bold">{challenge.title}</h4>
        <pre className="code-block text-xs whitespace-pre-wrap">{challenge.broken}</pre>
        <div className="grid gap-2 sm:grid-cols-3">
          {challenge.choices.map((choice) => (
            <button
              key={choice}
              type="button"
              onClick={() => submit(choice)}
              className={`rounded-lg border border-border px-3 py-2 text-left text-sm font-bold transition-colors ${
                selected === choice ? "bg-primary/10 text-primary" : "bg-background/50 hover:bg-muted"
              }`}
            >
              {choice}
            </button>
          ))}
        </div>
        {submitted ? (
          <div className={`rounded-lg border p-3 text-sm ${correct ? "border-emerald-500 bg-emerald-50 text-emerald-800 dark:bg-emerald-900/20 dark:text-emerald-200" : "border-red-500 bg-red-50 text-red-800 dark:bg-red-900/20 dark:text-red-200"}`}>
            <div className="mb-2 flex items-center gap-2 font-bold">
              <CheckCircle2 className="h-4 w-4" />
              {correct ? "Fixed" : "Try again"}
            </div>
            <p className="text-xs">{challenge.explanation}</p>
            {correct ? <pre className="mt-3 code-block text-xs whitespace-pre-wrap">{challenge.fixed}</pre> : null}
          </div>
        ) : null}
      </div>
    </section>
  );
}
