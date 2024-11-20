<script lang="ts">
    import { apiFetch } from '../utils/api';
  
    let email: string = '';
    let password: string = '';
    let message: string | null = null;
  
    const handleRegister = async () => {
      try {
        const response = await apiFetch('/auth/register', {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        });
  
        message = 'Registration successful!';
      } catch (error) {
        message = error.message || 'Registration failed.';
      }
    };
  </script>
  
  <h1>Register</h1>
  {#if message}
    <p>{message}</p>
  {/if}
  <form on:submit|preventDefault={handleRegister}>
    <label>Email</label>
    <input type="email" bind:value={email} required />
    <label>Password</label>
    <input type="password" bind:value={password} required />
    <button type="submit">Register</button>
  </form>
  