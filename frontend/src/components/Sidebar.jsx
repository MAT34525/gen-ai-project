import './Sidebar.css';

export default function Sidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
  onDeleteConversation,
  theme,
  onToggleTheme,
}) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-title-row">
          <h1>LLM Council</h1>
          <button
            type="button"
            className="theme-toggle"
            onClick={onToggleTheme}
          >
            {theme === 'dark' ? 'Light' : 'Dark'}
          </button>
        </div>
        <button className="new-conversation-btn" onClick={onNewConversation}>
          + New Conversation
        </button>
      </div>

      <div className="conversation-list">
        {conversations.length === 0 ? (
          <div className="no-conversations">No conversations yet</div>
        ) : (
          conversations.map((conv) => (
            <div
              key={conv.id}
              className={`conversation-item ${
                conv.id === currentConversationId ? 'active' : ''
              }`}
              onClick={() => onSelectConversation(conv.id)}
            >
              <div className="conversation-title-row">
                <div className="conversation-title">
                  {conv.title || 'New Conversation'}
                </div>
                <div className="conversation-actions">
                  <button
                    type="button"
                    className="delete-conv-btn"
                    onClick={(event) => {
                      event.stopPropagation();
                      onDeleteConversation(conv.id);
                    }}
                    aria-label="Delete conversation"
                  >
                    Delete
                  </button>
                </div>
              </div>
              <div className="conversation-meta">
                {conv.message_count} messages
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
