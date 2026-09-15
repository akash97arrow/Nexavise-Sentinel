import React from "react";

type Finding = {
    id: number;
    asset_id: number;
    scan_result_id: number;
    title: string;
    description: string;
    severity: string;
    risk_score: number;
    risk_level: string | null;
    status: string;
    created_at: string;
    last_seen_scan_id: number | null;
    occurrence_count: number;
};

type FindingsProps = {
    token: string;
    refreshKey: number;
    assetId: number | null;
};

function Findings({
    token,
    refreshKey,
    assetId,
}: FindingsProps) {
    const [findings, setFindings] = React.useState<Finding[]>([]);
    const [loading, setLoading] = React.useState(true);
    const [error, setError] = React.useState("");

    React.useEffect(() => {
        if (assetId === null) {
            setFindings([]);
            setLoading(false);
            setError("");
            return;
        }

        const fetchFindings = async () => {
            try {
                setLoading(true);
                setError("");

                const response = await fetch(
                    `http://127.0.0.1:8000/findings/latest?asset_id=${assetId}`,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }
                );

                if (!response.ok) {
                    throw new Error("Failed to fetch security findings");
                }

                const data = await response.json();
                setFindings(data);
            } catch (error) {
                setError(
                    error instanceof Error
                        ? error.message
                        : "Failed to fetch security findings"
                );
            } finally {
                setLoading(false);
            }
        };

        fetchFindings();
    }, [token, refreshKey, assetId]);

    return (
        <div className="findings-section">
            <div className="section-header">
                <div>
                    <h2>Security Findings</h2>
                    <p>
                        Security issues identified during vulnerability analysis
                    </p>
                </div>

                <span className="finding-count">
                    {findings.length} findings
                </span>
            </div>

            {loading ? (
                <p className="empty-message">
                    Loading security findings...
                </p>
            ) : error ? (
                <p className="error">{error}</p>
            ) : findings.length === 0 ? (
                <p className="empty-message">
                    No security findings found.
                </p>
            ) : (
                <div className="findings-grid">
                    {findings.map((finding) => {
                        const severity = finding.severity.toLowerCase();

                        const riskLevel =
                            finding.risk_level?.toLowerCase() || severity;

                        return (
                            <div
                                className={`finding-card ${riskLevel}`}
                                key={finding.id}
                            >
                                <div className="finding-header">
                                    <div>
                                        <h3>{finding.title}</h3>

                                        <span className="finding-id">
                                            Finding #{finding.id}
                                        </span>
                                    </div>

                                    <span
                                        className={`finding-badge ${severity}`}
                                    >
                                        {finding.severity}
                                    </span>
                                </div>

                                <p className="finding-description">
                                    {finding.description}
                                </p>

                                <div className="finding-details">
                                    <div>
                                        <span>Risk Score</span>

                                        <strong>
                                            {finding.risk_score}/100
                                        </strong>
                                    </div>

                                    <div>
                                        <span>Risk Level</span>

                                        <strong>
                                            {finding.risk_level || "N/A"}
                                        </strong>
                                    </div>

                                    <div>
                                        <span>Status</span>

                                        <strong
                                            className={finding.status.toLowerCase()}
                                        >
                                            {finding.status}
                                        </strong>
                                    </div>
                                </div>

                                <div className="finding-meta">
                                    <span>
                                        Asset ID: {finding.asset_id}
                                    </span>

                                    <span>
                                        Last Seen: Scan #
                                        {finding.last_seen_scan_id ?? "N/A"}
                                    </span>

                                    <span>
                                        Occurrences: {finding.occurrence_count}
                                    </span>
                                </div>

                                <div className="finding-actions">
                                    <button
                                        className={`finding-action-button ${
                                            finding.status === "OPEN"
                                                ? "resolve"
                                                : "reopen"
                                        }`}
                                        onClick={async () => {
                                            const newStatus =
                                                finding.status === "OPEN"
                                                    ? "RESOLVED"
                                                    : "OPEN";

                                            try {
                                                const response = await fetch(
                                                    `http://127.0.0.1:8000/findings/${finding.id}`,
                                                    {
                                                        method: "PATCH",
                                                        headers: {
                                                            "Content-Type":
                                                                "application/json",
                                                            Authorization: `Bearer ${token}`,
                                                        },
                                                        body: JSON.stringify({
                                                            status: newStatus,
                                                        }),
                                                    }
                                                );

                                                if (!response.ok) {
                                                    throw new Error(
                                                        "Failed to update finding"
                                                    );
                                                }

                                                setFindings((current) =>
                                                    current.map((item) =>
                                                        item.id === finding.id
                                                            ? {
                                                                  ...item,
                                                                  status: newStatus,
                                                              }
                                                            : item
                                                    )
                                                );
                                            } catch (error) {
                                                setError(
                                                    error instanceof Error
                                                        ? error.message
                                                        : "Failed to update finding"
                                                );
                                            }
                                        }}
                                    >
                                        {finding.status === "OPEN"
                                            ? "Resolve Finding"
                                            : "Reopen Finding"}
                                    </button>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}

export default Findings;