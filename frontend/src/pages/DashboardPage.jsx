import { useState, useEffect } from 'react';
import apiClient from '../api/client';

export default function DashboardPage() {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const fetchDocuments = async () => {
    try {
      const res = await apiClient.get('/documents/');
      setDocuments(res.data);
    } catch (err) {
      console.error("Failed to fetch documents", err);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);
    setError(null);
    try {
      await apiClient.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      fetchDocuments(); // Refresh list
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed");
    } finally {
      setUploading(false);
      e.target.value = null; // reset input
    }
  };

  return (
    <div className="max-w-6xl mx-auto animate-fade-up">
      {/* ── Page Header ──────────────────────────────────── */}
      <div className="flex justify-between items-center mb-10">
        <div>
          <h1 className="font-heading text-4xl font-bold text-dark">Knowledge Base</h1>
          <p className="text-muted text-sm mt-1.5">Manage and organize your research documents</p>
        </div>
        
        <div>
          <input 
            type="file" 
            id="file-upload" 
            className="hidden" 
            accept=".pdf,.txt,.docx,.csv"
            onChange={handleFileUpload}
            disabled={uploading}
          />
          <label 
            htmlFor="file-upload" 
            className={`btn-primary inline-flex items-center gap-2 cursor-pointer ${uploading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
            </svg>
            {uploading ? 'Uploading...' : 'Upload Document'}
          </label>
        </div>
      </div>

      {/* ── Error ────────────────────────────────────────── */}
      {error && (
        <div className="bg-accent-orange/10 text-accent-orange p-4 rounded-xl mb-6 text-sm font-medium flex items-center gap-2">
          <svg className="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
          </svg>
          {error}
        </div>
      )}

      {/* ── Documents Table Card ─────────────────────────── */}
      <div className="bg-cream-light rounded-3xl shadow-card border border-[rgba(0,0,0,0.06)] overflow-hidden">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-[rgba(0,0,0,0.06)]">
              <th className="px-6 py-4 font-medium text-sm text-muted uppercase tracking-wider font-body">Filename</th>
              <th className="px-6 py-4 font-medium text-sm text-muted uppercase tracking-wider font-body">Type</th>
              <th className="px-6 py-4 font-medium text-sm text-muted uppercase tracking-wider font-body">Size</th>
              <th className="px-6 py-4 font-medium text-sm text-muted uppercase tracking-wider font-body">Status</th>
            </tr>
          </thead>
          <tbody>
            {documents.length === 0 ? (
              <tr>
                <td colSpan="4" className="px-6 py-16 text-center">
                  <div className="flex flex-col items-center gap-3">
                    <div className="w-14 h-14 rounded-2xl bg-golden/10 flex items-center justify-center">
                      <svg className="w-7 h-7 text-golden" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                      </svg>
                    </div>
                    <p className="text-muted text-sm">No documents found</p>
                    <p className="text-muted/60 text-xs">Upload your first PDF to get started</p>
                  </div>
                </td>
              </tr>
            ) : (
              documents.map(doc => (
                <tr key={doc.id} className="border-b border-[rgba(0,0,0,0.04)] last:border-0 hover:bg-cream-dark/40 transition-colors duration-300">
                  <td className="px-6 py-4 font-medium text-dark text-sm">{doc.original_filename}</td>
                  <td className="px-6 py-4 text-sm text-muted">
                    <span className="inline-flex items-center px-2.5 py-1 rounded-lg bg-forest/8 text-forest text-xs font-medium">
                      {doc.file_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-muted">{(doc.file_size / 1024 / 1024).toFixed(2)} MB</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold ${
                      doc.status === 'processed' ? 'bg-forest/10 text-forest' :
                      doc.status === 'processing' ? 'bg-golden/15 text-golden-dark' :
                      'bg-accent-orange/10 text-accent-orange'
                    }`}>
                      <span className={`w-1.5 h-1.5 rounded-full ${
                        doc.status === 'processed' ? 'bg-forest' :
                        doc.status === 'processing' ? 'bg-golden animate-pulse' :
                        'bg-accent-orange'
                      }`} />
                      {doc.status.charAt(0).toUpperCase() + doc.status.slice(1)}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
