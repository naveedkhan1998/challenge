<script lang="ts">
    import { onMount } from 'svelte';
    import { apiFetch } from '../utils/api';

    // Ticket interface to match serializer
    interface Ticket {
        id?: number;
        title: string;
        description: string;
        status: string;
        priority: string;
        date_created?: string;
        assigned_to?: number | null;
        assigned_to_username?: string | null;
    }

    // User interface
    interface User {
        id: number;
        name: string;
        email: string;
    }

    // State management
    let tickets: Ticket[] = [];
    let users: User[] = [];
    let loading = true;
    let error: string | null = null;

    // Modal and form states
    let showModal = false;
    let editingTicket: Ticket | null = null;
    let modalMode: 'create' | 'edit' = 'create';

    // Filters
    let priorityFilter = '';
    let statusFilter = '';
    let searchQuery = '';
    let orderBy = 'date_created';
    let orderDirection = 'desc';

    // Fetch tickets with filtering
    const fetchTickets = async () => {
        loading = true;
        error = null;

        try {
            const params = new URLSearchParams();
            
            if (priorityFilter) params.append('priority', priorityFilter);
            if (statusFilter) params.append('status', statusFilter);
            if (searchQuery) params.append('search', searchQuery);
            
            params.append('ordering', `${orderDirection === 'desc' ? '-' : ''}${orderBy}`);

            const url = `/ticket/tickets/?${params.toString()}`;
            tickets = await apiFetch(url);
            loading = false;
        } catch (err) {
            error = err.message;
            loading = false;
        }
    };

    // Fetch users for assignment
    const fetchUsers = async () => {
        try {
            users = await apiFetch('/account/users/');
        } catch (err) {
            error = err.message;
        }
    };

    // Open modal for creating new ticket
    const openCreateModal = () => {
        editingTicket = {
            title: '',
            description: '',
            status: 'Open',
            priority: 'Medium',
            assigned_to: null
        };
        modalMode = 'create';
        showModal = true;
    };

    // Open modal for editing existing ticket
    const openEditModal = (ticket: Ticket) => {
        editingTicket = { ...ticket };
        modalMode = 'edit';
        showModal = true;
    };

    // Save ticket (create or update)
    const saveTicket = async () => {
        try {
            if (modalMode === 'create') {
                // Create new ticket
                await apiFetch('/ticket/tickets/', {
                    method: 'POST',
                    body: JSON.stringify(editingTicket)
                });
            } else if (editingTicket?.id) {
                // Update existing ticket
                await apiFetch(`/ticket/tickets/${editingTicket.id}/`, {
                    method: 'PUT',
                    body: JSON.stringify(editingTicket)
                });
            }

            // Refresh tickets and close modal
            await fetchTickets();
            showModal = false;
            editingTicket = null;
        } catch (err) {
            error = err.message;
        }
    };

    // Delete ticket
    const deleteTicket = async (ticketId: number) => {
        if (!confirm('Are you sure you want to delete this ticket?')) return;

        try {
            await apiFetch(`/ticket/tickets/${ticketId}/`, {
                method: 'DELETE'
            });
            await fetchTickets();
        } catch (err) {
            error = err.message;
        }
    };

    // Reset filters
    const resetFilters = () => {
        priorityFilter = '';
        statusFilter = '';
        searchQuery = '';
        orderBy = 'date_created';
        orderDirection = 'desc';
        fetchTickets();
    };

    // Lifecycle
    onMount(() => {
        fetchTickets();
        fetchUsers();
    });

    // Toggle ordering
    const toggleOrdering = (field: string) => {
        if (orderBy === field) {
            orderDirection = orderDirection === 'desc' ? 'asc' : 'desc';
        } else {
            orderBy = field;
            orderDirection = 'desc';
        }
        fetchTickets();
    };

    // Format date
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    // Priority and status color mapping
    const getPriorityColor = (priority: string) => {
        switch(priority) {
            case 'High': return 'bg-red-100 text-red-800';
            case 'Medium': return 'bg-yellow-100 text-yellow-800';
            case 'Low': return 'bg-green-100 text-green-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    };

    const getStatusColor = (status: string) => {
        switch(status) {
            case 'Open': return 'bg-blue-100 text-blue-800';
            case 'In Progress': return 'bg-yellow-100 text-yellow-800';
            case 'Closed': return 'bg-gray-100 text-gray-800';
            default: return 'bg-gray-100 text-gray-800';
        }
    };
</script>

<style>
    .ticket-container {
        max-width: 1200px;
        margin: 2rem auto;
        padding: 1rem;
    }

    .filters {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
        align-items: center;
    }

    .ticket-list {
        display: grid;
        gap: 1rem;
    }

    .ticket-card {
        background-color: #fff;
        border-radius: 8px;
        padding: 1.25rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .ticket-content {
        flex-grow: 1;
        margin-right: 1rem;
    }

    .ticket-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        border-bottom: 1px solid #eee;
        padding-bottom: 0.75rem;
    }

    .ticket-title {
        font-size: 1.25rem;
        font-weight: bold;
        color: #333;
    }

    .badge {
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-left: 0.5rem;
    }

    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .modal-content {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        width: 100%;
        max-width: 500px;
    }

    .modal-actions {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
    }

    input, select, textarea {
        width: 100%;
        padding: 0.5rem;
        margin-bottom: 1rem;
        border: 1px solid #ddd;
        border-radius: 4px;
    }

    .action-buttons {
        display: flex;
        gap: 0.5rem;
    }
</style>

<div class="ticket-container">
    <div class="filters">
        <!-- Search Input -->
        <input 
            type="text" 
            placeholder="Search tickets..." 
            bind:value={searchQuery}
            on:input={fetchTickets}
        />

        <!-- Priority Filter -->
        <select bind:value={priorityFilter} on:change={fetchTickets}>
            <option value="">All Priorities</option>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
        </select>

        <!-- Status Filter -->
        <select bind:value={statusFilter} on:change={fetchTickets}>
            <option value="">All Statuses</option>
            <option value="Open">Open</option>
            <option value="In Progress">In Progress</option>
            <option value="Closed">Closed</option>
        </select>

        <!-- Reset and Create Buttons -->
        <button on:click={resetFilters}>Reset Filters</button>
        <button on:click={openCreateModal}>+ Create Ticket</button>
    </div>

    {#if loading}
        <p>Loading tickets...</p>
    {:else if error}
        <p>Error: {error}</p>
    {:else if tickets.length === 0}
        <p>No tickets found.</p>
    {:else}
        <div class="ticket-list">
            {#each tickets as ticket (ticket.id)}
                <div class="ticket-card">
                    <div class="ticket-content">
                        <div class="ticket-header">
                            <div class="ticket-title">
                                {ticket.title}
                                
                                <!-- Priority Badge -->
                                <span 
                                    class="badge {getPriorityColor(ticket.priority)}"
                                >
                                    {ticket.priority}
                                </span>

                                <!-- Status Badge -->
                                <span 
                                    class="badge {getStatusColor(ticket.status)}"
                                >
                                    {ticket.status}
                                </span>
                            </div>
                            
                            <div>
                                {formatDate(ticket.date_created || new Date().toISOString())}
                            </div>
                        </div>

                        <p>{ticket.description}</p>

                        {#if ticket.assigned_to}
                            <p>Assigned to: {users.find(user => user.id === ticket.assigned_to)?.name || 'Unassigned'}</p>
                        {:else}
                            <p>Assigned to: Unassigned</p>
                        {/if}
                    </div>

                    <div class="action-buttons">
                        <button on:click={() => openEditModal(ticket)}>Edit</button>
                        <button on:click={() => deleteTicket(ticket.id!)}>Delete</button>
                    </div>
                </div>
            {/each}
        </div>
    {/if}

    <!-- Modal for Create/Edit Ticket -->
    {#if showModal && editingTicket}
        <div class="modal">
            <div class="modal-content">
                <h2>{modalMode === 'create' ? 'Create New Ticket' : 'Edit Ticket'}</h2>
                
                <input 
                    type="text" 
                    placeholder="Ticket Title" 
                    bind:value={editingTicket.title}
                    required
                />

                <textarea 
                    placeholder="Ticket Description" 
                    bind:value={editingTicket.description}
                    rows="4"
                    required
                ></textarea>

                <select bind:value={editingTicket.priority}>
                    <option value="Low">Low Priority</option>
                    <option value="Medium">Medium Priority</option>
                    <option value="High">High Priority</option>
                </select>

                <select bind:value={editingTicket.status}>
                    <option value="Open">Open</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Closed">Closed</option>
                </select>

                <select bind:value={editingTicket.assigned_to}>
                    <option value="">Unassigned</option>
                    {#each users as user}
                        <option value={user.id}>{user.name}</option>
                    {/each}
                </select>

                <div class="modal-actions">
                    <button on:click={() => showModal = false}>Cancel</button>
                    <button on:click={saveTicket}>
                        {modalMode === 'create' ? 'Create Ticket' : 'Update Ticket'}
                    </button>
                </div>
            </div>
        </div>
    {/if}
</div>
