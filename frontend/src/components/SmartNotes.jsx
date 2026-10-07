import { useContext, useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { NotebookPen } from "lucide-react";
import { AuthContext } from "../App";
import { learningAPI } from "../services/api";

export default function SmartNotes({ language }) {
  const { user } = useContext(AuthContext);
  const location = useLocation();
  const [note, setNote] = useState("");

  useEffect(() => {
    if (!user) {
      setNote("");
      return;
    }
    learningAPI.note(language)
      .then((response) => setNote(response.data.data.body || ""))
      .catch(() => setNote(""));
  }, [language, user]);

  useEffect(() => {
    if (!user) return;
    const timeout = setTimeout(() => {
      learningAPI.saveNote(language, note).catch(() => {});
    }, 350);
    return () => clearTimeout(timeout);
  }, [language, note, user]);

  return (
    <section className="learning-card bg-card rounded-xl overflow-hidden">
      <div className="px-4 py-3 bg-muted border-b border-border flex items-center gap-2">
        <NotebookPen className="h-4 w-4 text-primary" />
        <h3 className="text-sm font-bold uppercase tracking-tight">Smart Notes</h3>
      </div>
      <div className="p-4">
        {user ? (
          <textarea
            value={note}
            onChange={(event) => setNote(event.target.value)}
            placeholder="Write your own memory hooks, mistakes, or interview reminders..."
            className="min-h-36 w-full resize-y rounded-lg border bg-background p-3 text-sm leading-relaxed"
          />
        ) : (
          <div className="rounded-lg border border-border bg-background/50 p-4 text-center">
            <p className="text-sm font-bold">Login to keep personal notes.</p>
            <Link to="/login" state={{ from: `${location.pathname}${location.search}${location.hash}` }} className="mt-3 inline-flex rounded-md bg-primary px-4 py-2 text-sm font-bold text-primary-foreground">
              Login
            </Link>
          </div>
        )}
      </div>
    </section>
  );
}
