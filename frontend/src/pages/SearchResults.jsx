import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { searchAPI, analyticsAPI } from "../services/api";
import { toast } from "sonner";
import { getLanguageColor } from "../lib/languageMeta";
import { Search } from "lucide-react";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";

export default function SearchResults() {
  const [searchParams] = useSearchParams();
  const q = searchParams.get("q");
  const navigate = useNavigate();
  const [draftQuery, setDraftQuery] = useState(q || "");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!q) return;
    let cancelled = false;
    (async () => {
      try {
        setLoading(true);
        const res = await searchAPI.cachedSearch(q);
        let items = res?.data?.results ?? res?.data?.data ?? res?.data ?? [];
        if (!Array.isArray(items)) {
          if (items && typeof items === "object")
            items = items.results ?? items.items ?? [];
          else items = [];
        }
        if (!cancelled) {
          setResults(items);
          analyticsAPI
            .trackSearch({ query: q, results_count: items.length })
            .catch(() => {});
        }
      } catch (err) {
        console.error(err);
        toast.error("Search failed");
        if (!cancelled) setResults([]);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => (cancelled = true);
  }, [q]);

  const handleSubmit = (event) => {
    event.preventDefault();
    const nextQuery = draftQuery.trim();
    if (nextQuery) {
      navigate(`/search?q=${encodeURIComponent(nextQuery)}`);
    }
  };

  return (
    <div className="py-8 md:py-14">
      <div className="max-w-3xl mx-auto text-center mb-6">
        <h2 className="text-xl font-semibold">
          {q ? `Search results for "${q}"` : "Search CodeCache"}
        </h2>
      </div>

      <div className="max-w-3xl mx-auto">
        {!q ? (
          <form onSubmit={handleSubmit} className="bg-card rounded-xl p-4 sm:p-5 border">
            <div className="flex flex-col sm:flex-row gap-3">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-ink-faint" />
                <Input
                  value={draftQuery}
                  onChange={(event) => setDraftQuery(event.target.value)}
                  placeholder="Search snippets, topics, or languages..."
                  className="pl-9"
                />
              </div>
              <Button type="submit" className="sm:w-auto">
                Search
              </Button>
            </div>
          </form>
        ) : loading ? (
          <div className="text-sm text-ink-faint">Searching…</div>
        ) : results.length === 0 ? (
          <div className="text-sm text-ink-faint">No results found.</div>
        ) : (
          <motion.div className="space-y-3">
            {results.map((r) => {
              const langSlug = (
                (r.language?.slug) ||
                r.slug ||
                r.language_slug ||
                r.lang ||
                ""
              )
                .replace(/^\/?(languages?\/)?/, "")
                .replace(/\/$/, "");
              let href = "/";
              if (langSlug) href = `/language/${langSlug}`;
              if (r.subsection_id)
                href = `${href}#subsection-${r.subsection_id}`;
              else if (r.section_id) href = `${href}#section-${r.section_id}`;

              const cardColor = getLanguageColor(langSlug);

              return (
                <Link
                  key={r.id || r.pk || JSON.stringify(r)}
                  to={href}
                  className="block rounded-lg bg-card border border-border hover:bg-muted/80 transition-colors overflow-hidden"
                >
                  <div
                    className="language-accent-bar h-1 w-full"
                    style={{ "--language-accent": cardColor }}
                  />
                  <div className="p-3">
                  <div className="flex items-center justify-between">
                    <div className="font-semibold text-sm text-ink">
                      {r.title || r.name || r.heading || "Result"}
                    </div>
                    <div className="text-xs text-ink-faint">
                      {langSlug || ""}
                    </div>
                  </div>
                  {r.excerpt || r.snippet || r.summary ? (
                    <p className="text-xs text-ink-soft mt-1 line-clamp-3">
                      {r.excerpt || r.snippet || r.summary}
                    </p>
                  ) : null}
                  </div>
                </Link>
              );
            })}
          </motion.div>
        )}
      </div>
    </div>
  );
}
