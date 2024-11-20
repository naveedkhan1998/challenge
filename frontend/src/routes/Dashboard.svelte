<script lang="ts">
    import { onMount } from 'svelte';
    import { apiFetch } from '../utils/api';
    import { DonutChart, LineChart } from '@carbon/charts-svelte';
    import type { ChartConfig } from '@carbon/charts/interfaces';
    import '@carbon/charts/styles.css'; // Import Carbon Charts styles

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

    let tickets: Ticket[] = [];
    let loading = true;
    let error: string | null = null;

    // Key statistics
    let totalTickets = 0;
    let openTickets = 0;
    let inProgressTickets = 0;
    let closedTickets = 0;

    // Chart data and options
    let statusChartData: any[] = [];
    let priorityChartData: any[] = [];
    let ticketsOverTimeData: any[] = [];

    let statusChartOptions: ChartConfig<any>;
    let priorityChartOptions: ChartConfig<any>;
    let ticketsOverTimeOptions: ChartConfig<any>;

    // Fetch tickets
    const fetchTickets = async () => {
        loading = true;
        error = null;

        try {
            tickets = await apiFetch('/ticket/tickets/');
            calculateStatistics();
            prepareChartData();
            loading = false;
        } catch (err) {
            error = err.message;
            loading = false;
        }
    };

    const calculateStatistics = () => {
        totalTickets = tickets.length;
        openTickets = tickets.filter(ticket => ticket.status === 'Open').length;
        inProgressTickets = tickets.filter(ticket => ticket.status === 'In Progress').length;
        closedTickets = tickets.filter(ticket => ticket.status === 'Closed').length;
    };

    const prepareChartData = () => {
        // Status Chart Data
        const statusCounts: { [key: string]: number } = {
            'Open': 0,
            'In Progress': 0,
            'Closed': 0
        };

        // Priority Chart Data
        const priorityCounts: { [key: string]: number } = {
            'High': 0,
            'Medium': 0,
            'Low': 0
        };

        // Tickets Over Time Data
        const ticketsByDate: { [key: string]: number } = {};

        tickets.forEach(ticket => {
            // Status
            statusCounts[ticket.status] = (statusCounts[ticket.status] || 0) + 1;

            // Priority
            priorityCounts[ticket.priority] = (priorityCounts[ticket.priority] || 0) + 1;

            // Tickets Over Time
            const date = new Date(ticket.date_created).toISOString().split('T')[0];
            ticketsByDate[date] = (ticketsByDate[date] || 0) + 1;
        });

        statusChartData = Object.keys(statusCounts).map(status => ({
            group: status,
            value: statusCounts[status]
        }));

        priorityChartData = Object.keys(priorityCounts).map(priority => ({
            group: priority,
            value: priorityCounts[priority]
        }));

        ticketsOverTimeData = Object.keys(ticketsByDate).sort().map(date => ({
            group: 'Tickets Created',
            date: new Date(date),
            value: ticketsByDate[date]
        }));

        statusChartOptions = {
            title: 'Status Distribution',
            resizable: true,
            donut: {
                center: {
                    label: 'Tickets'
                }
            },
            legend: {
                position: 'right'
            },
            height: '400px'
        };

        priorityChartOptions = {
            title: 'Priority Distribution',
            resizable: true,
            donut: {
                center: {
                    label: 'Tickets'
                }
            },
            legend: {
                position: 'right'
            },
            height: '400px'
        };

        ticketsOverTimeOptions = {
            title: 'Tickets Over Time',
            axes: {
                bottom: {
                    title: 'Date',
                    mapsTo: 'date',
                    scaleType: 'time'
                },
                left: {
                    mapsTo: 'value',
                    title: 'Number of Tickets',
                    scaleType: 'linear'
                }
            },
            curve: 'curveMonotoneX',
            height: '400px',
            legend: {
                position: 'bottom'
            }
        };
    };

    onMount(fetchTickets);
</script>

<style>
    .dashboard-container {
        max-width: 1200px;
        margin: 2rem auto;
        padding: 1rem;
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .stat-card {
        background-color: #fff;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stat-title {
        font-size: 1rem;
        color: #666;
        margin-bottom: 0.5rem;
    }

    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #333;
    }

    .charts-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
    }

    h1 {
        text-align: center;
        margin-bottom: 2rem;
        color: #333;
    }

    .loading, .error {
        text-align: center;
        padding: 2rem;
        color: #666;
    }

    .error {
        color: #dc3545;
    }
</style>

<div class="dashboard-container">
    {#if loading}
        <div class="loading">
            <p>Loading dashboard...</p>
        </div>
    {:else if error}
        <div class="error">
            <p>Error: {error}</p>
        </div>
    {:else}
        <h1>Dashboard</h1>

        <!-- Key Statistics -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-title">Total Tickets</div>
                <div class="stat-value">{totalTickets}</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Open Tickets</div>
                <div class="stat-value">{openTickets}</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">In Progress Tickets</div>
                <div class="stat-value">{inProgressTickets}</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Closed Tickets</div>
                <div class="stat-value">{closedTickets}</div>
            </div>
        </div>

        <!-- Charts -->
        <div class="charts-grid">
            <!-- Status Distribution -->
            <div>
                <DonutChart data={statusChartData} options={statusChartOptions} />
            </div>

            <!-- Priority Distribution -->
            <div>
                <DonutChart data={priorityChartData} options={priorityChartOptions} />
            </div>

            <!-- Tickets Over Time -->
            <div style="grid-column: span 2;">
                <LineChart data={ticketsOverTimeData} options={ticketsOverTimeOptions} />
            </div>
        </div>
    {/if}
</div>
