import { useEffect, useState } from "react";
import Login from "./Login";
import StatCard from "./components/StatCard";
import AlertCard from "./components/AlertCard";
import EventCard from "./components/EventCard";
import EventForm from "./components/EventForm";
import "./App.css";

type DashboardStats = {
  total_events: number;
  total_alerts: number;
  open_alerts: number;
  resolved_alerts: number;
  high_risk_alerts: number;
};

type Alert = {
  id: number;
  event_id: number;
  risk_score: number;
  message: string;
  status: string;
  created_at: string;
};

type SecurityEvent = {
  id: number;
  event_type: string;
  source_ip: string;
  description: string;
  severity: string;
  created_at: string;
};

function App() {
  const [stats, setStats] = useState<DashboardStats>({
    total_events: 0,
    total_alerts: 0,
    open_alerts: 0,
    resolved_alerts: 0,
    high_risk_alerts: 0,
  });

  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [error, setError] = useState("");
  const [token, setToken] = useState(
    sessionStorage.getItem("token") || ""
  );

  useEffect(() => {
    if (!token) return;

    const fetchData = async () => {
      try {
        setError("");

        // 1. Fetch dashboard statistics
        const statsResponse = await fetch(
          "http://127.0.0.1:8000/dashboard/stats",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!statsResponse.ok) {
          throw new Error("Failed to fetch dashboard stats");
        }

        const statsData = await statsResponse.json();
        setStats(statsData);

        // 2. Fetch security alerts
        const alertsResponse = await fetch(
          "http://127.0.0.1:8000/alerts",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!alertsResponse.ok) {
          throw new Error("Failed to fetch alerts");
        }

        const alertsData = await alertsResponse.json();
        setAlerts(alertsData);

        // 3. Fetch security events
        const eventsResponse = await fetch(
          "http://127.0.0.1:8000/events",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!eventsResponse.ok) {
          throw new Error("Failed to fetch events");
        }

        const eventsData = await eventsResponse.json();
        setEvents(eventsData);

      } catch (error) {
        setError(
          error instanceof Error
            ? error.message
            : "Something went wrong"
        );
      }
    };

    fetchData();
  }, [token]);

  if (!token) {
    return (
      <Login
        onLogin={(newToken) => {
          sessionStorage.setItem("token", newToken);
          setToken(newToken);
        }}
      />
    );
  }

  return (
    <div className="dashboard">

      {/* Header */}
      <div className="header">
        <div>
          <h1>Nexavise Sentinel</h1>
          <p>Security Monitoring Dashboard</p>
        </div>

        <button
          className="logout-button"
          onClick={() => {
            sessionStorage.removeItem("token");
            setToken("");
          }}
        >
          Logout
        </button>
      </div>

      {/* Error message */}
      {error && <p className="error">{error}</p>}

      {/* Statistics */}
      <div className="stats-grid">

        <StatCard
          title="Total Events"
          value={stats.total_events}
        />

        <StatCard
          title="Total Alerts"
          value={stats.total_alerts}
        />

        <StatCard
          title="Open Alerts"
          value={stats.open_alerts}
        />

        <StatCard
          title="High Risk Alerts"
          value={stats.high_risk_alerts}
        />

      </div>

      {/* Create Security Event */}
      <EventForm
        token={token}
        onEventCreated={() => {
          window.location.reload();
        }}
      />

      {/* Alerts */}
      <div className="alerts-section">

        <h2>Recent Security Alerts</h2>

        {alerts.length === 0 ? (
          <p>No security alerts found.</p>
        ) : (
          alerts.map((alert) => (
            <AlertCard
              key={alert.id}
              id={alert.id}
              message={alert.message}
              eventId={alert.event_id}
              riskScore={alert.risk_score}
              status={alert.status}
              createdAt={alert.created_at}
              token={token}
              onResolved={() => {
                window.location.reload();
              }}
            />
          ))
        )}

      </div>

      {/* Events */}
      <div className="alerts-section">

        <h2>Security Events</h2>

        {events.length === 0 ? (
          <p>No security events found.</p>
        ) : (
          events.map((event) => (
            <EventCard
              key={event.id}
              eventType={event.event_type}
              sourceIp={event.source_ip}
              description={event.description}
              severity={event.severity}
              createdAt={event.created_at}
            />
          ))
        )}

      </div>

    </div>
  );
}

export default App;