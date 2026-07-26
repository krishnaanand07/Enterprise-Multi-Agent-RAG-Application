import { useState, useEffect, useRef } from 'react';
import apiClient from '../api/client';

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await apiClient.post('/chat/generate', {
        message: userMessage,
        conversation_id: conversationId
      });
      
      if (!conversationId) {
        setConversationId(response.data.conversation_id);
      }
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.message,
        citations: response.data.citations,
        chart_data: response.data.chart_data,
        agent_used: response.data.agent_used
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto w-full">
      {/* ── Messages Area ────────────────────────────────── */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
        {/* Empty State */}
        {messages.length === 0 && !loading && (
          <div className="text-center mt-24 animate-fade-up">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-golden/10 mb-6">
              <svg className="w-8 h-8 text-golden" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
              </svg>
            </div>
            <h2 className="font-heading text-3xl font-bold text-dark mb-3">
              How can I help you<span className="text-golden">?</span>
            </h2>
            <p className="text-muted text-sm max-w-sm mx-auto leading-relaxed">
              Ask a question about your documents, request analytical database statistics, or generate custom data science visualizations.
            </p>
          </div>
        )}
        
        {/* Messages */}
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-up`}>
            <div className={`max-w-[85%] rounded-2xl p-4 sm:p-5 ${
              msg.role === 'user' 
                ? 'bg-forest text-cream-light rounded-br-md' 
                : 'bg-cream-light shadow-card border border-[rgba(0,0,0,0.06)] text-dark rounded-bl-md'
            }`}>
              <div className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</div>
              
              {/* Dynamic Data Science Chart Card */}
              {msg.role === 'assistant' && msg.chart_data && msg.chart_data.image && (
                <div className="mt-4 overflow-hidden rounded-xl border border-[rgba(49,74,53,0.14)] bg-cream p-4 shadow-sm transition-all hover:shadow-md">
                  <div className="flex items-center justify-between mb-3 border-b border-[rgba(0,0,0,0.06)] pb-2.5 flex-wrap gap-2">
                    <div className="flex items-center gap-2">
                      <span className="flex h-6 w-6 items-center justify-center rounded-lg bg-forest text-cream-light text-xs font-bold shadow-sm">
                        📊
                      </span>
                      <h4 className="font-heading text-base font-bold text-dark">
                        {msg.chart_data.title || "Analytical Data Chart"}
                      </h4>
                    </div>
                    <span className="text-[11px] font-semibold tracking-wider uppercase px-2.5 py-1 rounded-full bg-golden text-dark shadow-[0_1px_2px_rgba(0,0,0,0.08)]">
                      Data Science Execution
                    </span>
                  </div>
                  <div className="overflow-x-auto flex justify-center py-2 bg-cream-light/60 rounded-lg border border-[rgba(0,0,0,0.04)]">
                    <img
                      src={msg.chart_data.image}
                      alt={msg.chart_data.title || "Generated Chart"}
                      className="max-h-[360px] rounded-md object-contain transition-transform duration-300 hover:scale-[1.01]"
                    />
                  </div>
                </div>
              )}
              
              {/* Agent & Citation Metadata */}
              {msg.role === 'assistant' && (
                <div className="mt-4 pt-3 border-t border-[rgba(0,0,0,0.06)] text-xs flex flex-wrap justify-between items-center gap-2">
                  <span className="inline-flex items-center gap-1.5 bg-golden/15 text-dark px-2.5 py-1 rounded-full font-semibold">
                    <svg className="w-3 h-3 text-dark" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
                    </svg>
                    {msg.agent_used}
                  </span>
                  
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="flex gap-1.5 flex-wrap">
                      {msg.citations.map((cite, cidx) => (
                        <span key={cidx} className="cursor-help bg-accent-orange/15 text-accent-orange px-2 py-1 rounded-lg font-medium hover:bg-accent-orange/25 transition-colors" title={cite.chunk_text}>
                          [{cidx + 1}] {cite.document_name}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {/* Loading Indicator */}
        {loading && (
          <div className="flex justify-start animate-fade-up">
            <div className="bg-cream-light shadow-card border border-[rgba(0,0,0,0.06)] rounded-2xl rounded-bl-md p-5 flex gap-2 items-center">
              <div className="w-2 h-2 rounded-full bg-golden animate-bounce-gentle" />
              <div className="w-2 h-2 rounded-full bg-golden animate-bounce-gentle" style={{ animationDelay: '0.15s' }} />
              <div className="w-2 h-2 rounded-full bg-golden animate-bounce-gentle" style={{ animationDelay: '0.3s' }} />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* ── Input Bar ────────────────────────────────────── */}
      <div className="p-4 sm:p-6 pt-3 bg-cream border-t border-[rgba(0,0,0,0.06)]">
        <form onSubmit={handleSend} className="flex gap-3">
          <input
            type="text"
            className="flex-1 px-5 py-3.5 bg-forest border border-transparent shadow-sm rounded-full
                       text-cream-light text-sm font-body placeholder:text-cream/70
                       focus:outline-none focus:border-golden/50 focus:shadow-[0_0_0_3px_rgba(240,179,33,0.2)]
                       transition-all duration-300"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />
          <button 
            type="submit" 
            disabled={loading || !input.trim()}
            className="btn-primary px-6 py-3.5 rounded-full inline-flex items-center gap-2 text-sm"
          >
            <span className="hidden sm:inline">Send</span>
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
}
