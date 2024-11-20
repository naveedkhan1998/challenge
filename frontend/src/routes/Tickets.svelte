<script lang="ts">
    import { apiFetch } from '../utils/api';
  
    let tickets: Array<{ id: number; title: string }> = [];
  
    const fetchTickets = async () => {
      try {
        tickets = await apiFetch('/tickets');
      } catch (error) {
        console.error(error.message);
      }
    };
  
    fetchTickets();
  </script>
  
  <h1>Tickets</h1>
  <ul>
    {#each tickets as ticket}
      <li>{ticket.title}</li>
    {/each}
  </ul>
  