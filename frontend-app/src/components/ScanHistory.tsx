import React from "react";

type Scan = {
    id: number;
    asset_id: number;
    status: string;
    started_at: string;
    completed_at: string | null;
};

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

type ScanHistoryProps = {
    token: string;
    refreshKey: number;
    assetId: number | null;
};

function ScanHistory({
    token,
    refreshKey,
    assetId,
}: ScanHistoryProps) {
    const [scans, setScans] = React.useState<Scan[]>([]);
    const [selectedScanId, setSelectedScanId] = React.useState<number | null>(
        null
    );
    const [results, setResults] = React.useState<ScanResult[]>([]);
    const [loading, setLoading] = React.useState(false);
    const [resultsLoading, setResultsLoading] = React.useState(false);
    const [error, setError] = React.useState("");

    React.useEffect(() => {
        if (assetId === null) {
            setScans([]);
            setSelectedScanId(null);
            setResults([]);
            return;
        }

        const fetchScanHistory = async () => {
            try {
                setLoading(true);
                setError("");

                const response = await fetch(
                    `http://127.0.0.1:8000/scans?asset_id=${assetId}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );

                if (!response.ok) {
                    throw new Error("Failed to fetch scan history");
                }

                const data = await response.json();
                setScans(data);
            } catch (error) {
                setError(
                    error instanceof Error
                        ? error.message
                        : "Failed to fetch scan history"
                );
            } finally {
                setLoading(false);
            }
        };

        fetchScanHistory();
    }, [token, refreshKey, assetId]);

    const viewScanResults = async (scanId: number) => {
        try {
            setResultsLoading(true);
            setError("");
            setSelectedScanId(scanId);

            const response = await fetch(
                `http://127.0.0.1:8000/scans/${scanId}/results`,
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
            setResultsLoading(false);
        }
    };

    if (assetId === null) {
        return (
            <div className="scan-history-section">
                <div className="section-header">
                    <div>
                        <h2>Scan History</h2>
                        <p>Select an asset to view scan history</p>
                    </div>
                </div>

                <p className="empty-message">
                    No asset selected.
                </p>
            </div>
        );
    }

    return (
        <div className="scan-history-section">
            <div className="section-header">
                <div>
                    <h2>Scan History</h2>
                    <p>
                        Previous security scans for the selected asset
                    </p>
                </div>

                <span className="scan-history-count">
                    {scans.length} scans
                </span>
            </div>

            {loading ? (
                <p className="empty-message">
                    Loading scan history...
                </p>
            ) : error ? (
                <p className="error">{error}</p>
            ) : scans.length === 0 ? (
                <p className="empty-message">
                    No scan history found.
                </p>
            ) : (
                <>
                    <div className="scan-history-list">
                        {scans.map((scan) => (
                            <div
                                className={`scan-history-card ${
                                    selectedScanId === scan.id
                                        ? "selected"
                                        : ""
                                }`}
                                key={scan.id}
                            >
                                <div className="scan-history-info">
                                    <div>
                                        <h3>
                                            Scan #{scan.id}
                                        </h3>

                                        <span>
                                            Asset #{scan.asset_id}
                                        </span>
                                    </div>

                                    <span
                                        className={`scan-history-status ${scan.status.toLowerCase()}`}
                                    >
                                        {scan.status}
                                    </span>
                                </div>

                                <div className="scan-history-details">
                                    <div>
                                        <span>Started</span>
                                        <strong>
                                            {new Date(
                                                scan.started_at
                                            ).toLocaleString()}
                                        </strong>
                                    </div>

                                    <div>
                                        <span>Completed</span>
                                        <strong>
                                            {scan.completed_at
                                                ? new Date(
                                                      scan.completed_at
                                                  ).toLocaleString()
                                                : "-"}
                                        </strong>
                                    </div>
                                </div>

                                <button
                                    className="view-scan-button"
                                    onClick={() =>
                                        viewScanResults(scan.id)
                                    }
                                >
                                    View Results
                                </button>
                            </div>
                        ))}
                    </div>

                    {selectedScanId !== null && (
                        <div className="scan-history-results">
                            <div className="section-header">
                                <div>
                                    <h3>
                                        Scan #{selectedScanId} Results
                                    </h3>

                                    <p>
                                        Exact results recorded during this scan
                                    </p>
                                </div>

                                <span className="scan-result-count">
                                    {results.length} results
                                </span>
                            </div>

                            {resultsLoading ? (
                                <p className="empty-message">
                                    Loading scan results...
                                </p>
                            ) : results.length === 0 ? (
                                <p className="empty-message">
                                    No results found for this scan.
                                </p>
                            ) : (
                                <div className="scan-results-table-container">
                                    <table className="scan-results-table">
                                        <thead>
                                            <tr>
                                                <th>Port</th>
                                                <th>Service</th>
                                                <th>Protocol</th>
                                                <th>State</th>
                                                <th>Discovered</th>
                                            </tr>
                                        </thead>

                                        <tbody>
                                            {results.map((result) => (
                                                <tr key={result.id}>
                                                    <td>
                                                        <strong>
                                                            {result.port}
                                                        </strong>
                                                    </td>

                                                    <td>
                                                        {result.service}
                                                    </td>

                                                    <td>
                                                        {result.protocol}
                                                    </td>

                                                    <td>
                                                        <span
                                                            className={`scan-state ${result.state.toLowerCase()}`}
                                                        >
                                                            {result.state}
                                                        </span>
                                                    </td>

                                                    <td>
                                                        {new Date(
                                                            result.created_at
                                                        ).toLocaleString()}
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </div>
                    )}
                </>
            )}
        </div>
    );
}

export default ScanHistory;