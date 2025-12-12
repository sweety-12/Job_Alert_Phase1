const Navbar = () => {
  return (
    <nav style={{
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      padding: "15px 25px",
      background: "#4f46e5",
      color: "white"
    }}>
      <h2>Job Alerts</h2>

      <div style={{ display: "flex", gap: "20px" }}>
        <a href="/" style={{ color: "white", textDecoration: "none" }}>Home</a>
        <a href="/saved" style={{ color: "white", textDecoration: "none" }}>Saved Jobs</a>
      </div>
    </nav>
  );
};

export default Navbar;
