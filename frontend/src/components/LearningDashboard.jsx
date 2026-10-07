import { useContext, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { Award, CheckCircle2, Flame, Medal, Route, Star, Trophy } from "lucide-react";
import { AuthContext } from "../App";
import { getDifficulty, getLevelFromXp } from "../lib/learningData";
import { learningAPI } from "../services/api";

const emptyProgress = { xp: 0, streak: 0, completed_subsection_ids: [], saved_content_item_ids: [] };

export default function LearningDashboard({ language, sections, onJump }) {
  const { user } = useContext(AuthContext);
  const [progress, setProgress] = useState(emptyProgress);

  useEffect(() => {
    if (!user) return;
    learningAPI.overview().then((response) => setProgress(response.data.data)).catch(() => setProgress(emptyProgress));
  }, [user]);

  const topics = useMemo(
    () =>
      (sections || []).flatMap((section, sectionIndex) =>
        (section.subsections || []).map((subsection, topicIndex) => ({
          id: String(subsection.id),
          title: subsection.title,
          sectionTitle: section.title,
          difficulty: getDifficulty(sectionIndex + topicIndex),
          subsectionId: subsection.id,
        })),
      ),
    [language, sections],
  );

  const completed = topics.filter((topic) => progress.completed_subsection_ids.includes(topic.id)).length;
  const percent = topics.length ? Math.round((completed / topics.length) * 100) : 0;
  const level = getLevelFromXp(progress.xp);
  const badges = [
    completed >= 1 && "First Topic",
    percent >= 50 && "Path Climber",
    progress.streak >= 3 && "Streak Builder",
    progress.saved_content_item_ids.length >= 3 && "Snippet Collector",
    progress.xp >= 500 && "Quiz Champion",
  ].filter(Boolean);

  const markTopic = (topic) => {
    if (!user) return;
    learningAPI.completeTopic(topic.id).then((response) => {
      setProgress((current) => ({
        ...current,
        xp: response.data.data.xp,
        completed_subsection_ids: current.completed_subsection_ids.includes(topic.id)
          ? current.completed_subsection_ids
          : [...current.completed_subsection_ids, topic.id],
      }));
    });
  };

  return (
    <div id="learning-path" className="learning-card bg-card rounded-xl overflow-hidden h-[650px] flex flex-col">
      <div className="px-4 py-3 bg-muted border-b border-border flex items-center gap-2">
        <Route className="h-4 w-4 text-primary" />
        <h3 className="text-sm font-bold uppercase tracking-tight">Learning Path</h3>
      </div>
      {!user ? (
        <div className="flex min-h-0 flex-1 flex-col items-center justify-center p-5 text-center">
          <Route className="mb-3 h-8 w-8 text-primary" />
          <h4 className="text-lg font-bold">Login to Track Progress</h4>
          <p className="mt-2 text-sm text-ink-soft">
            Cheat sheets stay open to everyone. Progress, XP, badges, and learning paths need an account.
          </p>
          <Link
            to="/login"
            className="mt-5 inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-bold text-primary-foreground"
          >
            Login
          </Link>
        </div>
      ) : (
      <div className="p-4 space-y-4 min-h-0 flex-1 overflow-y-auto">
        <div>
          <div className="flex items-center justify-between gap-3 text-sm font-bold">
            <span>Progress: {percent}%</span>
            <span>{completed}/{topics.length}</span>
          </div>
          <div className="mt-2 h-2 rounded-full bg-muted overflow-hidden border border-border">
            <div className="h-full bg-primary" style={{ width: `${percent}%` }} />
          </div>
        </div>

        <div className="rounded-lg border border-border bg-background/50 p-3">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-xs text-ink-faint">Level {level.level}</p>
              <p className="text-sm font-bold">{level.title}</p>
            </div>
            <Trophy className="h-5 w-5 text-amber-500" />
          </div>
          <div className="mt-3 h-2 rounded-full bg-muted overflow-hidden border border-border">
            <div className="h-full bg-amber-400" style={{ width: `${level.progress}%` }} />
          </div>
          <p className="mt-2 text-xs text-ink-soft">XP: {progress.xp}/{level.next}</p>
        </div>

        <div className="grid grid-cols-2 gap-2">
          <Stat icon={Flame} label="Streak" value={`${progress.streak} days`} />
          <Stat icon={Star} label="Saved" value={progress.saved_content_item_ids.length} />
        </div>

        <div className="space-y-1.5">
          {topics.map((topic) => (
            <button
              key={topic.id}
              type="button"
              onClick={() => {
                markTopic(topic);
                onJump?.(topic.subsectionId);
              }}
              className="w-full rounded-lg border border-border bg-background/50 px-3 py-2 text-left text-xs hover:bg-muted transition-colors"
            >
              <span className="flex items-center justify-between gap-2">
                <span className="min-w-0">
                  <span className="block font-bold truncate">{topic.title}</span>
                  <span className="block text-ink-faint truncate">{topic.sectionTitle}</span>
                </span>
                <span className={`difficulty-pill ${topic.difficulty.className}`}>
                  {topic.difficulty.label}
                </span>
              </span>
              {progress.completed_subsection_ids.includes(topic.id) ? (
                <span className="mt-1 flex items-center gap-1 text-emerald-600 font-bold">
                  <CheckCircle2 className="h-3 w-3" />
                  Complete
                </span>
              ) : null}
            </button>
          ))}
        </div>

        <div>
          <div className="mb-2 flex items-center gap-2 text-xs font-bold uppercase">
            <Medal className="h-3.5 w-3.5 text-primary" />
            Badges
          </div>
          <div className="flex flex-wrap gap-2">
            {(badges.length ? badges : ["Start Learning"]).map((badge) => (
              <span key={badge} className="badge-pill">
                <Award className="h-3 w-3" />
                {badge}
              </span>
            ))}
          </div>
        </div>
      </div>
      )}
    </div>
  );
}

function Stat({ icon: Icon, label, value }) {
  return (
    <div className="rounded-lg border border-border bg-background/50 p-3">
      <Icon className="mb-1 h-4 w-4 text-primary" />
      <p className="text-[10px] uppercase text-ink-faint font-bold">{label}</p>
      <p className="text-sm font-bold">{value}</p>
    </div>
  );
}
