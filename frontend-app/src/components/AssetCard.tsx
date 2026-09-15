import { useState } from "react";

type AssetCardProps = {
  id: number;
  name: string;
  target: string;
  assetType: string;
  authorizationStatus: string;
  token: string;
  onScanStarted: () => void;
};

function AssetCard({
  id,
  name,
  target,
  assetType,
  authorizationStatus,
  token,
  onScanStarted,
}: AssetCardProps) {
  const [scanning, setScanning] = useState(false);
  const [scanCompleted, setScanCompleted] = useState(false);
  const [scanError, setScanError] = useState("");

  const startScan = async () => {
    if (scanning) {
      return;
    }

    setScanning(true);
    setScanCompleted(false);
    setScanError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/scans/${id}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (response.status === 401) {
        setScanError(
          "Your session has expired. Please login again."
        );
        return;
      }

      if (response.status === 429) {
        const errorData = await response.json();

        setScanError(
          errorData.detail ||
            "Scan cooldown active. Please wait before scanning again."
        );
        return;
      }

      if (response.status === 403) {
        setScanError(
          "This asset is not authorized for scanning."
        );
        return;
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);

        throw new Error(
          errorData?.detail || "Failed to start scan"
        );
      }

      await response.json();

      setScanCompleted(true);

      onScanStarted();

      setTimeout(() => {
        setScanCompleted(false);
      }, 3000);

    } catch (error) {
      console.error("Scan error:", error);

      setScanError(
        error instanceof Error
          ? error.message
          : "Scan failed"
      );
    } finally {
      setScanning(false);
    }
  };

  const isAuthorized =
    authorizationStatus.toUpperCase() === "AUTHORIZED";

  return (
    <div className="asset-card">

      {/* Header */}
      <div className="asset-card-header">

        <div>
          <h3>{name}</h3>

          <span className="asset-id">
            Asset #{id}
          </span>
        </div>

        <span
          className={`authorization-badge ${
            isAuthorized
              ? "authorized"
              : "unauthorized"
          }`}
        >
          {authorizationStatus}
        </span>

      </div>

      {/* Asset Details */}
      <div className="asset-details">

        <div className="asset-detail">
          <span>Target</span>
          <strong>{target}</strong>
        </div>

        <div className="asset-detail">
          <span>Type</span>
          <strong>{assetType}</strong>
        </div>

      </div>

      {/* Scan Error */}
      {scanError && (
        <div className="scan-error">
          {scanError}
        </div>
      )}

      {/* Scan Action */}
      <button
        className={`start-scan-button ${
          scanning
            ? "scanning"
            : scanCompleted
              ? "scan-completed"
              : ""
        }`}
        onClick={startScan}
        disabled={!isAuthorized || scanning}
      >
        {scanning
          ? "⟳ Scanning..."
          : scanCompleted
            ? "✓ Scan Completed"
            : "Start Scan"}
      </button>

    </div>
  );
}

export default AssetCard;