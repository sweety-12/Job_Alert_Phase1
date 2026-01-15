import { Bell, Settings, Mail, MapPin, Briefcase, Clock, Monitor, CheckCircle } from "lucide-react";
import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
// import { Bell, Settings } from "lucide-react";
// import { useNavigate } from "react-router-dom";

const API_URL = import.meta.env.VITE_BACKEND_API_URL || "http://localhost:8000";

const SavedPreferences = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [preferences, setPreferences] = useState([]);

  // Fetch saved preferences
  const fetchPreferences = async () => {
    if (!email) {
      alert("Please enter your email");
      return;
    }

    try {
      const res = await fetch(`${API_URL}/get-preferences?email=${email}`);
      const data = await res.json();

      if (!data.preferences || data.preferences.length === 0) {
        alert("No preferences found for this email");
        setPreferences([]);
        return;
      }

      setPreferences(data.preferences);
    } catch (err) {
      console.error(err);
      alert("Failed to fetch preferences");
    }
  };

  // Delete preferences
  const deletePreferences = async () => {
    if (!email) {
      alert("Please enter your email first");
      return;
    }

    try {
      await fetch(`${API_URL}/delete-preferences?email=${email}`, {
        method: "DELETE",
      });
      alert("Preferences deleted");
      setPreferences([]);
    } catch (err) {
      console.error(err);
      alert("Failed to delete preferences");
    }
  };

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

      {/* Header */}
      <header className="bg-white shadow-sm relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Bell className="w-8 h-8 text-indigo-600" />
            <h1 className="text-2xl font-bold text-gray-900">Campus Inbox</h1>
          </div>
          <button
            type="button"
            className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            onClick={() => navigate("/")}
          >
            <Settings className="w-4 h-4" />
            <span>Back to Preferences</span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-grow max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 w-full relative z-10">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-xl font-semibold mb-6">Saved Job Preferences</h2>

          {/* Email Input */}
          <input
            type="email"
            placeholder="Enter your email"
            className="form-input w-full mb-4 px-4 py-2 border rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          {/* View Preferences Button */}
          <button
            type="button"
            className="form-btn w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 transition-colors mb-6"
            onClick={fetchPreferences}
          >
            View Preferences
          </button>

          {/* Preferences List */}
          {preferences.length > 0 && (
            <div className="space-y-4">
              {preferences.map((p, idx) => (
                <div key={idx} className="p-4 bg-gray-50 rounded-lg shadow-sm border">
                  <p><b>Role:</b> {p.job_role}</p>
                  <p><b>Location:</b> {p.location}</p>
                  <p><b>Experience:</b> {p.experience} years</p>
                  <p><b>Work Mode:</b> {p.work_mode}</p>
                </div>
              ))}

              {/* Delete Button */}
              <button
                type="button"
                className="form-btn secondary w-full mt-5 bg-red-600 text-white py-2 rounded-lg hover:bg-red-700 transition-colors"
                onClick={deletePreferences}
              >
                Delete Preferences
              </button>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 mt-auto relative z-10">
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
  );
};

export default SavedPreferences;



// -----------------------------------------
// import React, { useState } from "react";

// const API_URL = import.meta.env.VITE_BACKEND_API_URL  || "http://localhost:8000";

// const SavedPreferences = () => {
//   const [email, setEmail] = useState("");
//   const [preferences, setPreferences] = useState([]);

// //   const fetchPreferences = async () => {
// //     const res = await fetch(`${API_URL}/get-preferences?email=${email}`);
// //     const data = await res.json();
// //     setPreferences(data.preferences);
// //   };

//   const fetchPreferences = async () => {
//   if (!email) {
//     alert("Please enter email");
//     return;
//   }

//   const res = await fetch(`${API_URL}/get-preferences?email=${email}`);
//   const data = await res.json();

//   if (!data.preferences || data.preferences.length === 0) {
//     alert("No preferences found for this email");
//     setPreferences([]);
//     return;
//   }

//   setPreferences(data.preferences);
// };


//   const deletePreferences = async () => {
//     await fetch(`${API_URL}/delete-preferences?email=${email}`, {
//       method: "DELETE",
//     });
//     alert("Preferences deleted");
//     setPreferences([]);
//   };

//   return (
//     <div className="form-card">
//       <h2>Saved Job Preferences</h2>

//       <input
//         type="email"
//         placeholder="Enter your email"
//         className="form-input"
//         value={email}
//         onChange={(e) => setEmail(e.target.value)}
//       />

//       <button className="form-btn" onClick={fetchPreferences}>
//         View Preferences
//       </button>

//       {preferences.length > 0 && (
//         <>
//           <div style={{ marginTop: "20px" }}>
//             {preferences.map((p, idx) => (
//               <div key={idx} className="preference-card">
//                 <p><b>Role:</b> {p.job_role}</p>
//                 <p><b>Location:</b> {p.location}</p>
//                 <p><b>Experience:</b> {p.experience}</p>
//                 <p><b>Mode:</b> {p.work_mode}</p>
//               </div>
//             ))}
//           </div>

//           <button
//             className="form-btn secondary"
//             style={{ marginTop: "15px" }}
//             onClick={deletePreferences}
//           >
//             Delete Preferences
//           </button>
//         </>
//       )}
//     </div>
//   );
// };

// export default SavedPreferences;
