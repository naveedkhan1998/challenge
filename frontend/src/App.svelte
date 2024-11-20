<script lang="ts">
  import { Router, Route, Link } from 'svelte-routing';
  import { isAuthenticated } from './store';
  import Login from './routes/Login.svelte';
  import Registration from './routes/Registration.svelte';
  import Dashboard from './routes/Dashboard.svelte';
  import Profile from './routes/Profile.svelte';
  import Tickets from './routes/Tickets.svelte';

  let loggedIn = false;

  $: isAuthenticated.subscribe(value => {
    loggedIn = value || !!localStorage.getItem('token');
  });

  const logout = () => {
    localStorage.removeItem('token');
    isAuthenticated.set(false);
  };
</script>

<style>
  /* Global Reset and Base Styles */
  :root {
    --primary-color: #4c4c6d;
    --secondary-color: #282846;
    --background-color: #f8f9fa;
    --text-color: #333;
    --white: #ffffff;
    --transition-speed: 0.3s;
  }

  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Inter', 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    background: var(--background-color);
    color: var(--text-color);
    line-height: 1.6;
  }

  /* Navigation Styles */
  nav {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: var(--white);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  /* Navigation Links */
  .nav-container {
    display: flex;
    align-items: center;
    gap: 1.5rem;
  }

  .nav-links {
    display: flex;
    gap: 1rem;
  }

  .nav-links a {
    color: var(--white);
    text-decoration: none;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    transition: 
      background var(--transition-speed) ease,
      color var(--transition-speed) ease,
      transform var(--transition-speed) ease;
    position: relative;
    overflow: hidden;
  }

  .nav-links a::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.1);
    transition: var(--transition-speed);
  }

  .nav-links a:hover::before {
    left: 0;
  }

  .nav-links a:hover {
    transform: scale(1.05);
  }

  .nav-links a.active {
    background: var(--white);
    color: var(--primary-color);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  /* Logout Button */
  .logout-button {
    background: transparent;
    color: var(--white);
    border: 2px solid var(--white);
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    transition: 
      background var(--transition-speed) ease,
      color var(--transition-speed) ease,
      transform var(--transition-speed) ease;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .logout-button:hover {
    background: var(--white);
    color: var(--primary-color);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    nav {
      flex-direction: column;
      align-items: stretch;
      padding: 1rem;
    }

    .nav-container {
      flex-direction: column;
      gap: 1rem;
    }

    .nav-links {
      flex-direction: column;
      gap: 0.75rem;
    }

    .nav-links a, .logout-button {
      text-align: center;
      width: 100%;
    }
  }

  /* Additional Responsive Touches */
  @media (max-width: 480px) {
    nav {
      padding: 0.75rem;
    }

    .nav-links a {
      padding: 0.4rem 0.75rem;
    }
  }
</style>

<Router >
  <nav>
    <div class="nav-container">
      {#if loggedIn}
        <div class="nav-links">
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/profile">Profile</Link>
          <Link to="/tickets">Tickets</Link>
        </div>
        <button class="logout-button" on:click={logout}>Logout</button>
      {/if}
    </div>
  </nav>

  <Router>
    {#if loggedIn}
      <Route path="/dashboard" component={Dashboard} />
      <Route path="/profile" component={Profile} />
      <Route path="/tickets" component={Tickets} />
    {/if}

    <Route path="/" component={Login} />
    <Route path="/register" component={Registration} />

    {#if !loggedIn}
      <Route path="/dashboard" component={Login} />
      <Route path="/profile" component={Login} />
      <Route path="/tickets" component={Login} />
    {/if}
  </Router>
</Router>