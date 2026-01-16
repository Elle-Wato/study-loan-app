import { useEffect, useState } from "react";
import { api } from "../api";

export default function StaffDashboard() {
  const [applications, setApplications] = useState([]);

  // Fetch all applications from backend
  const fetchApplications = async () => {
    try {
      const res = await api.get("/staff/applications");
      setApplications(res.data);
    } catch (err) {
      console.error(err);
      alert("Error fetching applications");
    }
  };

  useEffect(() => {
    fetchApplications();
  }, []);

  // Review an application
  const handleReview = async (id) => {
    const status = prompt("Enter status (approved/rejected):");
    const feedback = prompt("Enter feedback for student:");

    if (!status || !feedback) return;

    try {
      await api.patch(`/staff/applications/${id}`, { status, feedback });
      alert("Application updated successfully");
      fetchApplications();
    } catch (err) {
      console.error(err);
      alert("Error updating application");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Staff Dashboard</h2>
      {applications.length === 0 ? (
        <p>No applications yet.</p>
      ) : (
        <ul>
          {applications.map((app) => (
            <li key={app.id} style={{ marginBottom: "10px" }}>
              <strong>Application #{app.id}</strong> — Status: {app.status}{" "}
              <button onClick={() => handleReview(app.id)}>Review</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
