<script lang="ts">
    import { apiFetch } from '../utils/api';
  
    interface User {
        id: number;
        email: string;
        name: string;
        avatar: string;
        is_admin: boolean;
        auth_provider: string;
    }

    interface Ticket {
        id: number;
        title: string;
        description: string;
        priority: string;
        status: string;
        date_created: string;
        date_updated: string;
        assigned_to: number | null;
        assigned_to_username: string | null;
    }
  
    let user: User | null = null;
    let tickets: Ticket[] = [];
    let loading = true;
    let error: string | null = null;
  
    const fetchProfile = async () => {
        try {
            user = await apiFetch('/account/profile');
            await fetchTickets();
            loading = false;
        } catch (err) {
            error = err.message;
            loading = false;
        }
    };

    const fetchTickets = async () => {
        if (!user) return;
        try {
            const params = new URLSearchParams();
            params.append('assigned_to', String(user.id));
            const url = `/ticket/tickets/?${params.toString()}`;
            tickets = await apiFetch(url);
        } catch (err) {
            error = err.message;
        }
    };
  
    fetchProfile();
</script>

<style>
    .profile-container {
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: #f9f9f9;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .profile-header {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 1rem;
    }

    .avatar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1.5rem;
        border: 3px solid #007bff;
    }

    .user-info {
        flex-grow: 1;
    }

    .user-name {
        font-size: 1.8rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }

    .user-email {
        color: #666;
        font-size: 1rem;
    }

    .profile-details {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
    }

    .detail-item {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .detail-label {
        font-weight: bold;
        color: #555;
        margin-bottom: 0.5rem;
        display: block;
    }

    .detail-value {
        color: #333;
    }

    .admin-badge {
        background-color: #007bff;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }

    .loading, .error {
        text-align: center;
        padding: 2rem;
        color: #666;
    }

    .error {
        color: #dc3545;
    }
    .tickets-section {
        margin-top: 2rem;
    }

    .ticket-item {
        background-color: #fff;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .ticket-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }

    .ticket-status {
        font-size: 0.9rem;
        color: #666;
    }
</style>

{#if loading}
    <div class="loading">
        <p>Loading profile...</p>
    </div>
{:else if error}
    <div class="error">
        <p>Error: {error}</p>
    </div>
{:else if user}
    <div class="profile-container">
        <div class="profile-header">
            <img 
                src={user.avatar} 
                alt="{user.name}'s avatar" 
                class="avatar"
            />
            <div class="user-info">
                <h1 class="user-name">
                    {user.name}
                    {#if user.is_admin}
                        <span class="admin-badge">Admin</span>
                    {/if}
                </h1>
                <p class="user-email">{user.email}</p>
            </div>
        </div>

        <div class="profile-details">
            <div class="detail-item">
                <span class="detail-label">User ID</span>
                <span class="detail-value">#{user.id}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Authentication Provider</span>
                <span class="detail-value">{user.auth_provider}</span>
            </div>
        </div>

        <!-- Tickets Section -->
        <div class="tickets-section">
            <h2>Assigned Tickets</h2>
            {#if tickets.length > 0}
                {#each tickets as ticket}
                    <div class="ticket-item">
                        <div class="ticket-title">{ticket.title}</div>
                        <div class="ticket-status">Status: {ticket.status}</div>
                        <p>{ticket.description}</p>
                    </div>
                {/each}
            {:else}
                <p>No tickets assigned to you.</p>
            {/if}
        </div>
    </div>
{/if}
