import { useContext, useMemo, useState } from "react";
import { Brain, Check, ChevronRight, Loader2, RotateCcw, Sparkles, Trophy, X } from "lucide-react";
import { Button } from "./ui/button";
import { aiAPI, learningAPI } from "../services/api";
import { toast } from "sonner";
import { AuthContext } from "../App";

const fallbackTopics = {
  javascript: ["strict equality", "scope", "promises", "arrays"],
  python: ["lists", "functions", "dictionaries", "exceptions"],
  default: ["debugging", "data structures", "testing", "clean code"],
};

function makeFallbackQuiz(language) {
  const topics = fallbackTopics[language] || fallbackTopics.default;
  return topics.map((topic, index) => ({
    id: `${language}-${topic}-${index}`,
    question: `Which statement best describes ${topic}?`,
    options: [
      `${topic} is a concept best learned through practical examples.`,
      `${topic} can be ignored in real projects.`,
      `${topic} only matters after deployment.`,
      `${topic} always works the same in every language.`,
    ],
    correctIndex: 0,
    explanation: `Review examples for ${topic} and focus on when you would use it.`,
  }));
}

function normalizeQuiz(items, language) {
  if (!Array.isArray(items)) return makeFallbackQuiz(language);
  const questions = items.map((item, index) => {
    const options = Array.isArray(item.options) ? item.options.filter(Boolean).slice(0, 4) : [];
    const correctIndex = Number(item.correctIndex ?? item.correct_index ?? item.answer);
    if (!item.question || options.length < 2 || Number.isNaN(correctIndex)) return null;
    return {
      id: item.id || `${language}-ai-${index}`,
      question: String(item.question),
      options,
      correctIndex: Math.max(0, Math.min(correctIndex, options.length - 1)),
      explanation: item.explanation || "",
    };
  }).filter(Boolean);
  return questions.length ? questions : makeFallbackQuiz(language);
}

export default function QuizSection({ language = "default" }) {
  const { user } = useContext(AuthContext);
  const [started, setStarted] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [index, setIndex] = useState(0);
  const [selected, setSelected] = useState(null);
  const [answered, setAnswered] = useState(false);
  const [score, setScore] = useState(0);
  const [complete, setComplete] = useState(false);
  const [loading, setLoading] = useState(false);
  const question = questions[index];

  const languageLabel = useMemo(
    () => (language === "default" ? "Programming" : language.charAt(0).toUpperCase() + language.slice(1)),
    [language],
  );

  const startQuiz = async () => {
    setLoading(true);
    try {
      const response = await aiAPI.generateQuiz(language);
      setQuestions(normalizeQuiz(response.data.data?.questions, language));
      toast.success("AI quiz generated");
    } catch {
      setQuestions(makeFallbackQuiz(language));
      toast.info("AI quiz is unavailable, so a practice quiz is ready instead");
    } finally {
      setIndex(0);
      setSelected(null);
      setAnswered(false);
      setScore(0);
      setComplete(false);
      setStarted(true);
      setLoading(false);
    }
  };

  const chooseAnswer = (optionIndex) => {
    if (answered || !question) return;
    setSelected(optionIndex);
    setAnswered(true);
    if (optionIndex === question.correctIndex) setScore((current) => current + 1);
  };

  const nextQuestion = () => {
    if (index === questions.length - 1) {
      setComplete(true);
      if (user && score === questions.length) {
        learningAPI.recordActivity("quiz", `${language}:${questions.map((item) => item.id).join("|")}`, language).catch(() => {});
      }
      return;
    }
    setIndex((current) => current + 1);
    setSelected(null);
    setAnswered(false);
  };

  return (
    <section className="quiz-card bg-card rounded-xl overflow-hidden" style={{ border: "2px solid var(--line)", boxShadow: "var(--shadow-primary)" }}>
      <div className="px-5 py-3.5 bg-muted border-b border-border flex items-center justify-between gap-3">
        <div className="flex items-center gap-2 min-w-0">
          <Brain className="h-4 w-4 text-primary flex-shrink-0" />
          <h3 className="text-sm font-semibold uppercase tracking-tight text-ink truncate">{languageLabel} Quiz</h3>
        </div>
        {started && !complete ? <span className="text-xs font-bold text-ink-soft">{index + 1}/{questions.length}</span> : null}
      </div>

      <div className="p-5 md:p-6">
        {!started ? (
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h3 className="text-lg font-bold">Test Your Knowledge</h3>
              <p className="mt-1 text-sm text-ink-soft">Answer one question at a time and get feedback immediately.</p>
            </div>
            <Button onClick={startQuiz} disabled={loading} className="gap-2 self-start sm:self-auto">
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
              {loading ? "Generating..." : "Start Quiz"}
            </Button>
          </div>
        ) : complete ? (
          <div className="py-4 text-center">
            <Trophy className="mx-auto mb-3 h-9 w-9 text-amber-500" />
            <h3 className="text-xl font-bold">Quiz complete</h3>
            <p className="mt-1 text-sm text-ink-soft">You answered {score} of {questions.length} correctly.</p>
            <Button onClick={startQuiz} disabled={loading} className="mt-5 gap-2"><RotateCcw className="h-4 w-4" />New Quiz</Button>
          </div>
        ) : question ? (
          <div className="space-y-4">
            <p className="text-base font-semibold leading-relaxed">{question.question}</p>
            <div className="grid gap-2">
              {question.options.map((option, optionIndex) => {
                const correct = answered && optionIndex === question.correctIndex;
                const wrong = answered && selected === optionIndex && optionIndex !== question.correctIndex;
                return (
                  <button type="button" key={option} disabled={answered} onClick={() => chooseAnswer(optionIndex)} className={`flex items-center justify-between gap-3 rounded-lg border px-3 py-2.5 text-left text-sm transition-colors ${
                    correct ? "border-emerald-500 bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-200" :
                    wrong ? "border-red-500 bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-200" :
                    selected === optionIndex ? "border-primary bg-primary/10 text-primary" : "border-border bg-card hover:bg-muted"
                  }`}>
                    <span>{option}</span>
                    {correct ? <Check className="h-4 w-4 flex-shrink-0 text-emerald-600" /> : null}
                    {wrong ? <X className="h-4 w-4 flex-shrink-0 text-red-600" /> : null}
                  </button>
                );
              })}
            </div>
            {answered ? <div className={`rounded-lg border p-3 text-sm ${selected === question.correctIndex ? "border-emerald-500 bg-emerald-50 text-emerald-800 dark:bg-emerald-900/20 dark:text-emerald-200" : "border-red-500 bg-red-50 text-red-800 dark:bg-red-900/20 dark:text-red-200"}`}>
              <p className="font-bold">{selected === question.correctIndex ? "Correct" : "Not quite"}</p>
              {question.explanation ? <p className="mt-1 text-xs leading-relaxed">{question.explanation}</p> : null}
            </div> : null}
            <div className="flex justify-end"><Button onClick={nextQuestion} disabled={!answered} className="gap-2">{index === questions.length - 1 ? "See Result" : "Next"}<ChevronRight className="h-4 w-4" /></Button></div>
          </div>
        ) : null}
      </div>
    </section>
  );
}
