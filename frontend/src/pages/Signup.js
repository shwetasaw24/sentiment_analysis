import { useState } from "react";
import API from "../api";

export default function Signup({ switchPage }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const signup = async () => {
    await API.post("/register", { email, password });
    alert("User created!");
    switchPage("login");
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Signup</h2>
        <input placeholder="Email" onChange={e => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
        <button onClick={signup}>Signup</button>
        <p onClick={() => switchPage("login")}>Go to Login</p>
      </div>
    </div>
  );
}