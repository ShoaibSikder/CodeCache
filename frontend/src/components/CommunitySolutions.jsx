import { useContext } from "react";
import { Link, useLocation } from "react-router-dom";
import { MessageSquare, Timer, Wand2 } from "lucide-react";
import { AuthContext } from "../App";

const solutions = [
  { label: "Most upvoted", code: "return text.split('').reverse().join('');", meta: "Clear and readable" },
  { label: "Shortest", code: "[...text].reverse().join('')", meta: "Compact expression" },
  { label: "Most creative", code: "const rev = [...text].reduce((a, c) => c + a, '');", meta: "Uses reduce" },
];

export default function CommunitySolutions() {
  const { user } = useContext(AuthContext);
  const location = useLocation();

  if (!user) {
    return (
      <section className="learning-card bg-card rounded-xl overflow-hidden">
        <div className="px-4 py-3 bg-muted border-b border-border flex items-center gap-2">
          <MessageSquare className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-bold uppercase tracking-tight">Community Solutions</h3>
        </div>
        <div className="p-5 text-center">
          <p className="text-sm font-bold">Login to browse community solutions.</p>
          <Link to="/login" state={{ from: `${location.pathname}${location.search}${location.hash}` }} className="mt-3 inline-flex rounded-md bg-primary px-4 py-2 text-sm font-bold text-primary-foreground">Login</Link>
        </div>
      </section>
    );
  }

  return (
    <section className="learning-card bg-card rounded-xl overflow-hidden">
      <div className="px-4 py-3 bg-muted border-b border-border flex items-center gap-2">
        <MessageSquare className="h-4 w-4 text-primary" />
        <h3 className="text-sm font-bold uppercase tracking-tight">Community Solutions</h3>
      </div>
      <div className="grid gap-3 p-4 md:grid-cols-3">
        {solutions.map((solution) => (
          <div key={solution.label} className="rounded-lg border border-border bg-background/50 p-3">
            <div className="mb-2 flex items-center justify-between gap-2">
              <p className="text-xs font-bold uppercase">{solution.label}</p>
              {solution.label === "Most creative" ? <Wand2 className="h-3.5 w-3.5 text-primary" /> : <Timer className="h-3.5 w-3.5 text-primary" />}
            </div>
            <pre className="code-block text-[11px] whitespace-pre-wrap">{solution.code}</pre>
            <p className="mt-2 text-xs text-ink-soft">{solution.meta}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
