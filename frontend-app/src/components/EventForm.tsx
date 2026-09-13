import { useState } from "react";

type EventFormProps = {
  token: string;
  onEventCreated: () => void;
};

function EventForm({ token, onEventCreated }: EventFormProps) {
  const [eventType, setEventType] = useState("");
  const [sourceIp, setSourceIp] = useState("");
  const [description, setDescription] = useState("");
  const [severity, setSeverity] = useState("LOW");
  const [message, setMessage] = useState("");

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setMessage("");

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
            description: description,
            severity: severity,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to create security event");
      }

      setMessage("Security event created successfully");

      setEventType("");
      setSourceIp("");
      setDescription("");
      setSeverity("LOW");

      onEventCreated();
    } catch (error) {
      setMessage(
        error instanceof Error
          ? error.message
          : "Something went wrong"
      );
    }
  };

  return (
    <div className="event-form-section">
      <h2>Create Security Event</h2>

      <form onSubmit={handleSubmit}>

        <input
          type="text"
          placeholder="Event Type (e.g. BRUTE_FORCE)"
          value={eventType}
          onChange={(e) => setEventType(e.target.value)}
          required
        />

        <input
          type="text"
          placeholder="Source IP"
          value={sourceIp}
          onChange={(e) => setSourceIp(e.target.value)}
          required
        />

        <textarea
          placeholder="Event Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />

        <select
          value={severity}
          onChange={(e) => setSeverity(e.target.value)}
        >
          <option value="LOW">LOW</option>
          <option value="MEDIUM">MEDIUM</option>
          <option value="HIGH">HIGH</option>
        </select>

        <button type="submit">
          Create Event
        </button>

      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

export default EventForm;