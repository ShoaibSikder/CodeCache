import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import {
  oneDark,
  oneLight,
} from "react-syntax-highlighter/dist/esm/styles/prism";

export default function CodeHighlighter({
  code,
  displayCode,
  language,
  isDark,
}) {
  return (
    <SyntaxHighlighter
      language={language}
      style={isDark ? oneDark : oneLight}
      customStyle={{
        margin: 0,
        padding: "1rem",
        fontSize: "0.8125rem",
        fontFamily: "'Fira Code', 'Cascadia Code', monospace",
        lineHeight: "1.6",
        borderRadius: 0,
        background: isDark ? "#0d1117" : "#f8fafc",
      }}
      showLineNumbers={code.split("\n").length > 3}
      lineNumberStyle={{
        color: isDark ? "#484f58" : "#9ca3af",
        paddingRight: "1rem",
        userSelect: "none",
        fontSize: "0.75rem",
      }}
    >
      {displayCode}
    </SyntaxHighlighter>
  );
}
