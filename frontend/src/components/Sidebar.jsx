import './Sidebar.css';

export default function Sidebar({
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewConversation,
  onDeleteConversation,
}) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h1>Biais Detector Council</h1>
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
                  <div className="conversation-count">{conv.message_count}</div>
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
