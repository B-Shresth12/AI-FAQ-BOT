import { useState, useRef, useEffect } from "react";
import "./App.css";

type Role = "user" | "assistant";
interface Message {
  id: number;
  role: Role;
  text: string;
}

const FAQ: { question: string; answer: string }[] = [
  {
    question: "What is this AI assistant?",
    answer:
      "It's a tool that answers common questions instantly, trained on our product docs so you don't have to dig through help pages.",
  },
  {
    question: "Is my data used to train the model?",
    answer:
      "No. Conversations here are used only to answer your question in this session — nothing is stored for training.",
  },
  {
    question: "Can I talk to a human instead?",
    answer:
      "Yes — type 'talk to support' any time and we'll connect you with our team during business hours.",
  },
  {
    question: "How accurate are the answers?",
    answer:
      "Answers are drawn from our official docs and reviewed regularly, but always double-check anything critical against the source page.",
  },
];

let nextId = 1;

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  const respond = (question: string) => {
    const userMsg: Message = { id: nextId++, role: "user", text: question };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsThinking(true);

    const match = FAQ.find((f) =>
      f.question.toLowerCase().includes(question.toLowerCase().slice(0, 8)),
    );
    const answer =
      match?.answer ??
      "I don't have an exact answer for that yet, but try one of the suggested questions below.";

    window.setTimeout(() => {
      setIsThinking(false);
      setMessages((prev) => [
        ...prev,
        { id: nextId++, role: "assistant", text: answer },
      ]);
    }, 700);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isThinking) return;
    respond(input.trim());
  };

  return (
    <div className="chat-shell">
      <header className="chat-header">
        <span className="chat-header-dot" />
        <h1>AI FAQ</h1>
      </header>

      <div className="chat-body">
        {messages.length === 0 && (
          <div className="chat-empty">
            <h2>Ask me anything about the product</h2>
            <p>Or pick a common question to get started</p>
            <div className="chip-row">
              {FAQ.map((f) => (
                <button
                  key={f.question}
                  className="chip"
                  onClick={() => respond(f.question)}
                >
                  {f.question}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((m) => (
          <div key={m.id} className={`bubble-row ${m.role}`}>
            <div className={`bubble ${m.role}`}>{m.text}</div>
          </div>
        ))}

        {isThinking && (
          <div className="bubble-row assistant">
            <div className="bubble assistant thinking">
              <span className="dot" />
              <span className="dot" />
              <span className="dot" />
            </div>
          </div>
        )}

        <div ref={endRef} />
      </div>

      <form className="chat-input-bar" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
        />
        <button type="submit" disabled={!input.trim() || isThinking}>
          ↑
        </button>
      </form>
    </div>
  );
}

export default App;
