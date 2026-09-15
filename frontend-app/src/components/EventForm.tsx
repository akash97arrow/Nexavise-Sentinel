import { useState } from "react";

type EventFormProps = {
  token: string;
  onEventCreated: () => void;
};

function EventForm({
  token,
  onEventCreated,
}: EventFormProps) {
  const [eventType, setEventType] = useState("");
  const [sourceIp, setSourceIp] = useState("");
  const [description, setDescription] = useState("");
  const [severity, setSeverity] = useState("LOW");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (
    event: React.FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/events",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            event_type: eventType,
            source_ip: sourceIp,
            description,
            severity,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to create security event");
      }

      setEventType("");
      setSourceIp("");
      setDescription("");
      setSeverity("LOW");

      onEventCreated();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="event-form-section">

      <div className="event-form-header">
        <div>
          <h2>Create Security Event</h2>
          <p>
            Record a security event for threat analysis
          </p>
        </div>

        <div className="event-form-icon">
          +
        </div>
      </div>

      <form
        className="event-form"
        onSubmit={handleSubmit}
      >

        <div className="form-field">
          <label htmlFor="event-type">
            Event Type
          </label>

          <input
            id="event-type"
            type="text"
            placeholder="e.g. BRUTE_FORCE"
            value={eventType}
            onChange={(e) =>
              setEventType(e.target.value)
            }
            required
          />
        </div>


        <div className="form-field">
          <label htmlFor="source-ip">
            Source IP
          </label>

          <input
            id="source-ip"
            type="text"
            placeholder="e.g. 192.168.1.50"
            value={sourceIp}
            onChange={(e) =>
              setSourceIp(e.target.value)
            }
            required
          />
        </div>


        <div className="form-field description-field">
          <label htmlFor="description">
            Description
          </label>

          <textarea
            id="description"
            placeholder="Describe the security event..."
            value={description}
            onChange={(e) =>
              setDescription(e.target.value)
            }
            rows={3}
            required
          />
        </div>


        <div className="form-field">
          <label htmlFor="severity">
            Severity
          </label>

          <select
            id="severity"
            value={severity}
            onChange={(e) =>
              setSeverity(e.target.value)
            }
          >
            <option value="LOW">LOW</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="HIGH">HIGH</option>
            <option value="CRITICAL">CRITICAL</option>
          </select>
        </div>


        {error && (
          <div className="event-form-error">
            {error}
          </div>
        )}


        <button
          className="create-event-button"
          type="submit"
          disabled={loading}
        >
          {loading ? "Creating..." : "Create Security Event"}
        </button>

      </form>

    </div>
  );
}

export default EventForm;