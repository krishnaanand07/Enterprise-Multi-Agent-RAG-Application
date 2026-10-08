/* Chat System JS Module */
const chatService = {
  async getConversations() {
    return await apiRequest('/chat/conversations');
  },

  async createConversation(title = "New Chat") {
    return await apiRequest('/chat/conversations', {
      method: 'POST',
      body: JSON.stringify({ title })
    });
  },

  async getMessages(conversationId) {
    return await apiRequest(`/chat/conversations/${conversationId}/messages`);
  },

  async sendMessage(conversationId, content, selectedDocumentId = null) {
    return await apiRequest('/chat/messages', {
      method: 'POST',
      body: JSON.stringify({
        conversation_id: conversationId,
        content,
        selected_document_id: selectedDocumentId || null
      })
    });
  },

  async deleteConversation(conversationId) {
    return await apiRequest(`/chat/conversations/${conversationId}`, {
      method: 'DELETE'
    });
  }
};
