type EventCardProps = {
  eventType: string;
  sourceIp: string;
  description: string;
  severity: string;
  createdAt: string;
};

function EventCard({
  eventType,
  sourceIp,
  description,
  severity,
  createdAt,
}: EventCardProps) {
  const severityLevel = severity.toUpperCase();

  return (
    <div
      className={`security-event-card ${severityLevel.toLowerCase()}`}
    >

      {/* Event Header */}
      <div className="security-event-header">

        <div>
          <h3>{eventType}</h3>

          <span className="security-event-source">
            Source IP: {sourceIp}
          </span>
        </div>

        <span
          className={`security-event-badge ${severityLevel.toLowerCase()}`}
        >
          {severityLevel}
        </span>

      </div>


      {/* Description */}
      <div className="security-event-description">
        {description}
      </div>


      {/* Footer */}
      <div className="security-event-footer">

        <span>
          Created:{" "}
          {new Date(createdAt).toLocaleString()}
        </span>

        <span className="security-event-status">
          EVENT RECORDED
        </span>

      </div>

    </div>
  );
}

export default EventCard;