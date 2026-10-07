export const levelNames = [
  "Beginner Coder",
  "Explorer",
  "Developer",
  "Builder",
  "Problem Solver",
  "Code Mentor",
];

export const xpActions = {
  read: 20,
  quiz: 75,
  challenge: 90,
  bugfix: 60,
  favorite: 10,
  note: 15,
};

export function getLevelFromXp(xp = 0) {
  const thresholds = [0, 200, 500, 1000, 1700, 2600];
  const index = thresholds.reduce(
    (level, threshold, i) => (xp >= threshold ? i : level),
    0,
  );
  const current = thresholds[index] || 0;
  const next = thresholds[index + 1] || current + 1200;
  return {
    level: index + 1,
    title: levelNames[index] || levelNames[levelNames.length - 1],
    current,
    next,
    progress: Math.min(100, Math.round(((xp - current) / (next - current)) * 100)),
  };
}

export function getDifficulty(index) {
  if (index <= 2) return { label: "Easy", className: "difficulty-easy" };
  if (index <= 5) return { label: "Intermediate", className: "difficulty-mid" };
  return { label: "Advanced", className: "difficulty-hard" };
}

export function getDailyChallenge(language = "javascript") {
  const bank = {
    python: {
      prompt: "What is the output?",
      code: "x = 10\nprint(x + 5)",
      answer: "15",
      explanation: "`x` stores 10, then Python prints 10 + 5.",
    },
    javascript: {
      prompt: "What is the output?",
      code: "const x = 10;\nconsole.log(x * 2);",
      answer: "20",
      explanation: "`x` stores 10, then JavaScript logs 10 multiplied by 2.",
    },
    c: {
      prompt: "What is printed?",
      code: "int a = 10;\nint b = 20;\nprintf(\"%d\", a + b);",
      answer: "30",
      explanation: "`printf` receives the sum of `a` and `b`.",
    },
    java: {
      prompt: "What is printed?",
      code: "int score = 7;\nSystem.out.println(score + 3);",
      answer: "10",
      explanation: "Java evaluates the integer addition before printing.",
    },
    default: {
      prompt: "Predict the output.",
      code: "value = 4\nvalue = value + 6\nprint(value)",
      answer: "10",
      explanation: "The variable is updated before it is printed.",
    },
  };
  return bank[language] || bank.default;
}

export function getBugFixChallenge(language = "javascript") {
  const bank = {
    python: {
      title: "Fix the missing colon",
      broken: "for i in range(5)\n    print(i)",
      fixed: "for i in range(5):\n    print(i)",
      choices: ["Missing colon", "Wrong variable name", "Invalid range"],
      answer: "Missing colon",
      explanation: "A Python `for` statement needs `:` before the indented block.",
    },
    javascript: {
      title: "Find the undefined value",
      broken: "const name = \"Mina\";\nconsole.log(age);",
      fixed: "const name = \"Mina\";\nconsole.log(name);",
      choices: ["Variable not defined", "Missing semicolon", "Wrong loop"],
      answer: "Variable not defined",
      explanation: "`age` was never declared. Log the existing `name` variable instead.",
    },
    default: {
      title: "Repair the reference",
      broken: "name = \"Mina\"\nprint(age)",
      fixed: "name = \"Mina\"\nprint(name)",
      choices: ["Variable not defined", "Bad indentation", "Missing import"],
      answer: "Variable not defined",
      explanation: "The code prints a variable that does not exist.",
    },
  };
  return bank[language] || bank.default;
}
