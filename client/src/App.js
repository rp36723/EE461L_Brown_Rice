import React, { useState, useEffect } from 'react';
import './App.css';
import ProjectDetails from './components/ProjectDetails';


const API_BASE_URL = 'http://127.0.0.1:5001';

function App() {
  // State management
  const [hardwareList, setHardwareList] = useState([]);
  const [selectedHardware, setSelectedHardware] = useState({});
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [userId, setUserId] = useState('');
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [loginNameInput, setLoginNameInput] = useState('');
  const [passwordInput, setPasswordInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const [showCreateProject, setShowCreateProject] = useState(false);
  const [newProjectData, setNewProjectData] = useState({
    projectName: '',
    projectId: '',
    description: ''
  });
  const [successMessage, setSuccessMessage] = useState('');


  // Fetch hardware sets on component mount
  useEffect(() => {
    fetchHardwareSets();
  }, []);

  // Fetch user's projects when logged in
  useEffect(() => {
    if (isLoggedIn && userId) {
      fetchUserProjects();
    }
  }, [isLoggedIn, userId]);

  useEffect(() => {
    if (successMessage) {
        const timer = setTimeout(() => setSuccessMessage(''), 3000);
        return () => clearTimeout(timer);
    }
  }, [successMessage]);

  useEffect(() => {
    if (error) {
        const timer = setTimeout(() => setError(''), 5000);
        return () => clearTimeout(timer);
    }
  }, [error]);

  const fetchHardwareSets = async () => {
    try {
      console.log('Fetching hardware sets...');
      const response = await fetch(`${API_BASE_URL}/get_hardware_sets`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Hardware sets data:', data);

      if (data.success) {
        setHardwareList(data.hardware_sets);
        setError('');
      } else {
        setError(data.message || 'Failed to fetch hardware sets');
      }
    } catch (err) {
      console.error('Error fetching hardware sets:', err);
      setError('Error connecting to server: ' + err.message);
    }
  };

  const fetchUserProjects = async () => {
    try {
        console.log('Fetching user projects for userId:', userId);
        const response = await fetch(`${API_BASE_URL}/get_user_projects?userId=${userId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('User projects data:', data);

        if (data.success) {
            setProjects(data.projects);
            console.log('Projects set to:', data.projects);
            setError('');
        } else {
            setError(data.message || 'Failed to fetch projects');
        }
    } catch (err) {
        console.error('Error fetching projects:', err);
        setError('Error connecting to server: ' + err.message);
    }
};

  const handleCreateProject = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccessMessage('');

    // Basic validation
    if (newProjectData.projectId.length < 3) {
        setError('Project ID must be at least 3 characters long');
        setLoading(false);
        return;
    }

    // Prevent special characters in Project ID
    if (!/^[a-zA-Z0-9-_]+$/.test(newProjectData.projectId)) {
        setError('Project ID can only contain letters, numbers, hyphens, and underscores');
        setLoading(false);
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/create_project`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                ...newProjectData,
                userId: userId
            }),
        });

        const data = await response.json();

        if (data.success) {
            setSuccessMessage('Project created successfully!');
            setShowCreateProject(false);
            setNewProjectData({ projectName: '', projectId: '', description: '' });
            await fetchUserProjects();
            setSelectedProject(newProjectData.projectId);  
        } else {
            setError(data.message || 'Failed to create project');
        }
    } catch (err) {
        setError('Failed to create project: ' + (err.message || 'Unknown error'));
    } finally {
        setLoading(false);
        // Clear success message after 3 seconds
        if (successMessage) {
            setTimeout(() => setSuccessMessage(''), 3000);
        }
    }
};

// Add these new states at the top of App.js with other states
const [showJoinProject, setShowJoinProject] = useState(false);
const [joinProjectId, setJoinProjectId] = useState('');

// Add this new handler function
const handleJoinProject = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError('');
  setSuccessMessage('');

  try {
      const response = await fetch(`${API_BASE_URL}/join_project`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
          },
          body: JSON.stringify({
              projectId: joinProjectId,
              userId: userId
          }),
      });

      const data = await response.json();

      if (data.success) {
          setSuccessMessage('Successfully joined project!');
          setJoinProjectId('');
          setShowJoinProject(false);
          await fetchUserProjects();
          setSelectedProject(joinProjectId);  
      } else {
          setError(data.message);
      }
  } catch (err) {
      console.error('Error joining project:', err);
      setError('Failed to join project: ' + err.message);
  } finally {
      setLoading(false);
      // Clear success message after 3 seconds
      if (successMessage) {
          setTimeout(() => setSuccessMessage(''), 3000);
      }
  }
};



  const handleCheckout = async () => {
    if (!selectedProject) {
      setError("Please select a project first");
      return;
    }
    if (Object.keys(selectedHardware).length === 0) {
      setError("Please select at least one item to checkout");
      return;
    }

    setLoading(true);
    setError('');

    try {
      console.log('Processing checkout...');
      for (const [hwSetName, quantity] of Object.entries(selectedHardware)) {
        if (quantity > 0) {
          const response = await fetch(`${API_BASE_URL}/check_out`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json'
            },
            body: JSON.stringify({
              projectId: selectedProject,
              hwSetName,
              quantity,
              userId
            }),
          });

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const data = await response.json();
          console.log('Checkout response:', data);

          if (!data.success) {
            throw new Error(data.message || 'Checkout failed');
          }
        }
      }

      setSelectedHardware({});
      await fetchHardwareSets();
      await fetchUserProjects();
      setError('');
    } catch (err) {
      console.error('Error during checkout:', err);
      setError('Checkout failed: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

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
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          username: loginNameInput,
          password: passwordInput,
          userId: loginNameInput
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Login response:', data);

      if (data.success) {
        setUsername(data.username);
        setUserId(data.userId);
        setIsLoggedIn(true);
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
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          username: loginNameInput,
          password: passwordInput,
          userId: loginNameInput
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

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUsername('');
    setUserId('');
    setSelectedHardware({});
    setSelectedProject(null);
    setProjects([]);
    setError('');
  };

  // The JSX return remains the same
  return (
    <div className="App">
      <header className="App-header">
              <h1 className="title">Brown Rice</h1>
              
              <div className="notification-container">
                  {error && <div className="error-message">{error}</div>}
                  {successMessage && <div className="success-message">{successMessage}</div>}
              </div>
        
        <div className="user-login">
          {isLoggedIn ? (
            <div>
              <span>Welcome, {username}!</span>
              <button onClick={handleLogout} className="logout-button">
                Logout
              </button>
            </div>
          ) : (
            <button 
              onClick={() => setShowLoginForm(!showLoginForm)} 
              className="login-button"
            >
              {showLoginForm ? 'Close' : 'Login/Register'}
            </button>
          )}
        </div>

        {showLoginForm && !isLoggedIn && (
          <div className="login-form">
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
        )}

        {isLoggedIn && (
          <div className="main-content">
<div className="projects-section">
    <div className="projects-header">
        <h2>Projects</h2>
        <div className="project-actions">
            <button onClick={() => {
                setShowCreateProject(false);
                setShowJoinProject(false);
                setSelectedProject(null);
            }}>
                View All Projects
            </button>
            <button onClick={() => setShowCreateProject(!showCreateProject)}>
                {showCreateProject ? 'Cancel' : 'Create New Project'}
            </button>
            <button onClick={() => setShowJoinProject(!showJoinProject)}>
                {showJoinProject ? 'Cancel' : 'Join Existing Project'}
            </button>
        </div>
    </div>

    {!showCreateProject && !showJoinProject && (
        <div className="projects-list">
            {projects.length > 0 ? (
                projects.map(project => (
                    <div 
                        key={project.projectId} 
                        className={`project-item ${selectedProject === project.projectId ? 'selected' : ''}`}
                        onClick={() => setSelectedProject(project.projectId)}
                    >
                        <h3>{project.projectName}</h3>
                        <p>{project.description}</p>
                        <p className="project-id">Project ID: {project.projectId}</p>
                    </div>
                ))
            ) : (
                <p className="no-projects-message">No projects yet. Create or join a project to get started!</p>
            )}
        </div>
    )}

    {showJoinProject && (
        <form onSubmit={handleJoinProject} className="join-project-form">
            <input
                type="text"
                placeholder="Enter Project ID"
                value={joinProjectId}
                onChange={(e) => setJoinProjectId(e.target.value)}
                required
            />
            <button type="submit" disabled={loading}>
                {loading ? 'Joining...' : 'Join Project'}
            </button>
        </form>
    )}

    {showCreateProject && (
        <form onSubmit={handleCreateProject} className="create-project-form">
            <input
                type="text"
                placeholder="Project Name"
                value={newProjectData.projectName}
                onChange={(e) => setNewProjectData(prev => ({
                    ...prev,
                    projectName: e.target.value
                }))}
                required
            />
            <input
                type="text"
                placeholder="Project ID"
                value={newProjectData.projectId}
                onChange={(e) => setNewProjectData(prev => ({
                    ...prev,
                    projectId: e.target.value
                }))}
                required
            />
            <textarea
                placeholder="Project Description"
                value={newProjectData.description}
                onChange={(e) => setNewProjectData(prev => ({
                    ...prev,
                    description: e.target.value
                }))}
            />
            <button type="submit" disabled={loading}>
                {loading ? 'Creating...' : 'Create Project'}
            </button>
        </form>
    )}
            


            </div>

            {selectedProject && projects.find(p => p.projectId === selectedProject) && (
              <ProjectDetails 
                project={projects.find(p => p.projectId === selectedProject)}
              />
            )}

            {selectedProject && (
              <div className="hardware-section">
                <h2>Available Hardware</h2>
                <div className="hardware-list">
                  {hardwareList.map(hw => (
                    <div key={hw.hwName} className="hardware-item">
                      <h3>{hw.hwName}</h3>
                      <p>Available: {hw.availability} / {hw.capacity}</p>
                      <div className="quantity-selector">
                        <label>Quantity:</label>
                        <input
                          type="number"
                          min="0"
                          max={hw.availability}
                          value={selectedHardware[hw.hwName] || 0}
                          onChange={(e) => {
                            const value = Math.min(
                              Math.max(0, parseInt(e.target.value) || 0),
                              hw.availability
                            );
                            setSelectedHardware(prev => ({
                              ...prev,
                              [hw.hwName]: value
                            }));
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
                
                <div className="action-buttons">
                  <button 
                    onClick={handleCheckout}
                    disabled={loading || Object.keys(selectedHardware).length === 0}
                    className="checkout-button"
                  >
                    {loading ? 'Processing...' : 'Checkout Hardware'}
                  </button>
                </div>
              </div>
            )}

            {!selectedProject && (
              <div className="no-project-selected">
                <p>Please select or create a project to checkout hardware.</p>
              </div>
            )}
          </div>
        )}

        {!isLoggedIn && (
          <div className="welcome-message">
            <p>Please log in or register to manage projects and hardware.</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;