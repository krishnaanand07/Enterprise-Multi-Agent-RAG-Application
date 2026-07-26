import { useState, useEffect } from 'react';
import apiClient from '../api/client';

const StepItem = ({ label, isActive, isDone }) => (
  <div className={`flex items-center gap-3 text-sm ${isActive ? 'text-dark font-medium' : isDone ? 'text-forest font-medium' : 'text-muted'}`}>
    <div className={`w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 ${isActive ? 'bg-golden text-white animate-pulse' : isDone ? 'bg-forest text-white' : 'bg-[rgba(0,0,0,0.05)]'}`}>
      {isDone ? (
        <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
      ) : isActive ? (
        <div className="w-1.5 h-1.5 rounded-full bg-white"></div>
      ) : null}
    </div>
    {label}
  </div>
);

export default function DashboardPage() {
  const [documents, setDocuments] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [currentUploadDoc, setCurrentUploadDoc] = useState(null);

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

  useEffect(() => {
    let intervalId;
    
    if (currentUploadDoc && currentUploadDoc.id) {
      const updatedDoc = documents.find(d => d.id === currentUploadDoc.id);
      if (updatedDoc && updatedDoc.status !== currentUploadDoc.status) {
        setCurrentUploadDoc(updatedDoc);
        if (updatedDoc.status === 'processed' || updatedDoc.status === 'failed') {
          setTimeout(() => setCurrentUploadDoc(null), 4000); // Clear after 4 seconds of completion
        }
      }
    }

    const hasPendingDocuments = documents.some(doc => !['processed', 'failed'].includes(doc.status));
    if (hasPendingDocuments) {
      intervalId = setInterval(() => {
        fetchDocuments();
      }, 2000);
    }
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [documents, currentUploadDoc]);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);
    setError(null);
    setUploadProgress(0);
    setCurrentUploadDoc({ original_filename: file.name, status: 'uploading' });
    
    try {
      const res = await apiClient.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(percentCompleted);
        }
      });
      setCurrentUploadDoc(res.data.document);
      fetchDocuments(); // Refresh list immediately to get new document
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed");
      setCurrentUploadDoc(null);
    } finally {
      setUploading(false);
      e.target.value = null; // reset input
    }
  };

  const handleDeleteDocument = async (docId) => {
    if (!window.confirm("Are you sure you want to delete this document? This will remove it from the database and AI knowledge base.")) return;
    
    try {
      await apiClient.delete(`/documents/${docId}`);
      fetchDocuments(); // refresh list
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to delete document");
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

      {/* ── Upload Progress Widget ─────────────────────────── */}
      {currentUploadDoc && (
        <div className="bg-cream-light border border-[rgba(0,0,0,0.06)] shadow-sm rounded-2xl p-6 mb-6 animate-fade-in">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-dark font-semibold text-sm">Processing: {currentUploadDoc.original_filename}</h3>
            {uploadProgress < 100 && currentUploadDoc.status === 'uploading' && <span className="text-xs font-medium text-muted">{uploadProgress}%</span>}
          </div>
          
          {/* Upload Progress Bar */}
          {currentUploadDoc.status === 'uploading' && (
            <div className="mb-6">
              <div className="w-full bg-[rgba(0,0,0,0.04)] rounded-full h-1.5 overflow-hidden">
                <div className="bg-forest h-1.5 rounded-full transition-all duration-300" style={{ width: `${uploadProgress}%` }}></div>
              </div>
            </div>
          )}

          {/* Steps */}
          <div className="space-y-3">
             <StepItem label="Uploading File" isActive={currentUploadDoc.status === 'uploading'} isDone={currentUploadDoc.status !== 'uploading'} />
             <StepItem label="Extracting Text" isActive={currentUploadDoc.status === 'extracting' || currentUploadDoc.status === 'processing'} isDone={['chunking', 'embedding', 'processed'].includes(currentUploadDoc.status)} />
             <StepItem label="Chunking Content" isActive={currentUploadDoc.status === 'chunking'} isDone={['embedding', 'processed'].includes(currentUploadDoc.status)} />
             <StepItem label="Creating Embeddings" isActive={currentUploadDoc.status === 'embedding'} isDone={currentUploadDoc.status === 'processed'} />
          </div>
        </div>
      )}

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
              <th className="px-6 py-4 font-medium text-sm text-muted uppercase tracking-wider font-body text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {documents.length === 0 ? (
              <tr>
                <td colSpan="5" className="px-6 py-16 text-center">
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
                      ['processing', 'extracting', 'chunking', 'embedding'].includes(doc.status) ? 'bg-golden/15 text-golden-dark' :
                      'bg-accent-orange/10 text-accent-orange'
                    }`}>
                      <span className={`w-1.5 h-1.5 rounded-full ${
                        doc.status === 'processed' ? 'bg-forest' :
                        ['processing', 'extracting', 'chunking', 'embedding'].includes(doc.status) ? 'bg-golden animate-pulse' :
                        'bg-accent-orange'
                      }`} />
                      {doc.status.charAt(0).toUpperCase() + doc.status.slice(1)}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button 
                      onClick={() => handleDeleteDocument(doc.id)}
                      className="p-2 text-muted hover:text-accent-orange bg-transparent hover:bg-accent-orange/10 rounded-xl transition-colors duration-200"
                      title="Delete document"
                    >
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                      </svg>
                    </button>
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
