import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";
import { chat } from "./Actions";

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

const getConversationId = () => {
  // const existing = sessionStorage.getItem("conversation_id");
  // if (existing) return existing;
  // const id = crypto.randomUUID();
  // sessionStorage.setItem("conversation_id", id);
  // return id;
  return "faq-001";
};

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);
  const conversationIdRef = useRef<string>(getConversationId());

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  const respond = async (question: string) => {
    const userMsg: Message = { id: nextId++, role: "user", text: question };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsThinking(true);

    try {
      const { answer } = await chat(conversationIdRef.current, question);
      setMessages((prev) => [
        ...prev,
        { id: nextId++, role: "assistant", text: answer },
      ]);
    } catch (err) {
      console.error("chat request failed", err);
      setMessages((prev) => [
        ...prev,
        {
          id: nextId++,
          role: "assistant",
          text: "Something went wrong reaching the assistant. Please try again.",
        },
      ]);
    } finally {
      setIsThinking(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isThinking) return;
    respond(input.trim());
  };

  return (
    <div className="page">
      <aside className="side-panel">
        <div className="side-content">
          <div className="side-brand">
            <span className="chat-header-dot" />
            <span className="side-brand-label">AI FAQ</span>
          </div>

          <h1 className="side-title">
            Ask anything.
            <br />
            Get answers instantly.
          </h1>
          <p className="side-desc">
            This assistant is trained on our product docs so you can get
            straight answers without digging through help pages.
          </p>

          <ul className="side-features">
            <li>
              <span className="feature-dot" />
              Answers grounded in official documentation
            </li>
            <li>
              <span className="feature-dot" />
              Nothing you type here is used for training
            </li>
            <li>
              <span className="feature-dot" />
              Hand off to a human whenever you need to
            </li>
          </ul>
        </div>

        <p className="side-footer">Available Monday–Friday, business hours</p>
      </aside>

      <main className="chat-shell">
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
              <div className={`bubble ${m.role}`}>
                {m.role === "assistant" ? (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {m.text}
                  </ReactMarkdown>
                ) : (
                  m.text
                )}
              </div>
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
      </main>
    </div>
  );
}

export default App;
