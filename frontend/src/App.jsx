import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import DoctorDashboard from "./pages/DoctorDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import PredictionDetail from "./pages/PredictionDetail";
import DoctorPredictionDetail from "./pages/DoctorPredictionDetail";
import Insights from "./pages/Insights";

function RoleBasedDashboard() {
  const { user } = useAuth();
  if (!user) return <p className="p-8">Loading...</p>;
  if (user.role === "doctor") return <DoctorDashboard />;
  if (user.role === "admin") return <AdminDashboard />;
  return <Dashboard />;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <RoleBasedDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/predictions/:id"
            element={
              <ProtectedRoute>
                <PredictionDetail />
              </ProtectedRoute>
            }
          />
          <Route
            path="/doctor/predictions/:id"
            element={
              <ProtectedRoute>
                <DoctorPredictionDetail />
              </ProtectedRoute>
            }
          />
          <Route
            path="/insights"
            element={
              <ProtectedRoute>
                <Insights />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;