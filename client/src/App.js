import React, { useState } from 'react';
import './App.css';

function App() {
  // Sample data for available hardware
  const [hardwareList, setHardwareList] = useState([
    { id: 1, name: 'Raspberry Pi 4', available: true },
    { id: 2, name: 'Arduino Uno', available: false },
    { id: 3, name: 'ESP32 Microcontroller', available: true },
    { id: 4, name: 'Jetson Nano', available: true },
  ]);

  // State to track the user's selected hardware for checkout
  const [selectedHardware, setSelectedHardware] = useState([]);

  // State to track login status and user details
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [loginNameInput, setLoginNameInput] = useState('');

  // Handle selecting or deselecting hardware items
  const handleSelection = (id) => {
    if (selectedHardware.includes(id)) {
      setSelectedHardware(selectedHardware.filter(item => item !== id));
    } else {
      setSelectedHardware([...selectedHardware, id]);
    }
  };

  // Handle checkout submission
  const handleCheckout = () => {
    if (selectedHardware.length === 0) {
      alert("Please select at least one item to checkout.");
      return;
    }
    
    const checkedOutItems = hardwareList.filter(item => selectedHardware.includes(item.id));
    alert(`You have checked out: ${checkedOutItems.map(item => item.name).join(', ')}`);
    
    // Reset the selected hardware list
    setSelectedHardware([]);
  };

  // Handle login form submission
  const handleLoginSubmit = (e) => {
    e.preventDefault();
    setUsername(loginNameInput);
    setIsLoggedIn(true);
    setShowLoginForm(false);
  };

  // Handle logout
  const handleLogout = () => {
    setIsLoggedIn(false);
    setUsername('');
    setSelectedHardware([]);
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
              {showLoginForm ? 'Close Login' : 'Login'}
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
              <button type="submit">Login</button>
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

        {!isLoggedIn && <p>Please log in to select and check out hardware.</p>}
      </header>
    </div>
  );
}

export default App;
