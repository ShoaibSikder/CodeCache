import { useState, useEffect } from "react";
import { Link, useSearchParams, useNavigate } from "react-router-dom";
import { ArrowRight, BookOpen, Zap, Shield, Code2 } from "lucide-react";
import { motion } from "framer-motion";
import { languagesAPI } from "../services/api";
import { getLanguageColor, getLanguageLogo } from "../lib/languageMeta";
import {
  LanguageCardSkeleton,
  StatsSkeleton,
  HeroSkeleton,
} from "../components/LoadingSkeletons";
import { toast } from "sonner";

export default function Home() {
  const [languages, setLanguages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    fetchLanguages();
  }, []);

  const fetchLanguages = async () => {
    try {
      setLoading(true);
      const response = await languagesAPI.cachedList();
      applyLanguages(response.data.data || []);
      setLoading(false);

      if (response.fromCache) {
        languagesAPI.revalidateList((fresh) => {
          applyLanguages(fresh.data || []);
        });
      }
    } catch (error) {
      console.error("Failed to fetch languages:", error);
      toast.error("Failed to load languages. Please try again.");
      setLanguages([]);
      setLoading(false);
    }
  };

  const applyLanguages = (data) => {
      const enriched = data.map((lang) => ({
        ...lang,
        color: getLanguageColor(lang.slug),
        logo: lang.icon || getLanguageLogo(lang.slug),
        snippetCount: lang.section_count || 0,
      }));
      setLanguages(enriched);
  };

  const totalSnippets = languages.reduce(
    (sum, l) => sum + (l.snippetCount || 0),
    0,
  );

  const searchQuery = searchParams.get("search");

  useEffect(() => {
    if (searchQuery) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`, {
        replace: true,
      });
    }
  }, [searchQuery, navigate]);

  return (
    <div className="py-8 md:py-14">
      {/* Hero Section */}
      {loading ? (
        <HeroSkeleton />
      ) : (
        <div className="mb-14 text-center max-w-2xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-4 tracking-tight leading-tight">
              <span>Code</span>
              <span className="text-primary dark:text-red-400">Cache</span>
            </h1>
            <p className="text-ink font-bold text-lg mb-3">
              The Fastest Way to Recall Code
            </p>
            <p className="text-base text-ink-soft leading-relaxed">
              Curated code snippets for modern developers. Edit, run, and copy —
              right in your browser.
            </p>
          </motion.div>
        </div>
      )}

      {/* Language Grid */}
      {loading ? (
        <div id="languages" className="scroll-mt-24 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5 mb-14">
          {Array.from({ length: 8 }).map((_, i) => (
            <LanguageCardSkeleton key={i} />
          ))}
        </div>
      ) : (
        <div id="languages" className="scroll-mt-24 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5 mb-14">
          {languages.map((language, index) => (
            <motion.div
              key={language.id}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                delay: index * 0.05,
                duration: 0.3,
                ease: "easeOut",
              }}
            >
              <Link to={`/language/${language.slug}`}>
                <div
                  className="group lang-card bg-card cursor-pointer h-full"
                  style={{
                    "--accent": language.color,
                    "--language-accent": language.color,
                  }}
                >
                  <div className="p-5">
                    <div className="flex items-center justify-between mb-3">
                      <span className="language-logo-tile flex h-10 w-10 items-center justify-center rounded-lg bg-background/70">
                        {language.logo ? (
                          <img
                            src={language.logo}
                            alt={`${language.name} logo`}
                            className="h-7 w-7 object-contain"
                            loading="lazy"
                            decoding="async"
                          />
                        ) : (
                          <Code2 className="h-6 w-6 text-ink-soft" />
                        )}
                      </span>
                      <span className="text-xs font-medium text-ink-faint bg-muted px-2 py-0.5 rounded-full">
                        {language.snippetCount} snippets
                      </span>
                    </div>
                    <h3 className="text-base font-bold mb-1 group-hover:text-primary transition-colors">
                      {language.name}
                    </h3>
                    {language.description && (
                      <p className="text-xs text-ink-soft mb-2 line-clamp-1">
                        {language.description}
                      </p>
                    )}
                    <div className="flex items-center gap-1 text-xs text-ink-faint opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                      <span>Explore snippets</span>
                      <ArrowRight className="h-3 w-3" />
                    </div>
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      )}

      {/* Stats Section */}
      {loading ? (
        <StatsSkeleton />
      ) : (
        <div id="stats" className="scroll-mt-24 grid grid-cols-1 sm:grid-cols-3 gap-5">
          {[
            {
              value: `${totalSnippets}+`,
              label: "Code Snippets",
              color: "text-primary",
              icon: BookOpen,
            },
            {
              value: `${languages.length}`,
              label: "Languages",
              color: "text-emerald-600 dark:text-emerald-400",
              icon: Zap,
            },
            {
              value: "AI",
              label: "Powered Features",
              color: "text-violet-600 dark:text-violet-400",
              icon: Shield,
            },
          ].map((stat) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.3 }}
              className="bg-card rounded-xl p-6 text-center transition-all duration-200"
              style={{
                border: "2px solid var(--line)",
                boxShadow: "var(--shadow-primary)",
              }}
            >
              <stat.icon className={`h-6 w-6 mx-auto mb-2 ${stat.color}`} />
              <div
                className={`text-3xl md:text-4xl font-bold mb-1 ${stat.color}`}
              >
                {stat.value}
              </div>
              <div className="text-sm text-ink-soft font-medium uppercase tracking-wide">
                {stat.label}
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Features Section */}

      {/* <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
          {
            icon: '\u{1F4BB}',
            title: 'Editable Code Snippets',
            description: 'Modify code directly in the browser, run it, and see results instantly.',
          },
          {
            icon: '\u{1F9EA}',
            title: 'AI Code Doctor',
            description: 'Get AI-powered code analysis, bug fixes, and optimization suggestions.',
          },
          {
            icon: '\u{1F3AF}',
            title: 'Knowledge Quizzes',
            description: 'Test your understanding with interactive quizzes for each language.',
          },
          {
            icon: '\u{1F4A1}',
            title: 'Real-world Analogies',
            description: 'Complex concepts explained with simple, relatable analogies.',
          },
          {
            icon: '\u{26A0}\u{FE0F}',
            title: 'Common Gotchas',
            description: 'Learn about common pitfalls and how to avoid them in your code.',
          },
          {
            icon: '\u{1F31F}',
            title: 'Syntax Highlighting',
            description: 'Beautiful, readable code with proper syntax highlighting for all languages.',
          },
        ].map((feature, index) => (
          <motion.div
            key={feature.title}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 + index * 0.05, duration: 0.3 }}
            className="bg-card rounded-xl p-6"
                  style={{
                    border: '2px solid var(--line)',
                    boxShadow: 'var(--shadow-primary)',
                  }}
          >
            <span className="text-3xl mb-3 block">{feature.icon}</span>
            <h3 className="font-bold text-foreground mb-2">{feature.title}</h3>
            <p className="text-sm text-ink-soft leading-relaxed">{feature.description}</p>
          </motion.div>
        ))}
      </div> */}
    </div>
  );
}
