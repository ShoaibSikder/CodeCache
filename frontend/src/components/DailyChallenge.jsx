import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../App";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Check, Flame, RotateCcw } from "lucide-react";
import { Button } from "./ui/button";
import { getDailyChallenge } from "../lib/learningData";
import { learningAPI } from "../services/api";

export default function DailyChallenge({ language }) {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();
  const challenge = getDailyChallenge(language);
  const today = new Date().toISOString().slice(0, 10);
  const [answer, setAnswer] = useState("");
  const [streak, setStreak] = useState(0);
  const [checked, setChecked] = useState(false);
  const [solvedToday, setSolvedToday] = useState(false);
  const correct = answer.trim() === challenge.answer;

  if (!user) {
    return (
      <section className="learning-card bg-card rounded-xl overflow-hidden">
        <div className="px-4 py-3 bg-muted border-b border-border flex items-center gap-2">
          <Flame className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-bold uppercase tracking-tight">Daily Challenge</h3>
        </div>
        <div className="p-5 text-center">
          <p className="text-sm font-bold">Login to unlock your daily challenge.</p>
          <Link to="/login" state={{ from: `${location.pathname}${location.search}${location.hash}` }} className="mt-3 inline-flex rounded-md bg-primary px-4 py-2 text-sm font-bold text-primary-foreground">
            Login
          </Link>
        </div>
      </section>
    );
  }

  useEffect(() => {
    if (!user) return;
    learningAPI.overview().then((response) => setStreak(response.data.data.streak || 0)).catch(() => {});
  }, [user]);

  const submit = () => {
    setChecked(true);
    if (!correct || solvedToday) return;
    if (!user) {
      navigate("/login", { state: { from: `${location.pathname}${location.search}${location.hash}` } });
      return;
    }
    learningAPI.recordActivity("daily_challenge", `${language}:${today}`, language)
      .then((response) => {
        setStreak(response.data.data.streak || 0);
        setSolvedToday(true);
      });
  };

  return (
    <section className="learning-card bg-card rounded-xl overflow-hidden">
      <div className="px-4 py-3 bg-muted border-b border-border flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <Flame className="h-4 w-4 text-primary" />
          <h3 className="text-sm font-bold uppercase tracking-tight">Daily Challenge</h3>
        </div>
        <span className="text-xs font-bold">{streak} day streak</span>
      </div>
      <div className="p-4 space-y-3">
        <p className="text-sm font-semibold">{challenge.prompt}</p>
        <pre className="code-block text-xs whitespace-pre-wrap">{challenge.code}</pre>
        <div className="flex gap-2">
          <input
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            placeholder="Type output"
            className="min-w-0 flex-1 rounded-md border bg-background px-3 py-2 text-sm"
          />
          <Button type="button" onClick={submit} className="gap-2">
            {solvedToday ? <Check className="h-4 w-4" /> : <RotateCcw className="h-4 w-4" />}
            Check
          </Button>
        </div>
        {checked || solvedToday ? (
          <p className={`text-xs font-semibold ${correct || solvedToday ? "text-emerald-600" : "text-red-600"}`}>
            {correct || solvedToday ? `Correct. ${challenge.explanation}` : "Not quite. Run through the code once more."}
          </p>
        ) : null}
      </div>
    </section>
  );
}
