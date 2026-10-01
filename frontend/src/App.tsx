import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";
import {
  chat,
  getMessagesofConversation,
  getConversations,
  type ConversationSummary,
} from "./Actions";
import Sidebar from "./Sidebar";

type Role = "user" | "assistant";
interface Message {
  id: number;
  role: Role;
  text: string;
}

const FAQ: { question: string }[] = [
  { question: "What is this AI assistant?" },
  { question: "Is my data used to train the model?" },
  { question: "Can I talk to a human instead?" },
  { question: "How accurate are the answers?" },
];

let nextId = 1;

const getConversationId = () => {
  return "faq-001";
};

const generateNewConversationId = () => {
  return crypto.randomUUID();
};

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [activeConversationId, setActiveConversationId] =
    useState<string>(getConversationId());
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isThinking]);

  // Load the list of conversations once on mount
  useEffect(() => {
    let cancelled = false;

    const loadConversations = async () => {
      try {
        const { conversations } = await getConversations();
        if (cancelled) return;
        setConversations(conversations);
      } catch (err) {
        console.error("failed to load conversations", err);
      }
    };

    loadConversations();

    return () => {
      cancelled = true;
    };
  }, []);

  // Load messages whenever the active conversation changes
  useEffect(() => {
    let cancelled = false;

    const loadHistory = async () => {
      try {
        const conversation =
          await getMessagesofConversation(activeConversationId);
        if (cancelled) return;

        const history: Message[] = conversation.messages
          .filter((m) => m.role === "user" || m.role === "assistant")
          .map((m) => ({
            id: nextId++,
            role: m.role as Role,
            text: m.content,
          }));

        setMessages(history);
      } catch (err) {
        console.error("failed to load conversation history", err);
      }
    };

    loadHistory();

    return () => {
      cancelled = true;
    };
  }, [activeConversationId]);

  const respond = async (question: string) => {
    const userMsg: Message = { id: nextId++, role: "user", text: question };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsThinking(true);

    try {
      const { answer } = await chat(activeConversationId, question);
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

  const handleNewChat = () => {
    setActiveConversationId(generateNewConversationId());
    setMessages([]);
    setInput("");
  };

  return (
    <div className="page">
      <Sidebar
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={setActiveConversationId}
        onNewChat={handleNewChat}
        collapsed={sidebarCollapsed}
        onToggleCollapsed={() => setSidebarCollapsed((prev) => !prev)}
      />

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
