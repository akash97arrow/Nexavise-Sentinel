import { useEffect, useState } from "react";
import Login from "./Login";
import StatCard from "./components/StatCard";
import AlertCard from "./components/AlertCard";
import EventCard from "./components/EventCard";
import EventForm from "./components/EventForm";
import AssetCard from "./components/AssetCard";
import ScanResults from "./components/ScanResults";
import Findings from "./components/Findings";
import ScanHistory from "./components/ScanHistory";
import "./App.css";

type DashboardStats = {
  total_events: number;
  total_alerts: number;
  open_alerts: number;
  resolved_alerts: number;
  high_risk_alerts: number;

  total_findings: number;
  open_findings: number;
  resolved_findings: number;
  critical_findings: number;

  total_attack_paths: number;
  open_attack_paths: number;
  resolved_attack_paths: number;
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

type AttackPath = {
  id: number;
  asset_id: number;
  finding_id: number;
  entry_point: string;
  risk_score: number;
  risk_level: string;
  status: string;
  created_at: string;
};

type Asset = {
  id: number;
  name: string;
  target: string;
  asset_type: string;
  authorization_status: string;
  created_at: string;
};

function App() {
  const [stats, setStats] = useState<DashboardStats>({
    total_events: 0,
    total_alerts: 0,
    open_alerts: 0,
    resolved_alerts: 0,
    high_risk_alerts: 0,

    total_findings: 0,
    open_findings: 0,
    resolved_findings: 0,
    critical_findings: 0,

    total_attack_paths: 0,
    open_attack_paths: 0,
    resolved_attack_paths: 0,
  });

  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [events, setEvents] = useState<SecurityEvent[]>([]);
  const [attackPaths, setAttackPaths] = useState<AttackPath[]>([]);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [dataRefreshKey, setDataRefreshKey] = useState(0);

  const [selectedAssetId, setSelectedAssetId] = useState<number | null>(() => {
    const savedAssetId = sessionStorage.getItem("selectedAssetId");
    return savedAssetId ? Number(savedAssetId) : null;
  });

  const [token, setToken] = useState(
    sessionStorage.getItem("token") || ""
  );


  const handleUnauthorized = () => {
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("selectedAssetId");
    setToken("");
    setSelectedAssetId(null);
    setError("Your session has expired. Please login again.");
  };

  const fetchDashboardData = async () => {
    try {
      setError("");
      setLoading(true);

      // Dashboard statistics
      const statsResponse = await fetch(
        "http://127.0.0.1:8000/dashboard/stats",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (statsResponse.status === 401) {
        handleUnauthorized();
        return;
      }

      if (!statsResponse.ok) {
        throw new Error("Failed to fetch dashboard stats");
      }

      const statsData = await statsResponse.json();
      setStats(statsData);

      // Security alerts
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

      // Security events
      const eventsResponse = await fetch(
        "http://127.0.0.1:8000/events",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!eventsResponse.ok) {
        throw new Error("Failed to fetch security events");
      }

      const eventsData = await eventsResponse.json();
      setEvents(eventsData);

      // Attack paths
      const attackPathsResponse = await fetch(
        "http://127.0.0.1:8000/attack-paths",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!attackPathsResponse.ok) {
        throw new Error("Failed to fetch attack paths");
      }

      const attackPathsData = await attackPathsResponse.json();
      setAttackPaths(attackPathsData);

      // Assets
      const assetsResponse = await fetch(
        "http://127.0.0.1:8000/assets",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!assetsResponse.ok) {
        throw new Error("Failed to fetch assets");
      }

      const assetsData = await assetsResponse.json();
      setAssets(assetsData);

    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!token) return;

    fetchDashboardData();

    const savedAssetId = sessionStorage.getItem("selectedAssetId");

    if (savedAssetId) {
      setSelectedAssetId(Number(savedAssetId));
    }
  }, [token]);

  const resolveAttackPath = async (
    attackPathId: number
  ) => {
    try {
      setError("");

      const response = await fetch(
        `http://127.0.0.1:8000/attack-paths/${attackPathId}`,
        {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            status: "RESOLVED",
          }),
        }
      );

      if (response.status === 401) {
        handleUnauthorized();
        return;
      }

      if (response.status === 403) {
        throw new Error(
          "You are not authorized to update this attack path."
        );
      }

      if (response.status === 404) {
        throw new Error("Attack path not found.");
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);

        throw new Error(
          errorData?.detail ||
          "Failed to resolve attack path."
        );
      }

      const updatedPath = await response.json();

      setAttackPaths((currentPaths) =>
        currentPaths.map((path) =>
          path.id === updatedPath.id
            ? updatedPath
            : path
        )
      );

    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to resolve attack path."
      );
    }
  };

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

      {/* Loading */}
      {loading && (
        <p className="loading-message">
          Loading security dashboard...
        </p>
      )}

      {/* Error */}
      {error && (
        <p className="error">
          {error}
        </p>
      )}

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

        <StatCard
          title="Total Findings"
          value={stats.total_findings}
        />

        <StatCard
          title="Open Findings"
          value={stats.open_findings}
        />

        <StatCard
          title="Critical Findings"
          value={stats.critical_findings}
        />

        <StatCard
          title="Open Attack Paths"
          value={stats.open_attack_paths}
        />

      </div>

      {/* Assets */}
      <div className="asset-section">

        <div className="asset-section-header">

          <div>
            <h2>Authorized Assets</h2>

            <p>
              Assets approved for security assessment
            </p>
          </div>

          <span className="asset-count">
            {assets.length} assets
          </span>

        </div>

        {assets.length === 0 ? (
          <p className="empty-message">
            No authorized assets found.
          </p>
        ) : (
          <div className="asset-grid">

            {assets.map((asset) => (
              <AssetCard
                key={asset.id}
                id={asset.id}
                name={asset.name}
                target={asset.target}
                assetType={asset.asset_type}
                authorizationStatus={
                  asset.authorization_status
                }
                token={token}
                onScanStarted={() => {
                  fetchDashboardData();

                  setSelectedAssetId(asset.id);

                  sessionStorage.setItem(
                    "selectedAssetId",
                    String(asset.id)
                  );

                  setDataRefreshKey(
                    (current) => current + 1
                  );
                }}
              />
            ))}

          </div>
        )}

      </div>

      {/* Create Security Event */}
      <EventForm
        token={token}
        onEventCreated={() => {
          fetchDashboardData();
        }}
      />

      {/* Scan Results */}
      <ScanResults
        token={token}
        refreshKey={dataRefreshKey}
        assetId={selectedAssetId}
      />

      {/* Findings */}
      <Findings
        token={token}
        refreshKey={dataRefreshKey}
        assetId={selectedAssetId}
      />

      <ScanHistory
        token={token}
        refreshKey={dataRefreshKey}
        assetId={selectedAssetId}
      />

      {/* Security Alerts */}
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
                fetchDashboardData();
              }}
            />
          ))
        )}

      </div>

      {selectedAssetId !== null && (
        <button
          className="download-report-button"
          onClick={async () => {
            try {
              const response = await fetch(
                `http://127.0.0.1:8000/reports/${selectedAssetId}/download`,
                {
                  headers: {
                    Authorization: `Bearer ${token}`,
                  },
                }
              );

              if (response.status === 401) {
                handleUnauthorized();
                return;
              }

              if (response.status === 403) {
                throw new Error(
                  "You are not authorized to download this report."
                );
              }

              if (response.status === 404) {
                throw new Error(
                  "Asset not found."
                );
              }

              if (!response.ok) {
                throw new Error(
                  "Failed to download report."
                );
              }

              const blob = await response.blob();
              const url = window.URL.createObjectURL(blob);

              const link = document.createElement("a");
              link.href = url;
              link.download = `nexavise-report-asset-${selectedAssetId}.html`;

              document.body.appendChild(link);
              link.click();
              link.remove();

              window.URL.revokeObjectURL(url);

            } catch (error) {
              console.error("Report download error:", error);

              alert(
                error instanceof Error
                  ? error.message
                  : "Failed to download report."
              );
            }
          }}
        >
          Download Security Report
        </button>
      )}

      {/* Security Events */}
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

      {/* Attack Paths */}
      <div className="alerts-section attack-paths-section">

        <div className="section-header">

          <div>
            <h2>Attack Paths</h2>

            <p>
              Potential entry points identified from exposed
              services
            </p>
          </div>

          <span className="attack-path-count">
            {attackPaths.length} paths
          </span>

        </div>

        {attackPaths.length === 0 ? (
          <p>No attack paths found.</p>
        ) : (
          <div className="attack-path-grid">

            {attackPaths.map((path) => (

              <div
                className={`attack-path-card ${path.risk_level.toLowerCase()}`}
                key={path.id}
              >

                {/* Card Header */}
                <div className="attack-path-header">

                  <div>

                    <h3>
                      {path.entry_point}
                    </h3>

                    <span className="attack-path-id">
                      Attack Path #{path.id}
                    </span>

                  </div>

                  <span
                    className={`risk-badge ${path.risk_level.toLowerCase()}`}
                  >
                    {path.risk_level}
                  </span>

                </div>

                {/* Risk Score */}
                <div className="risk-score-container">

                  <span className="risk-score-label">
                    Risk Score
                  </span>

                  <span className="risk-score">
                    {path.risk_score}
                    <small>/100</small>
                  </span>

                </div>

                {/* Details */}
                <div className="attack-path-details">

                  <div>
                    <span>Asset ID</span>

                    <strong>
                      {path.asset_id}
                    </strong>
                  </div>

                  <div>
                    <span>Finding ID</span>

                    <strong>
                      {path.finding_id}
                    </strong>
                  </div>

                  <div>
                    <span>Status</span>

                    <strong
                      className={path.status.toLowerCase()}
                    >
                      {path.status}
                    </strong>
                  </div>

                </div>

                {/* Action */}
                {path.status === "OPEN" ? (

                  <button
                    className="resolve-button"
                    onClick={() =>
                      resolveAttackPath(path.id)
                    }
                  >
                    Resolve Attack Path
                  </button>

                ) : (

                  <button
                    className="resolve-button reopen"
                    onClick={async () => {
                      try {
                        setError("");

                        const response = await fetch(
                          `http://127.0.0.1:8000/attack-paths/${path.id}`,
                          {
                            method: "PATCH",
                            headers: {
                              "Content-Type": "application/json",
                              Authorization: `Bearer ${token}`,
                            },
                            body: JSON.stringify({
                              status: "OPEN",
                            }),
                          }
                        );

                        if (!response.ok) {
                          throw new Error(
                            "Failed to reopen attack path"
                          );
                        }

                        const updatedPath =
                          await response.json();

                        setAttackPaths(
                          (currentPaths) =>
                            currentPaths.map(
                              (currentPath) =>
                                currentPath.id ===
                                  updatedPath.id
                                  ? updatedPath
                                  : currentPath
                            )
                        );

                      } catch (error) {
                        setError(
                          error instanceof Error
                            ? error.message
                            : "Failed to reopen attack path"
                        );
                      }
                    }}
                  >
                    Reopen Attack Path
                  </button>

                )}

              </div>

            ))}

          </div>
        )}

      </div>

    </div>
  );
}

export default App;