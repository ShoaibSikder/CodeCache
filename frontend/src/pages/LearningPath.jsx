import { useEffect, useState } from "react";
import { ArrowLeft, Route } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import LearningDashboard from "../components/LearningDashboard";
import { languagesAPI, learningAPI } from "../services/api";

export default function LearningPath() {
  const navigate = useNavigate();
  const [language, setLanguage] = useState(null);
  const [loading, setLoading] = useState(true);
  const [slug, setSlug] = useState(null);

  useEffect(() => {
    let active = true;

    Promise.all([learningAPI.overview(), languagesAPI.cachedList()])
      .then(([overviewResponse, languagesResponse]) => {
        const languages = languagesResponse.data.data || [];
        const selectedSlug = overviewResponse.data.data?.last_language_slug || languages[0]?.slug;
        if (!selectedSlug) return null;
        setSlug(selectedSlug);
        return languagesAPI.cachedDetail(selectedSlug);
      })
      .then((response) => {
        if (!response || !active) return;
        setLanguage(response.data.data);
      })
      .catch(() => {
        if (active) setLanguage(null);
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, []);

  return (
    <div className="mx-auto max-w-3xl py-8 md:py-12">
      <Link
        to="/"
        className="mb-6 inline-flex items-center gap-1.5 text-sm text-ink-soft hover:text-primary"
      >
        <ArrowLeft className="h-3.5 w-3.5" />
        Back to Home
      </Link>

      <div className="mb-6">
        <div className="flex items-center gap-2">
          <Route className="h-5 w-5 text-primary" />
          <h1 className="text-3xl font-bold tracking-tight">Learning Path</h1>
        </div>
        <p className="mt-1 text-sm text-ink-soft">
          Track your progress and choose the next topic in your {language?.name || "learning"} path.
        </p>
      </div>

      {loading ? (
        <div className="learning-card h-[650px] animate-pulse bg-card rounded-xl" />
      ) : language ? (
        <LearningDashboard
          language={slug}
          sections={language.sections || []}
          onJump={(subsectionId) => navigate(`/language/${slug}#subsection-${subsectionId}`)}
        />
      ) : (
        <div className="learning-card rounded-xl bg-card p-8 text-center">
          <Route className="mx-auto mb-3 h-8 w-8 text-primary" />
          <h2 className="text-xl font-bold">Choose a language to begin</h2>
          <p className="mt-2 text-sm text-ink-soft">Open a cheat sheet first, then return here to track its path.</p>
          <Link to="/" className="mt-5 inline-flex rounded-md bg-primary px-4 py-2 text-sm font-bold text-primary-foreground">
            Browse languages
          </Link>
        </div>
      )}
    </div>
  );
}
