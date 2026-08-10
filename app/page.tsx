"use client";

import { useEffect, useMemo, useRef, useState } from "react";

const STALL_AFTER_MS = 10_000;
const STORAGE_KEY = "unsaid-draft";

const paths = [
  {
    id: "facts",
    label: "what happened",
    questions: [
      "What happened, without explaining why?",
      "What is the one detail you keep circling around?",
      "What would a camera have recorded?",
    ],
  },
  {
    id: "feeling",
    label: "what I feel",
    questions: [
      "What feeling are you trying to make reasonable?",
      "Where do you feel this in your body?",
      "What feeling would be embarrassing to name here?",
    ],
  },
  {
    id: "want",
    label: "what I want",
    questions: [
      "What did you want to happen instead?",
      "If nobody judged the answer, what would you ask for?",
      "What do you wish the other person understood without being told?",
    ],
  },
  {
    id: "admit",
    label: "what I won't admit",
    questions: [
      "What are you avoiding because it sounds harsh, needy, or selfish?",
      "Write the sentence you would delete before anyone saw it.",
      "What do you already know but keep negotiating with?",
    ],
  },
  {
    id: "next",
    label: "what comes next",
    questions: [
      "If nothing changes, what happens next?",
      "What is the smallest honest thing you could do now?",
      "Which decision are you postponing by thinking about it?",
    ],
  },
] as const;

type PathId = (typeof paths)[number]["id"];

export default function Home() {
  const [text, setText] = useState("");
  const [hydrated, setHydrated] = useState(false);
  const [stalled, setStalled] = useState(false);
  const [question, setQuestion] = useState<string | null>(null);
  const [selectedPath, setSelectedPath] = useState<PathId | null>(null);
  const lastQuestion = useRef<Record<string, number>>({});

  useEffect(() => {
    const frame = window.requestAnimationFrame(() => {
      setText(window.localStorage.getItem(STORAGE_KEY) ?? "");
      setHydrated(true);
    });
    return () => window.cancelAnimationFrame(frame);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    window.localStorage.setItem(STORAGE_KEY, text);
  }, [hydrated, text]);

  useEffect(() => {
    if (!hydrated || text.trim().length < 12 || stalled) return;
    const timer = window.setTimeout(() => setStalled(true), STALL_AFTER_MS);
    return () => window.clearTimeout(timer);
  }, [hydrated, stalled, text]);

  const wordCount = useMemo(
    () => (text.trim() ? text.trim().split(/\s+/).length : 0),
    [text],
  );

  function handleChange(value: string) {
    setText(value);
    setStalled(false);
    setQuestion(null);
    setSelectedPath(null);
  }

  function choosePath(pathId: PathId) {
    const path = paths.find((item) => item.id === pathId);
    if (!path) return;
    const previous = lastQuestion.current[pathId] ?? -1;
    const next = (previous + 1) % path.questions.length;
    lastQuestion.current[pathId] = next;
    setSelectedPath(pathId);
    setQuestion(path.questions[next]);
  }

  function dismissPrompt() {
    setStalled(false);
    setQuestion(null);
    setSelectedPath(null);
  }

  return (
    <main className={`journal-shell ${stalled ? "is-stalled" : ""}`}>
      <header className="topbar">
        <div className="wordmark">UNSAID<span className="wordmark-dot">.</span></div>
        <div className="privacy-note">
          <span className="privacy-light" aria-hidden="true" />
          stays in this browser
        </div>
      </header>

      <section className="writing-space" aria-label="Private journal editor">
        <div className="session-line">
          <span>{wordCount} {wordCount === 1 ? "word" : "words"}</span>
          <span className="session-state">
            {stalled ? "thought paused" : "keep moving"}
          </span>
        </div>

        <textarea
          aria-label="Journal entry"
          className="editor"
          value={text}
          onChange={(event) => handleChange(event.target.value)}
          placeholder="Write the sentence you keep avoiding."
          spellCheck="true"
        />
      </section>

      <aside className="intervention" aria-live="polite" aria-hidden={!stalled}>
        <div className="intervention-header">
          <p className="eyebrow">You stopped.</p>
          <button type="button" className="dismiss" onClick={dismissPrompt}>
            I know what to write
          </button>
        </div>

        {!question ? (
          <>
            <h1>Where did the thought get stuck?</h1>
            <div className="path-grid">
              {paths.map((path, index) => (
                <button
                  type="button"
                  className="path-button"
                  key={path.id}
                  onClick={() => choosePath(path.id)}
                >
                  <span>0{index + 1}</span>
                  {path.label}
                </button>
              ))}
            </div>
          </>
        ) : (
          <div className="question-card">
            <p>{paths.find((path) => path.id === selectedPath)?.label}</p>
            <h1>{question}</h1>
            <span>Start typing. The question will get out of the way.</span>
          </div>
        )}
      </aside>

      <footer className="footer-note">No analysis. No account. No cloud.</footer>
    </main>
  );
}
