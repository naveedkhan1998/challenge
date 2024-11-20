<script lang="ts">
    import { isAuthenticated } from '../store';
    import { apiFetch } from '../utils/api';
    import { navigate } from 'svelte-routing';
  
    // Enum for form modes
    const FormMode = {
      LOGIN: 'LOGIN',
      REGISTER: 'REGISTER'
    };
  
    // State variables
    let email: string = '';
    let password: string = '';
    let confirmPassword: string = '';
    let name: string = '';
    let errorMessage: string | null = null;
    let currentMode: typeof FormMode[keyof typeof FormMode] = FormMode.LOGIN;
  
    // Toggle between login and registration
    const toggleMode = () => {
      currentMode = currentMode === FormMode.LOGIN 
        ? FormMode.REGISTER 
        : FormMode.LOGIN;
      
      // Reset form and error message when switching
      email = '';
      password = '';
      confirmPassword = '';
      name = '';
      errorMessage = null;
    };
  
    // Handle login submission
    const handleLogin = async () => {
      try {
        const response = await apiFetch('/account/login/', {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        });
  
        if (response.token) {
          isAuthenticated.set(true);
          localStorage.setItem('token', response.token);
          navigate('/dashboard');
        }
      } catch (error) {
        errorMessage = error.message || 'Login failed.';
      }
    };
  
    // Handle registration submission
    const handleRegistration = async () => {
      // Basic password validation
      if (password !== confirmPassword) {
        errorMessage = 'Passwords do not match.';
        return;
      }
  
      try {
        const response = await apiFetch('/account/register/', {
          method: 'POST',
          body: JSON.stringify({ 
            email, 
            password, 
            password2:password,
            name,
            tc:true
          }),
        });
  
        if (response.token) {
          isAuthenticated.set(true);
          localStorage.setItem('token', response.token);
          navigate('/dashboard');
        }
      } catch (error) {
        errorMessage = error.message || 'Registration failed.';
      }
    };
  
    // Submission handler based on current mode
    const handleSubmit = () => {
      errorMessage = null;
      currentMode === FormMode.LOGIN 
        ? handleLogin() 
        : handleRegistration();
    };
  </script>
  
  <style>
    /* Design Tokens */
    :root {
      --primary-color: #4c4c6d;
      --secondary-color: #282846;
      --background-color: #f8f9fa;
      --text-color: #333;
      --white: #ffffff;
      --error-color: #dc3545;
      --transition-speed: 0.3s;
    }
  
    /* Container Styles */
    .auth-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: var(--background-color);
      padding: 1rem;
    }
  
    .auth-card {
      background: var(--white);
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
      width: 100%;
      max-width: 400px;
      padding: 2.5rem;
      transition: transform var(--transition-speed) ease;
    }
  
    .auth-card:hover {
      transform: translateY(-5px);
    }
  
    /* Form Styles */
    .auth-form {
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }
  
    .form-title {
      text-align: center;
      color: var(--primary-color);
      margin-bottom: 1.5rem;
      font-size: 2rem;
      font-weight: 700;
    }
  
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
  
    label {
      color: var(--text-color);
      font-weight: 500;
      transition: color var(--transition-speed) ease;
    }
  
    input {
      width: 100%;
      padding: 0.75rem;
      border: 2px solid #e0e0e0;
      border-radius: 8px;
      font-size: 1rem;
      transition: 
        border-color var(--transition-speed) ease,
        box-shadow var(--transition-speed) ease;
    }
  
    input:focus {
      outline: none;
      border-color: var(--primary-color);
      box-shadow: 0 0 0 3px rgba(76, 76, 109, 0.1);
    }
  
    .error-message {
      color: var(--error-color);
      text-align: center;
      margin-bottom: 1rem;
      font-weight: 500;
    }
  
    .submit-button {
      background: var(--primary-color);
      color: var(--white);
      border: none;
      padding: 0.75rem;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: 
        background var(--transition-speed) ease,
        transform var(--transition-speed) ease;
      text-transform: uppercase;
      letter-spacing: 1px;
    }
  
    .submit-button:hover {
      background: var(--secondary-color);
      transform: translateY(-2px);
    }
  
    .toggle-mode {
      text-align: center;
      margin-top: 1rem;
      color: var(--text-color);
    }
  
    .toggle-link {
      color: var(--primary-color);
      text-decoration: none;
      font-weight: 600;
      cursor: pointer;
      transition: color var(--transition-speed) ease;
    }
  
    .toggle-link:hover {
      color: var(--secondary-color);
      text-decoration: underline;
    }
  
    /* Responsive Adjustments */
    @media (max-width: 480px) {
      .auth-card {
        padding: 1.5rem;
        max-width: 100%;
      }
  
      .form-title {
        font-size: 1.5rem;
      }
    }
  </style>
  
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="form-title">
        {currentMode === FormMode.LOGIN ? 'Welcome Back' : 'Create Account'}
      </h1>
  
      {#if errorMessage}
        <p class="error-message">{errorMessage}</p>
      {/if}
  
      <form class="auth-form" on:submit|preventDefault={handleSubmit}>
        {#if currentMode === FormMode.REGISTER}
          <div class="form-group">
            <label for="name">Name</label>
            <input 
              id="name"
              type="text" 
              bind:value={name} 
              required 
              placeholder="Your Name"
            />
          </div>
        {/if}
  
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            id="email"
            type="email" 
            bind:value={email} 
            required 
            placeholder="Enter your email"
          />
        </div>
  
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            id="password"
            type="password" 
            bind:value={password} 
            required 
            placeholder="Enter your password"
            minlength="4"
          />
        </div>
  
        {#if currentMode === FormMode.REGISTER}
          <div class="form-group">
            <label for="confirm-password">Confirm Password</label>
            <input 
              id="confirm-password"
              type="password" 
              bind:value={confirmPassword} 
              required 
              placeholder="Confirm your password"
              minlength="4"
            />
          </div>
        {/if}
  
        <button type="submit" class="submit-button">
          {currentMode === FormMode.LOGIN ? 'Login' : 'Register'}
        </button>
      </form>
  
      <div class="toggle-mode">
        {#if currentMode === FormMode.LOGIN}
          Don't have an account? 
          <span class="toggle-link" on:click={toggleMode}>Register</span>
        {:else}
          Already have an account? 
          <span class="toggle-link" on:click={toggleMode}>Login</span>
        {/if}
      </div>
    </div>
  </div>