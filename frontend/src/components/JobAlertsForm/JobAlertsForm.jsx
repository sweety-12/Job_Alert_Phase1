import React, { useState } from 'react';
import { Bell, Settings, Mail, MapPin, Briefcase, Clock, Monitor, CheckCircle } from 'lucide-react';
import { useNavigate } from "react-router-dom";



export default function JobPreferencesUI() {
  //have to delete the below after checking
  // const [formData, setFormData] = useState({
  //   jobRole: '',
  //   location: '',
  //   experience: '',
  //   modeOfWork: '',
  //   email: ''
  // });

  const [formData, setFormData] = useState({
  job_role: "",
  location: "",
  experience: "",
  work_mode: "",
  email: "",
});

  const API_URL = import.meta.env.VITE_BACKEND_API_URL || "http://localhost:8000";
  const [showSuccess] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await fetch(`${API_URL}/save-preferences`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    const data = await response.json();
    alert(data.message);
  } catch {
    alert("Failed to save preferences");
  }
};


  // const handleSave = () => {
  //   setShowSuccess(true);
  //   setTimeout(() => setShowSuccess(false), 3000);
  // };

  // const handleTestAlert = () => {
  //   alert('Test alert will be sent to: ' + formData.email);
  // };

  const handleTestAlert = async () => {
  if (!formData.email) {
    alert("Please enter your email first");
    return;
  }
  try {
    const response = await fetch(`${API_URL}/send-test-alert`, {
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
  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-50 to-indigo-100"></div>
        
        {/* Animated Blobs */}
        <div className="absolute top-0 left-0 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute top-0 right-0 w-96 h-96 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute bottom-0 left-20 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
        <div className="absolute bottom-0 right-20 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-6000"></div>
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-green-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-3000"></div>
        <div className="absolute top-1/4 right-1/4 w-72 h-72 bg-indigo-300 rounded-full mix-blend-multiply filter blur-xl opacity-60 animate-blob animation-delay-5000"></div>
        
        {/* Floating Particles */}
        <div className="absolute top-20 left-10 w-4 h-4 bg-indigo-400 rounded-full opacity-60 animate-float"></div>
        <div className="absolute top-40 right-20 w-3 h-3 bg-purple-400 rounded-full opacity-60 animate-float animation-delay-1000"></div>
        <div className="absolute bottom-40 left-1/4 w-5 h-5 bg-pink-400 rounded-full opacity-60 animate-float animation-delay-2000"></div>
        <div className="absolute top-60 right-1/3 w-3 h-3 bg-blue-400 rounded-full opacity-60 animate-float animation-delay-3000"></div>
        <div className="absolute bottom-20 right-40 w-4 h-4 bg-yellow-400 rounded-full opacity-60 animate-float animation-delay-4000"></div>
        <div className="absolute top-1/3 left-1/3 w-3 h-3 bg-green-400 rounded-full opacity-60 animate-float animation-delay-2500"></div>
        <div className="absolute bottom-1/3 right-1/4 w-4 h-4 bg-indigo-400 rounded-full opacity-60 animate-float animation-delay-3500"></div>
        
        {/* Animated Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white to-transparent opacity-20 animate-shimmer"></div>
      </div>

      {/* Content Wrapper */}
      <div className="relative z-10 flex flex-col min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Bell className="w-8 h-8 text-indigo-600" />
            <h1 className="text-2xl font-bold text-gray-900">Campus Inbox</h1>
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          type="button"
          onClick={() => navigate("/preferences")}
          // className="text-blue-600 hover:underline text-sm"
          >
            <Settings className="w-4 h-4" />
            <span>Manage Preferences</span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 w-full">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Set Your Job Preferences</h2>
            <p className="text-gray-600">Configure your preferences to receive personalized job alerts directly to your email</p>
          </div>

          {/* Success Message */}
          {showSuccess && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center space-x-2 text-green-800">
              <CheckCircle className="w-5 h-5" />
              <span>Preferences saved successfully!</span>
            </div>
          )}

          {/* Form */}
          <div className="space-y-6">
            {/* Job Role */}
            <div>
              <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-2">
                <Briefcase className="w-4 h-4 text-indigo-600" />
                <span>Job Role</span>
              </label>
              {/* <input
                type="text"
                name="jobRole"
                value={formData.jobRole}
                onChange={handleChange}
                placeholder="e.g., Software Engineer, Product Manager"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
              /> */}
              <input
              type="text"
              name="job_role"
              value={formData.job_role}
              onChange={handleChange}
              placeholder="e.g., Software Engineer, AI Engineer"
              className="w-full px-4 py-3 border rounded-lg"
              />
            </div>

            {/* Location */}
            <div>
              <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-2">
                <MapPin className="w-4 h-4 text-indigo-600" />
                <span>Location</span>
              </label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="e.g., New York, Remote, San Francisco"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
              />
            </div>

            {/* Experience */}
            <div>
              <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-2">
                <Clock className="w-4 h-4 text-indigo-600" />
                <span>Experience Level</span>
              </label>
              <select
                name="experience"
                value={formData.experience}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all bg-white"
              >
                <option value="">Select experience level</option>
                <option value="entry">Entry Level (0-2 years)</option>
                <option value="mid">Mid Level (2-5 years)</option>
                <option value="senior">Senior Level (5-10 years)</option>
                <option value="lead">Lead/Principal (10+ years)</option>
              </select>
            </div>

            {/* Mode of Work */}
            <div>
              <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-2">
                <Monitor className="w-4 h-4 text-indigo-600" />
                <span>Mode of Work</span>
              </label>
              <select
                name="modeOfWork"
                value={formData.modeOfWork}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all bg-white"
              >
                <option value="">Select work mode</option>
                <option value="remote">Remote</option>
                <option value="hybrid">Hybrid</option>
                <option value="onsite">On-site</option>
                <option value="any">Any</option>
              </select>
            </div>

            {/* Email */}
            <div>
              <label className="flex items-center space-x-2 text-sm font-medium text-gray-700 mb-2">
                <Mail className="w-4 h-4 text-indigo-600" />
                <span>Email Address</span>
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="your.email@example.com"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
              />
            </div>
          </div>

          {/* Buttons */}
          <div className="mt-8 flex flex-col sm:flex-row gap-4">
            <button
              onClick={handleSubmit}
              className="flex-1 px-6 py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 transition-colors shadow-md hover:shadow-lg"
            >
              Save Preferences
            </button>
            <button
              onClick={handleTestAlert}
              className="flex-1 px-6 py-3 bg-white text-indigo-600 font-semibold rounded-lg border-2 border-indigo-600 hover:bg-indigo-50 transition-colors"
            >
              Send Test Alert
            </button>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Company Info */}
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center space-x-2 mb-4">
                <Bell className="w-6 h-6 text-indigo-400" />
                <h3 className="text-xl font-bold text-white">Campus Inbox</h3>
              </div>
              <p className="text-gray-400 mb-4">
                Your trusted partner in finding the perfect job. Get personalized job alerts delivered straight to your inbox based on your preferences.
              </p>
              <p className="text-sm text-gray-500">© 2026 CampusInbox. All rights reserved.</p>
            </div>

            {/* Quick Links */}
            <div>
              <h4 className="text-white font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-indigo-400 transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-indigo-400 transition-colors">How It Works</a></li>
                <li><a href="#" className="hover:text-indigo-400 transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="hover:text-indigo-400 transition-colors">Terms of Service</a></li>
              </ul>
            </div>

            {/* Contact */}
            <div>
              <h4 className="text-white font-semibold mb-4">Contact Us</h4>
              <ul className="space-y-2">
                <li className="flex items-start space-x-2">
                  <Mail className="w-4 h-4 mt-1 text-indigo-400" />
                  <a href="mailto:support@campusinbox.org" className="hover:text-indigo-400 transition-colors">
                    support@campusinbox.org
                  </a>
                </li>
                {/* <li className="flex items-start space-x-2">
                  <MapPin className="w-4 h-4 mt-1 text-indigo-400" />
                  <span>123 Tech Street, Silicon Valley, CA 94025</span>
                </li> */}
              </ul>
              <div className="mt-4">
                <a href="#" className="inline-block px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm">
                  Contact Support
                </a>
              </div>
            </div>
          </div>
        </div>
      </footer>
      </div>

      {/* Custom Animations */}
      <style>{`
        @keyframes blob {
          0% {
            transform: translate(0px, 0px) scale(1);
          }
          33% {
            transform: translate(30px, -50px) scale(1.1);
          }
          66% {
            transform: translate(-20px, 20px) scale(0.9);
          }
          100% {
            transform: translate(0px, 0px) scale(1);
          }
        }
        
        @keyframes float {
          0% {
            transform: translateY(0px) translateX(0px);
            opacity: 0.6;
          }
          50% {
            transform: translateY(-100px) translateX(50px);
            opacity: 0.3;
          }
          100% {
            transform: translateY(-200px) translateX(100px);
            opacity: 0;
          }
        }
        
        @keyframes shimmer {
          0% {
            transform: translateX(-100%);
          }
          100% {
            transform: translateX(100%);
          }
        }
        
        .animate-blob {
          animation: blob 7s infinite;
        }
        
        .animate-float {
          animation: float 8s infinite;
        }
        
        .animate-shimmer {
          animation: shimmer 8s infinite;
        }
        
        .animation-delay-1000 {
          animation-delay: 1s;
        }
        .animation-delay-2000 {
          animation-delay: 2s;
        }
        .animation-delay-2500 {
          animation-delay: 2.5s;
        }
        .animation-delay-3000 {
          animation-delay: 3s;
        }
        .animation-delay-3500 {
          animation-delay: 3.5s;
        }
        .animation-delay-4000 {
          animation-delay: 4s;
        }
        .animation-delay-5000 {
          animation-delay: 5s;
        }
        .animation-delay-6000 {
          animation-delay: 6s;
        }
      `}</style>
    </div>
  );
}


// // -------------------------------
// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";


// const JobAlertsForm = () => {
//   const navigate = useNavigate();

//   const [formData, setFormData] = useState({
//     job_role: "",
//     location: "",
//     experience: "",
//     work_mode: "",
//     email: "",
//   });

//  const API_URL = import.meta.env.VITE_BACKEND_API_URL;

//   const handleChange = (e) => {
//     setFormData({
//       ...formData,
//       [e.target.name]: e.target.value,
//     });
//   };

//   // const handleSubmit = (e) => {
//   //   e.preventDefault();
//   //   console.log("Submitted Job Alert Data:", formData);
//   //   alert("Your job alert preferences were saved!");
//   // };

//   const handleSubmit = async (e) => {
//   e.preventDefault();

//   // const API_URL = import.meta.env.VITE_BACKEND_API_URL;
//   try {
//     const response = await fetch(`${API_URL}/save-preferences`, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(formData),
//     });

//     const data = await response.json();
//     alert(data.message);
//   } catch (err) {
//     console.error(err);
//     alert("Failed to save preferences");
//   }
// };


// const handleTestAlert = async () => {
//   if (!formData.email) {
//     alert("Please enter your email first");
//     return;
//   }
//   try {
//     const response = await fetch(
//       `${API_URL}/send-test-alert`,
//       {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ email: formData.email }),
//       });
//       const data = await response.json();
//       alert(data.message);
//   } catch {
//     alert("Failed to send test alert");
//   }
// }; 

// // const navigate = useNavigate();


//   // const response = await fetch("http://localhost:8000/save-preferences", {
//   //   method: "POST",
//   //   headers: {
//   //     "Content-Type": "application/json",
//   //   },
//   //   body: JSON.stringify(formData),
//   // });
  
//   return (
//     <div className="form-card">

//       {/* HEADER */}
//       <div className="form-header">
//         <h2>Job Alert Preferences</h2>

//         <button
//           className="link-btn"
//           onClick={() => navigate("/preferences")}
//         >
//           Manage Preferences
//         </button>
//       </div>

//       <form onSubmit={handleSubmit}>
//         <label className="form-label">Job Role</label>
//         <input
//           className="form-input"
//           name="job_role"
//           onChange={handleChange}
//         />

//         <label className="form-label">Location</label>
//         <input
//           className="form-input"
//           name="location"
//           onChange={handleChange}
//         />

//         <label className="form-label">Experience</label>
//         <select
//           className="form-select"
//           name="experience"
//           onChange={handleChange}
//         >
//           <option value="">Select</option>
//           {Array.from({ length: 21 }).map((_, i) => (
//             <option key={i} value={i}>{i} years</option>
//           ))}
//         </select>

//         <label className="form-label">Work Mode</label>
//         <select
//           className="form-select"
//           name="work_mode"
//           onChange={handleChange}
//         >
//           <option value="">Choose</option>
//           <option>Remote</option>
//           <option>Hybrid</option>
//           <option>On-site</option>
//         </select>

//         <label className="form-label">Email</label>
//         <input
//           className="form-input"
//           type="email"
//           name="email"
//           onChange={handleChange}
//         />

//         <div className="button-group">
//           <button type="submit" className="form-btn">
//             Save Preferences
//           </button>

//           <button
//             type="button"
//             className="form-btn secondary"
//             onClick={handleTestAlert}
//           >
//             Send Test Alert
//           </button>
//         </div>
//       </form>
//     </div>
//    );
//   };
//   // return (
//   //   <div>
//   //     <div className="form-card">
//   //       <h2 style={{ marginBottom: "20px", color: "#356fe0" }}>
//   //         Job Alert Preferences
//   //       </h2>

//   //       <form onSubmit={handleSubmit}>

//   //         {/* Job Role */}
//   //         <label className="form-label">Job Role</label>
//   //         <input
//   //           type="text"
//   //           name="job_role"
//   //           placeholder="e.g., AI Engineer"
//   //           className="form-input"
//   //           onChange={handleChange}
//   //         />

//   //         {/* Location */}
//   //         <label className="form-label">Location</label>
//   //         <input
//   //           type="text"
//   //           name="location"
//   //           placeholder="e.g., India, Remote"
//   //           className="form-input"
//   //           onChange={handleChange}
//   //         />

//   //         {/* Experience */}
//   //         <label className="form-label">Experience</label>
//   //         <select
//   //           name="experience"
//   //           className="form-select"
//   //           onChange={handleChange}
//   //         >
//   //           <option value="">Select Experience</option>
//   //           {Array.from({ length: 21 }).map((_, i) => (
//   //             <option key={i} value={i}>
//   //               {i} years
//   //             </option>
//   //           ))}
//   //         </select>

//   //         {/* Work Mode */}
//   //         <label className="form-label">Work Mode</label>
//   //         <select
//   //           name="work_mode"
//   //           className="form-select"
//   //           onChange={handleChange}
//   //         >
//   //           <option value="">Choose Work Mode</option>
//   //           <option value="Remote">Remote</option>
//   //           <option value="Hybrid">Hybrid</option>
//   //           <option value="On-site">On-site</option>
//   //         </select>

//   //         {/* Email */}
//   //         <label className="form-label">Email Address</label>
//   //         <input
//   //           type="email"
//   //           name="email"
//   //           placeholder="Enter your email"
//   //           className="form-input"
//   //           onChange={handleChange}
//   //         />

//   //         <div style={{ display: "flex", gap: "12px", marginTop: "20px" }}>
//   //         {/* Submit Button */}
//   //         <button type="submit" className="form-btn">
//   //           Save Preferences
//   //         </button>

//   //         {/*Sent test Alert button */}
//   //         <button
//   //         type="button"
//   //         className="form-btn secondary"
//   //         onClick={handleTestAlert}
//   //         >
//   //        Send Alert
//   //        </button>
//   //       </div>
//   //       </form>

//   //       <div>
//   //         {/* Manage Preferences Button */}
//   //         <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "10px" }}>
//   //           <button
//   //             className="form-btn secondary"
//   //             onClick={() => navigate("/preferences")}
//   //           >
//   //             Manage Preferences
//   //           </button>
//   //         </div>

//   //         <div className="form-card">
//   //           {/* existing form */}
//   //         </div>
//   //       </div>

//   //     </div>
//   //   </div>
//   // );


// export default JobAlertsForm;
