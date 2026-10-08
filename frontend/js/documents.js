/* Document Management & Real-time Stage Polling Module */
const documentService = {
  async getDocuments() {
    return await apiRequest('/documents');
  },

  async getDocument(docId) {
    return await apiRequest(`/documents/${docId}`);
  },

  async uploadDocument(file) {
    const formData = new FormData();
    formData.append('file', file);
    return await apiRequest('/documents/upload', {
      method: 'POST',
      body: formData
    });
  },

  async deleteDocument(docId) {
    return await apiRequest(`/documents/${docId}`, {
      method: 'DELETE'
    });
  }
};
