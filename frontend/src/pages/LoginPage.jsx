import { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import apiClient from '../api/client';
import { AuthContext } from '../context/AuthContext';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await apiClient.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      
      login(response.data.access_token, response.data.user);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className="animate-stagger">
      {/* Header */}
      <div className="text-center mb-8">
        <h2 className="font-heading text-3xl font-bold text-dark mb-2">Welcome Back</h2>
        <p className="text-muted text-sm">Sign in to your research workspace</p>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-accent-orange/10 text-accent-orange p-3.5 rounded-xl mb-5 text-sm font-medium flex items-center gap-2">
          <svg className="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
          </svg>
          {error}
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm font-medium mb-2 text-dark/70">Email Address</label>
          <input 
            type="email" 
            className="input-field"
            placeholder="you@example.com"
            value={email} onChange={(e) => setEmail(e.target.value)} required 
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2 text-dark/70">Password</label>
          <input 
            type="password" 
            className="input-field"
            placeholder="••••••••"
            value={password} onChange={(e) => setPassword(e.target.value)} required 
          />
        </div>
        <button type="submit" className="btn-primary w-full text-center py-3 text-base mt-2">
          Sign In
        </button>
      </form>

      {/* Footer link */}
      <p className="mt-6 text-center text-sm text-muted">
        Don't have an account?{' '}
        <Link to="/register" className="text-accent-orange hover:text-accent-orange-dark font-medium transition-colors">
          Create account
        </Link>
      </p>
    </div>
  );
}
