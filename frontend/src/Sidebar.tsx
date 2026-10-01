import type { ConversationSummary } from "./Actions";

interface SidebarProps {
  conversations: ConversationSummary[];
  activeConversationId: string;
  onSelectConversation: (id: string) => void;
  onNewChat: () => void;
  collapsed: boolean;
  onToggleCollapsed: () => void;
}

function Sidebar({
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewChat,
  collapsed,
  onToggleCollapsed,
}: SidebarProps) {
  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : ""}`}>
      <div className="sidebar-top">
        <button
          className="sidebar-toggle"
          onClick={onToggleCollapsed}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          ☰
        </button>
        {!collapsed && (
          <div className="side-brand">
            <span className="chat-header-dot" />
            <span className="side-brand-label">AI FAQ</span>
          </div>
        )}
      </div>

      <button className="new-chat-btn" onClick={onNewChat}>
        <span className="new-chat-icon">+</span>
        {!collapsed && <span>New chat</span>}
      </button>

      {!collapsed && (
        <nav className="conversation-list">
          {conversations.length === 0 ? (
            <p className="conversation-empty">No conversations yet</p>
          ) : (
            <ul>
              {conversations.map((c) => (
                <li key={c.id}>
                  <button
                    className={`conversation-item ${
                      c.id === activeConversationId ? "active" : ""
                    }`}
                    onClick={() => onSelectConversation(c.id)}
                    title={c.id}
                  >
                    <span className="conversation-icon">💬</span>
                    <span className="conversation-label">{c.id}</span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </nav>
      )}

      {!collapsed && (
        <p className="side-footer">Available Monday–Friday, business hours</p>
      )}
    </aside>
  );
}

export default Sidebar;
