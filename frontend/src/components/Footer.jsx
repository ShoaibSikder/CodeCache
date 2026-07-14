import { Link } from "react-router-dom";
import {
  Code2,
  Github,
  Linkedin,
  Instagram,
  Globe,
  Facebook,
  Mail,
  Home,
  Search,
  BookOpen,
  Brain,
} from "lucide-react";

const socialLinks = [
  {
    label: "GitHub",
    value: "github.com/ShoaibSikder",
    href: "https://github.com/ShoaibSikder",
    icon: Github,
  },
  {
    label: "LinkedIn",
    value: "linkedin.com/in/md-shoaib-sikder-232abb3b3",
    href: "https://www.linkedin.com/in/md-shoaib-sikder-232abb3b3/",
    icon: Linkedin,
  },
  {
    label: "Instagram",
    value: "instagram.com/shoaibsikder0",
    href: "https://www.instagram.com/shoaibsikder0",
    icon: Instagram,
  },
  {
    label: "Website",
    value: "shoaibsikderportfolio.vercel.app",
    href: "https://shoaibsikderportfolio.vercel.app",
    icon: Globe,
  },
  {
    label: "Facebook",
    value: "facebook.com/shoaib.sikder.35",
    href: "https://www.facebook.com/shoaib.sikder.35",
    icon: Facebook,
  },
  {
    label: "Email",
    value: "shoaibsikder0@gmail.com",
    href: "mailto:shoaibsikder0@gmail.com",
    icon: Mail,
  },
];

const readmeBadges = [
  ["React", "blue"],
  ["JavaScript", "yellow"],
  ["Python", "pink"],
  ["Django", "green"],
  ["Tailwind CSS", "cyan"],
  ["PostgreSQL", "orange"],
];

const footerLinks = [
  { label: "Home", to: "/", icon: Home },
  { label: "Browse Languages", to: "/#languages", icon: BookOpen },
  { label: "Search Snippets", to: "/search", icon: Search },
  { label: "Practice Quizzes", to: "/#languages", icon: Brain },
];

const badgeColors = {
  blue: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
  yellow:
    "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
  pink: "bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300",
  green: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
  cyan: "bg-cyan-100 text-cyan-800 dark:bg-cyan-900/30 dark:text-cyan-300",
  orange:
    "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300",
};

export default function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="mt-16 bg-card border-t border-border">
      <div className="container mx-auto max-w-[1800px] px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 mb-10">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2.5 mb-4">
              <div className="brand-mark w-8 h-8 bg-primary rounded-lg flex items-center justify-center shadow-sm">
                <Code2 className="h-4 w-4 text-primary-foreground" />
              </div>
              <div>
                <div className="text-base font-bold leading-tight">
                  <span>Code</span>
                  <span className="text-primary">Cache</span>
                </div>
                <div className="text-[10px] text-ink font-bold leading-none">
                  The Fastest Way to Recall Code
                </div>
              </div>
            </div>
            <p className="text-sm text-ink-soft leading-relaxed mb-5">
              Curated, editable code snippets for modern developers. Copy, run,
              and ship faster.
            </p>
            {/* Tech Badges */}
            <div className="flex flex-wrap gap-1.5">
              {readmeBadges.map(([name, color]) => (
                <span
                  key={name}
                  className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${badgeColors[color] || badgeColors.blue}`}
                >
                  {name}
                </span>
              ))}
            </div>
          </div>

          {/* Social Links */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-widest mb-4 text-foreground">
              Connect
            </h4>
            <ul className="space-y-2.5">
              {socialLinks.map((link) => (
                <li key={link.label}>
                  <a
                    href={link.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-2 text-sm text-ink-soft hover:text-primary transition-colors group"
                  >
                    <link.icon className="h-3.5 w-3.5" />
                    <span className="transition-transform">{link.label}</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-widest mb-4 text-foreground">
              Resources
            </h4>
            <ul className="space-y-2.5">
              {footerLinks.map((item) => (
                <li key={item.label}>
                  <Link
                    to={item.to}
                    className="text-sm text-ink-soft hover:text-primary transition-colors group inline-flex items-center gap-2"
                  >
                    <item.icon className="h-3.5 w-3.5 flex-shrink-0" />
                    <span className="transition-transform">{item.label}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Developer */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-widest mb-4 text-foreground">
              Developer
            </h4>
            <p className="text-sm text-ink-soft mb-3">
              Made with 💕 by{" "}
              <a
                href="https://shoaibsikderportfolio.vercel.app"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:underline font-medium"
              >
                @shoaibsikder
              </a>
            </p>
            <a
              href="https://shoaibsikderportfolio.vercel.app"
              target="_blank"
              rel="noopener noreferrer"
              className="action-pill action-pill-blue inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-100 hover:bg-blue-200 transition-all text-sm font-bold dark:bg-muted dark:hover:bg-primary dark:hover:text-primary-foreground"
            >
              <Globe className="h-4 w-4" />
              Visit Portfolio
            </a>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-6 border-t flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-xs text-ink-faint">
            &copy; {year} CodeCache. Built for future coders.
          </p>
        </div>
      </div>
    </footer>
  );
}

