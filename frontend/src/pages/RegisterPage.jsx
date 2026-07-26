import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import apiClient from '../api/client';

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    full_name: ''
  });
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await apiClient.post('/auth/register', formData);
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
    }
  };

  return (
    <div className="animate-stagger">
      {/* Header */}
      <div className="text-center mb-8">
        <h2 className="font-heading text-3xl font-bold text-dark mb-2">Create Account</h2>
        <p className="text-muted text-sm">Set up your research workspace</p>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-accent-orange/10 text-accent-orange p-3.5 rounded-xl mb-5 text-sm font-medium flex items-center gap-2">
          <svg className="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
          </svg>
          {typeof error === 'string' ? error : JSON.stringify(error)}
        </div>
      )}

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label className="block text-sm font-medium mb-2 text-dark/70">Email Address</label>
          <input 
            type="email" name="email"
            className="input-field"
            placeholder="you@example.com"
            value={formData.email} onChange={handleChange} required 
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2 text-dark/70">Username</label>
          <input 
            type="text" name="username"
            className="input-field"
            placeholder="johndoe"
            value={formData.username} onChange={handleChange} required minLength={3}
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2 text-dark/70">
            Full Name <span className="text-muted font-normal">(Optional)</span>
          </label>
          <input 
            type="text" name="full_name"
            className="input-field"
            placeholder="John Doe"
            value={formData.full_name} onChange={handleChange} 
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2 text-dark/70">Password</label>
          <input 
            type="password" name="password"
            className="input-field"
            placeholder="••••••••"
            value={formData.password} onChange={handleChange} required minLength={8}
          />
        </div>
        <button type="submit" className="btn-primary w-full text-center py-3 text-base mt-2">
          Create Account
        </button>
      </form>

      {/* Footer link */}
      <p className="mt-6 text-center text-sm text-muted">
        Already have an account?{' '}
        <Link to="/login" className="text-accent-orange hover:text-accent-orange-dark font-medium transition-colors">
          Sign in
        </Link>
      </p>
    </div>
  );
}
