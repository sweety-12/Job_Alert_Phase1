import React, { useState } from "react";

const API_URL = import.meta.env.VITE_BACKEND_API_URL;

const SavedPreferences = () => {
  const [email, setEmail] = useState("");
  const [preferences, setPreferences] = useState([]);

  const fetchPreferences = async () => {
    const res = await fetch(`${API_URL}/get-preferences?email=${email}`);
    const data = await res.json();
    setPreferences(data.preferences);
  };

  const deletePreferences = async () => {
    await fetch(`${API_URL}/delete-preferences?email=${email}`, {
      method: "DELETE",
    });
    alert("Preferences deleted");
    setPreferences([]);
  };

  return (
    <div className="form-card">
      <h2>Saved Job Preferences</h2>

      <input
        type="email"
        placeholder="Enter your email"
        className="form-input"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <button className="form-btn" onClick={fetchPreferences}>
        View Preferences
      </button>

      {preferences.length > 0 && (
        <>
          <div style={{ marginTop: "20px" }}>
            {preferences.map((p, idx) => (
              <div key={idx} className="preference-card">
                <p><b>Role:</b> {p.job_role}</p>
                <p><b>Location:</b> {p.location}</p>
                <p><b>Experience:</b> {p.experience}</p>
                <p><b>Mode:</b> {p.work_mode}</p>
              </div>
            ))}
          </div>

          <button
            className="form-btn secondary"
            style={{ marginTop: "15px" }}
            onClick={deletePreferences}
          >
            Delete Preferences
          </button>
        </>
      )}
    </div>
  );
};

export default SavedPreferences;
