// LoginForm.js
import React, { useState } from 'react';

const API_BASE_URL = 'http://127.0.0.1:5001';

function LoginForm({ onLoginSuccess, showLoginForm, setShowLoginForm }) {
  const [loginNameInput, setLoginNameInput] = useState('');
  const [passwordInput, setPasswordInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log('Attempting login...');
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          username: loginNameInput,
          password: passwordInput,
          userId: loginNameInput,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Login response:', data);

      if (data.success) {
        onLoginSuccess({
          username: data.username,
          userId: data.userId,
        });
        setShowLoginForm(false);
        setLoginNameInput('');
        setPasswordInput('');
        setError('');
      } else {
        setError(data.message || 'Login failed');
      }
    } catch (err) {
      console.error('Error during login:', err);
      setError('Error connecting to server: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log('Attempting registration...');
      const response = await fetch(`${API_BASE_URL}/add_user`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({
          username: loginNameInput,
          password: passwordInput,
          userId: loginNameInput,
        }),
      });

      const data = await response.json();
      console.log('Registration response:', data);

      if (data.success) {
        alert('Registration successful! Please login.');
        setLoginNameInput('');
        setPasswordInput('');
        setError('');
      } else {
        setError(data.message);
      }
    } catch (err) {
      console.error('Error during registration:', err);
      setError('Error connecting to server: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    showLoginForm && (
      <div className="login-form">
        {error && <div className="error-message">{error}</div>}
        <form onSubmit={handleLoginSubmit}>
          <div className="form-group">
            <label>Username:</label>
            <input
              type="text"
              value={loginNameInput}
              onChange={(e) => setLoginNameInput(e.target.value)}
              disabled={loading}
              required
            />
          </div>
          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              value={passwordInput}
              onChange={(e) => setPasswordInput(e.target.value)}
              disabled={loading}
              required
            />
          </div>
          <div className="form-buttons">
            <button type="submit" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </button>
            <button
              type="button"
              onClick={handleRegisterSubmit}
              disabled={loading}
            >
              {loading ? 'Registering...' : 'Register'}
            </button>
          </div>
        </form>
      </div>
    )
  );
}

export default LoginForm;
