import React, { useState } from 'react';
import './App.css';

function App() {
  const [hardwareList, setHardwareList] = useState([
    { id: 1, name: 'Raspberry Pi 4', available: true },
    { id: 2, name: 'Arduino Uno', available: false },
    { id: 3, name: 'ESP32 Microcontroller', available: true },
    { id: 4, name: 'Jetson Nano', available: true },
  ]);

  const [selectedHardware, setSelectedHardware] = useState([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [loginNameInput, setLoginNameInput] = useState('');
  const [passwordInput, setPasswordInput] = useState('');

  // Handle hardware selection
  const handleSelection = (id) => {
    setSelectedHardware(prevSelected =>
      prevSelected.includes(id) ? prevSelected.filter(item => item !== id) : [...prevSelected, id]
    );
  };

  // Handle checkout
  const handleCheckout = () => {
    if (selectedHardware.length === 0) {
      alert("Please select at least one item to checkout.");
      return;
    }

    const checkedOutItems = hardwareList.filter(item => selectedHardware.includes(item.id));
    alert(`You have checked out: ${checkedOutItems.map(item => item.name).join(', ')}`);
    setSelectedHardware([]);
  };

  // Handle login submission
  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: loginNameInput, password: passwordInput }),
      });

      const data = await response.json();

      if (response.ok) {
        setUsername(loginNameInput);
        setIsLoggedIn(true);
        setShowLoginForm(false);
      } else {
        alert(data.message || 'Invalid login credentials');
      }
    } catch (error) {
      console.error('Error during login:', error);
      alert('An error occurred during login.');
    }
  };

  // Handle user registration
  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/add_user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: loginNameInput, password: passwordInput }),
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message || 'Registration successful');
        setLoginNameInput('');
        setPasswordInput('');
      } else {
        alert(data.message || 'Failed to register');
      }
    } catch (error) {
      console.error('Error during registration:', error);
      alert('An error occurred during registration.');
    }
  };

  // Handle logout
  const handleLogout = () => {
    setIsLoggedIn(false);
    setUsername('');
    setSelectedHardware([]);
    setLoginNameInput('');
    setPasswordInput('');
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Hardware Checkout</h1>
        
        <div className="user-login">
          {isLoggedIn ? (
            <div>
              <span>Welcome, {username}!</span>
              <button onClick={handleLogout} className="logout-button">Logout</button>
            </div>
          ) : (
            <button onClick={() => setShowLoginForm(!showLoginForm)} className="login-button">
              {showLoginForm ? 'Close Login/Register' : 'Login/Register'}
            </button>
          )}
        </div>

        {showLoginForm && (
          <div className="login-form">
            <form onSubmit={handleLoginSubmit}>
              <label>
                Username:
                <input
                  type="text"
                  value={loginNameInput}
                  onChange={(e) => setLoginNameInput(e.target.value)}
                />
              </label>
              <label>
                Password:
                <input
                  type="password"
                  value={passwordInput}
                  onChange={(e) => setPasswordInput(e.target.value)}
                />
              </label>
              <button type="submit">Login</button>
              <button type="button" onClick={handleRegisterSubmit}>Register</button>
            </form>
          </div>
        )}

        {isLoggedIn && (
          <>
            <p>Select hardware items you'd like to check out:</p>
            <div className="hardware-list">
              {hardwareList.map(item => (
                <div key={item.id} className={`hardware-item ${!item.available ? 'unavailable' : ''}`}>
                  <label>
                    <input
                      type="checkbox"
                      disabled={!item.available}
                      checked={selectedHardware.includes(item.id)}
                      onChange={() => handleSelection(item.id)}
                    />
                    {item.name} {item.available ? '(Available)' : '(Not Available)'}
                  </label>
                </div>
              ))}
            </div>

            <button onClick={handleCheckout} className="checkout-button">Checkout</button>
          </>
        )}

        {!isLoggedIn && <p>Please log in or register to select and check out hardware.</p>}
      </header>
    </div>
  );
}

export default App;
