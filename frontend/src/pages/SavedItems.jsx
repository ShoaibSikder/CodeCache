import { useContext, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, Bookmark, Copy } from "lucide-react";
import { AuthContext } from "../App";
import { Button } from "../components/ui/button";
import { learningAPI } from "../services/api";
import { toast } from "sonner";

export default function SavedItems() {
  const { user } = useContext(AuthContext);
  const [items, setItems] = useState([]);

  useEffect(() => {
    if (!user) return;
    learningAPI.saved().then((response) => setItems(response.data.data)).catch(() => setItems([]));
  }, [user]);

  if (!user) {
    return (
      <div className="py-12 max-w-xl mx-auto">
        <Link to="/" className="inline-flex items-center gap-1.5 text-sm text-ink-soft hover:text-primary mb-6">
          <ArrowLeft className="h-3.5 w-3.5" />
          Back to Home
        </Link>
        <div className="learning-card bg-card rounded-xl p-6 text-center">
          <Bookmark className="h-8 w-8 text-primary mx-auto mb-3" />
          <h1 className="text-2xl font-bold mb-2">Login to See Saved Items</h1>
          <p className="text-sm text-ink-soft mb-5">
            Saved snippets belong to your personal CodeCache account.
          </p>
          <Button asChild>
            <Link to="/login">Login</Link>
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="py-8 md:py-12">
      <Link to="/" className="inline-flex items-center gap-1.5 text-sm text-ink-soft hover:text-primary mb-6">
        <ArrowLeft className="h-3.5 w-3.5" />
        Back to Home
      </Link>
      <div className="mb-6">
        <h1 className="text-3xl font-bold tracking-tight">Saved Items</h1>
        <p className="text-sm text-ink-soft mt-1">{items.length} snippets in your library</p>
      </div>
      {items.length ? (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {items.map((item) => (
            <article key={item.id} className="learning-card bg-card rounded-xl overflow-hidden">
              <div className="border-b border-border bg-muted px-4 py-3">
                <p className="text-sm font-bold truncate">{item.title}</p>
                <p className="text-xs text-ink-faint">{item.language} · {item.category}</p>
              </div>
              <div className="p-4">
                <pre className="code-block max-h-64 text-xs whitespace-pre-wrap">{item.code}</pre>
                <Button
                  type="button"
                  variant="outline"
                  className="mt-3 w-full gap-2"
                  onClick={() => {
                    navigator.clipboard.writeText(item.code);
                    toast.success("Snippet copied");
                  }}
                >
                  <Copy className="h-4 w-4" />
                  Copy
                </Button>
              </div>
            </article>
          ))}
        </div>
      ) : (
        <div className="learning-card bg-card rounded-xl p-8 text-center">
          <Bookmark className="h-8 w-8 text-primary mx-auto mb-3" />
          <h2 className="text-xl font-bold mb-2">No saved snippets yet</h2>
          <p className="text-sm text-ink-soft">Open a language page and save useful examples.</p>
        </div>
      )}
    </div>
  );
}
