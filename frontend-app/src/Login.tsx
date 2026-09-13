import { useState } from "react";

type LoginProps = {
  onLogin: (token: string) => void;
};

function Login({ onLogin }: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (!response.ok) {
        throw new Error("Invalid email or password");
      }

      const data = await response.json();

      onLogin(data.access_token);
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Login failed"
      );
    }
  };

  return (
    <div>
      <h1>Nexavise Sentinel</h1>
      <h2>Security Monitoring Login</h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
      />

      <br />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
      />

      <br />

      <button onClick={handleLogin}>
        Login
      </button>

      {error && <p>{error}</p>}
    </div>
  );
}

export default Login;