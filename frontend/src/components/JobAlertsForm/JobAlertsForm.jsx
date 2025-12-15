import React, { useState } from "react";
import { useNavigate } from "react-router-dom";


const JobAlertsForm = () => {
  const [formData, setFormData] = useState({
    job_role: "",
    location: "",
    experience: "",
    work_mode: "",
    email: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // const handleSubmit = (e) => {
  //   e.preventDefault();
  //   console.log("Submitted Job Alert Data:", formData);
  //   alert("Your job alert preferences were saved!");
  // };

  const handleSubmit = async (e) => {
  e.preventDefault();

  const API_URL = import.meta.env.VITE_BACKEND_API_URL;

  try {
    const response = await fetch(`${API_URL}/save-preferences`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    });

    const data = await response.json();
    alert(data.message);
  } catch (err) {
    console.error(err);
    alert("Failed to save preferences");
  }
};


const handleTestAlert = async () => {
  if (!formData.email) {
    alert("Please enter your email first");
    return;
  }
  try {
    const response = await fetch(
      `${import.meta.env.API_URL}/send-test-alert`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: formData.email }),
      });
      const data = await response.json();
      alert(data.message);
  } catch {
    alert("Failed to send test alert");
  }
};

const navigate = useNavigate();


  // const response = await fetch("http://localhost:8000/save-preferences", {
  //   method: "POST",
  //   headers: {
  //     "Content-Type": "application/json",
  //   },
  //   body: JSON.stringify(formData),
  // });

 

  return (
    <div>
      <div className="form-card">
        <h2 style={{ marginBottom: "20px", color: "#356fe0" }}>
          Job Alert Preferences
        </h2>

        <form onSubmit={handleSubmit}>

          {/* Job Role */}
          <label className="form-label">Job Role</label>
          <input
            type="text"
            name="job_role"
            placeholder="e.g., AI Engineer"
            className="form-input"
            onChange={handleChange}
          />

          {/* Location */}
          <label className="form-label">Location</label>
          <input
            type="text"
            name="location"
            placeholder="e.g., India, Remote"
            className="form-input"
            onChange={handleChange}
          />

          {/* Experience */}
          <label className="form-label">Experience</label>
          <select
            name="experience"
            className="form-select"
            onChange={handleChange}
          >
            <option value="">Select Experience</option>
            {Array.from({ length: 21 }).map((_, i) => (
              <option key={i} value={i}>
                {i} years
              </option>
            ))}
          </select>

          {/* Work Mode */}
          <label className="form-label">Work Mode</label>
          <select
            name="work_mode"
            className="form-select"
            onChange={handleChange}
          >
            <option value="">Choose Work Mode</option>
            <option value="Remote">Remote</option>
            <option value="Hybrid">Hybrid</option>
            <option value="On-site">On-site</option>
          </select>

          {/* Email */}
          <label className="form-label">Email Address</label>
          <input
            type="email"
            name="email"
            placeholder="Enter your email"
            className="form-input"
            onChange={handleChange}
          />

          <div style={{ display: "flex", gap: "12px", marginTop: "20px" }}>
          {/* Submit Button */}
          <button type="submit" className="form-btn">
            Save Preferences
          </button>

          {/*Sent test Alert button */}
          <button
          type="button"
          className="form-btn secondary"
          onClick={handleTestAlert}
          >
         Send Alert
         </button>
        </div>
        </form>
        
        <div>
          {/* Manage Preferences Button */}
          <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "10px" }}>
            <button
              className="form-btn secondary"
              onClick={() => navigate("/preferences")}
            >
              Manage Preferences
            </button>
          </div>

          <div className="form-card">
            {/* existing form */}
          </div>
        </div>

      </div>
    </div>
  );
};

export default JobAlertsForm;
