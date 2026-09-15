
import React from "react";

type ScanResult = {
  id: number;
  asset_id: number;
  scan_id: number | null;
  port: number;
  protocol: string;
  service: string;
  state: string;
  created_at: string;
};

type ScanResultsProps = {
  token: string;
  refreshKey: number;
  assetId: number | null;
};

function ScanResults({
  token,
  refreshKey,
  assetId,
}: ScanResultsProps) {
  const [results, setResults] = React.useState<ScanResult[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState("");

  React.useEffect(() => {
  if (assetId === null) {
    setResults([]);
    setLoading(false);
    return;
  }

  const fetchScanResults = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(
          `http://127.0.0.1:8000/scan-results/latest?asset_id=${assetId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch scan results");
        }

        const data = await response.json();
        setResults(data);
      } catch (error) {
        setError(
          error instanceof Error
            ? error.message
            : "Failed to fetch scan results"
        );
      } finally {
        setLoading(false);
      }
    };

    fetchScanResults();
}, [token, refreshKey, assetId]);

  return (
    <div className="scan-results-section">
      <div className="section-header">
        <div>
          <h2>Scan Results</h2>
          <p>Discovered ports and services from security scans</p>
        </div>

        <span className="scan-result-count">
          {results.length} results
        </span>
      </div>

      {loading ? (
        <p className="empty-message">Loading scan results...</p>
      ) : error ? (
        <p className="error">{error}</p>
      ) : results.length === 0 ? (
        <p className="empty-message">No scan results found.</p>
      ) : (
        <div className="scan-results-table-container">
          <table className="scan-results-table">
            <thead>
              <tr>
                <th>Port</th>
                <th>Service</th>
                <th>Protocol</th>
                <th>State</th>
                <th>Scan ID</th>
                <th>Discovered</th>
              </tr>
            </thead>

            <tbody>
              {results.map((result) => (
                <tr key={result.id}>
                  <td>
                    <strong>{result.port}</strong>
                  </td>

                  <td>{result.service}</td>

                  <td>{result.protocol}</td>

                  <td>
                    <span
                      className={`scan-state ${result.state.toLowerCase()}`}
                    >
                      {result.state}
                    </span>
                  </td>

                  <td>{result.scan_id ?? "-"}</td>

                  <td>
                    {new Date(result.created_at).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default ScanResults;