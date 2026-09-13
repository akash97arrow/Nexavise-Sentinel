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

    const handleResolve = async () => {
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

    return (
        <div className="alert-card">

            <h3>{message}</h3>

            <div className="alert-details">
                <span>Event ID: {eventId}</span>

                <span>
                    Risk Score: <strong>{riskScore}/100</strong>
                </span>

                <span className="status">
                    Status: {status}
                </span>
            </div>

            <div className="risk-bar">
                <div
                    className="risk-bar-fill"
                    style={{ width: `${riskScore}%` }}
                />
            </div>

            <p>Created: {createdAt}</p>

            {status === "OPEN" && (
                <button
                    className="resolve-button"
                    onClick={handleResolve}
                >
                    Resolve Alert
                </button>
            )}

        </div>
    );
}

export default AlertCard;