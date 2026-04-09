import { useState } from "react";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Navbar from "./components/Navbar";
import "./styles.css";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [page, setPage] = useState("login");

  if (!token) {
    return (
      <>
        {page === "login" ? (
          <Login setToken={setToken} switchPage={setPage} />
        ) : (
          <Signup switchPage={setPage} />
        )}
      </>
    );
  }

  return (
    <>
      <Navbar setToken={setToken} />
      <Dashboard />
    </>
  );
}

export default App;