import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, ChevronRight, Layers } from "lucide-react";

export default function TopicIndex({
  sections,
  onSectionClick,
  onSubsectionClick,
  activeSection,
  activeSubsection,
}) {
  const [expandedSections, setExpandedSections] = useState({});

  if (!sections || sections.length === 0) return null;

  const toggleSection = (secId, e) => {
    e.stopPropagation();
    setExpandedSections((prev) => ({ ...prev, [secId]: !prev[secId] }));
  };

  const handleSectionClick = (secId) => {
    onSectionClick?.(secId);
  };

  const handleSubsectionClick = (subId) => {
    onSubsectionClick?.(subId);
  };

  return (
    <div
      className="topic-index-card overflow-hidden h-[650px] flex flex-col"
      style={{
        border: "2px solid var(--line)",
      }}
    >
      <div className="topic-index-header px-4 py-3 bg-muted border-b border-border">
        <h3 className="text-sm font-semibold tracking-tight uppercase text-ink">
          Sections Index
        </h3>
      </div>
      <div className="p-2 min-h-0 flex-1 overflow-y-auto">
        <div className="space-y-0.5">
          {sections.map((section, index) => {
            const isExpanded = expandedSections[section.id];
            const subs = section.subsections || [];
            return (
              <div key={section.id}>
                <motion.div
                  initial={{ opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{
                    delay: index * 0.04,
                    duration: 0.2,
                    ease: "easeOut",
                  }}
                >
                  <div className="flex items-center w-full">
                    <button
                      onClick={(e) => toggleSection(section.id, e)}
                      className="p-1 rounded-md flex-shrink-0"
                      title={
                        isExpanded ? "Collapse subsections" : "Show subsections"
                      }
                    >
                      {isExpanded ? (
                        <ChevronDown className="h-3 w-3 text-ink-faint" />
                      ) : (
                        <ChevronRight className="h-3 w-3 text-ink-faint" />
                      )}
                    </button>
                    <button
                      onClick={() => handleSectionClick(section.id)}
                      className={`flex-1 text-left px-2 py-2 rounded-lg text-sm transition-all duration-150 flex items-center gap-2 ${
                        activeSection === section.id
                          ? "bg-primary/10 text-primary font-medium"
                          : "text-ink-soft"
                      }`}
                    >
                      <Layers
                        className={`h-3 w-3 flex-shrink-0 ${
                          activeSection === section.id
                            ? "text-primary"
                            : "text-ink-faint"
                        }`}
                      />
                      <span className="truncate">{section.title}</span>
                      {subs.length > 0 && (
                        <span className="text-[10px] text-ink-faint ml-auto flex-shrink-0">
                          {subs.length}
                        </span>
                      )}
                    </button>
                  </div>
                </motion.div>

                <AnimatePresence>
                  {isExpanded && subs.length > 0 && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="overflow-hidden"
                    >
                      <div className="ml-5 pl-3 border-l-2 border-border space-y-0.5">
                        {subs.map((sub, subIdx) => (
                          <motion.button
                            key={sub.id}
                            initial={{ opacity: 0, x: -4 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{
                              delay: subIdx * 0.03,
                              duration: 0.15,
                            }}
                            onClick={() => handleSubsectionClick(sub.id)}
                            className={`w-full text-left px-2.5 py-1.5 rounded-md text-xs transition-all duration-150 flex items-center gap-2 ${
                              activeSubsection === sub.id
                                ? "bg-primary/10 text-primary font-medium"
                                : "text-ink-soft"
                            }`}
                          >
                            <ChevronRight
                              className={`h-2.5 w-2.5 flex-shrink-0 ${
                                activeSubsection === sub.id
                                  ? "rotate-90 text-primary"
                                  : "text-ink-faint"
                              }`}
                            />
                            <span className="truncate">{sub.title}</span>
                          </motion.button>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
