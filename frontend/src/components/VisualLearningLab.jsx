import { useContext, useMemo, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { Boxes, Play } from "lucide-react";
import { AuthContext } from "../App";

export default function VisualLearningLab({ language }) {
  const { user } = useContext(AuthContext);
  const location = useLocation();
  const [value, setValue] = useState(5);
  const [increment, setIncrement] = useState(3);
  const result = value + increment;
  const isPython = language === "python";
  const code = isPython
    ? `x = ${value}\nx += ${increment}\nprint(x)`
    : `let x = ${value};\nx += ${increment};\nconsole.log(x);`;
  const memory = useMemo(
    () => [
      { label: "x", before: value, after: result },
      { label: "increment", before: increment, after: increment },
    ],
    [value, increment, result],
  );

  if (!user) {
    return (
      <section className="learning-card bg-card rounded-xl overflow-hidden">
        <div className="px-4 py-3 bg-muted border-b border-border flex items-center gap-2">
          <Boxes className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-bold uppercase tracking-tight">Memory Visualizer</h3>
        </div>
        <div className="p-5 text-center">
          <p className="text-sm font-bold">Login to use the interactive memory visualizer.</p>
          <Link to="/login" state={{ from: `${location.pathname}${location.search}${location.hash}` }} className="mt-3 inline-flex rounded-md bg-primary px-4 py-2 text-sm font-bold text-primary-foreground">
            Login
          </Link>
        </div>
      </section>
    );
  }

  return (
    <section className="learning-card bg-card rounded-xl overflow-hidden">
      <div className="px-4 py-3 bg-muted border-b border-border flex items-center gap-2">
        <Boxes className="h-4 w-4 text-primary" />
        <h3 className="text-sm font-bold uppercase tracking-tight">Memory Visualizer</h3>
      </div>
      <div className="grid gap-4 p-4 md:grid-cols-[1fr_220px]">
        <div className="space-y-3">
          <pre className="code-block text-xs whitespace-pre-wrap">{code}</pre>
          <div className="grid grid-cols-2 gap-3">
            <label className="text-xs font-bold">
              Start value
              <input
                type="range"
                min="0"
                max="20"
                value={value}
                onChange={(e) => setValue(Number(e.target.value))}
                className="mt-2 w-full"
              />
            </label>
            <label className="text-xs font-bold">
              Add
              <input
                type="range"
                min="1"
                max="10"
                value={increment}
                onChange={(e) => setIncrement(Number(e.target.value))}
                className="mt-2 w-full"
              />
            </label>
          </div>
        </div>
        <div className="rounded-lg border border-border bg-background/50 p-3">
          <div className="mb-2 flex items-center gap-2 text-xs font-bold uppercase">
            <Play className="h-3.5 w-3.5 text-primary" />
            Animation
          </div>
          <div className="space-y-2">
            {memory.map((slot) => (
              <div key={slot.label} className="rounded-md border border-border bg-card p-2 text-xs">
                <div className="font-bold">{slot.label}</div>
                <div className="mt-1 flex items-center justify-between gap-2">
                  <span>{slot.before}</span>
                  <span className="text-ink-faint">to</span>
                  <span className="font-bold text-primary">{slot.after}</span>
                </div>
              </div>
            ))}
          </div>
          <p className="mt-3 text-xs text-ink-soft">Output: {result}</p>
        </div>
      </div>
    </section>
  );
}
