<script lang="ts">
    import { apiFetch } from '../utils/api';
  
    let user: { email: string; name: string } | null = null;
  
    const fetchProfile = async () => {
      try {
        user = await apiFetch('/auth/profile');
      } catch (error) {
        console.error(error.message);
      }
    };
  
    fetchProfile();
  </script>
  
  <h1>Profile</h1>
  {#if user}
    <p>Email: {user.email}</p>
    <p>Name: {user.name}</p>
  {:else}
    <p>Loading...</p>
  {/if}
  