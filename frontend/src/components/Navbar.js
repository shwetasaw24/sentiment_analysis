export default function Navbar({ setToken }) {

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <div className="navbar">
      AI Feedback System
      <button className="logout" onClick={logout}>
        Logout
      </button>
    </div>
  );
}