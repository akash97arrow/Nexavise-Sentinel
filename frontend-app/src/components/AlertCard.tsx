type AlertCardProps = {
  id: number;
  message: string;
  eventId: number;
  riskScore: number;
  status: string;
  createdAt: string;
  token: string;
  onResolved: () => void;
};

function AlertCard({
  id,
  message,
  eventId,
  riskScore,
  status,
  createdAt,
  token,
  onResolved,
}: AlertCardProps) {
  const resolveAlert = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:8000/alerts/${id}`,
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

      if (!response.ok) {
        throw new Error("Failed to resolve alert");
      }

      onResolved();
    } catch (error) {
      console.error(error);
    }
  };

  const riskLevel =
    riskScore >= 75
      ? "HIGH"
      : riskScore >= 50
        ? "MEDIUM"
        : "LOW";

  return (
    <div className={`security-alert-card ${riskLevel.toLowerCase()}`}>

      <div className="security-alert-header">

        <div>
          <h3>{message}</h3>

          <span className="security-alert-id">
            Alert #{id}
          </span>
        </div>

        <span
          className={`security-alert-badge ${riskLevel.toLowerCase()}`}
        >
          {riskLevel}
        </span>

      </div>


      <div className="security-alert-details">

        <div className="security-alert-detail">
          <span>Event ID</span>
          <strong>{eventId}</strong>
        </div>

        <div className="security-alert-detail">
          <span>Risk Score</span>
          <strong>{riskScore}/100</strong>
        </div>

        <div className="security-alert-detail">
          <span>Status</span>
          <strong className={status.toLowerCase()}>
            {status}
          </strong>
        </div>

      </div>


      <div className="security-alert-footer">

        <span>
          Created:{" "}
          {new Date(createdAt).toLocaleString()}
        </span>

        {status === "OPEN" ? (
          <button
            className="resolve-alert-button"
            onClick={resolveAlert}
          >
            Resolve Alert
          </button>
        ) : (
          <span className="alert-resolved-message">
            ✓ Resolved
          </span>
        )}

      </div>

    </div>
  );
}

export default AlertCard;