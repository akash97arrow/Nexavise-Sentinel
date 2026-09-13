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

  const severityClass = severity.toLowerCase();

  return (
    <div className="event-card">
      <div className="event-header">
        <h3>{eventType}</h3>

        <span className={`severity ${severityClass}`}>
          {severity}
        </span>
      </div>

      <div className="event-details">
        <span>Source IP: {sourceIp}</span>
      </div>

      <p>{description}</p>

      <small>Created: {createdAt}</small>
    </div>
  );
}

export default EventCard;