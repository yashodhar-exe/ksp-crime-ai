import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "@/context/AuthContext";
import { ProtectedRoute } from "@/components/layout/ProtectedRoute";

import LoginPage from "@/pages/LoginPage";
import RegisterPage from "@/pages/RegisterPage";
import DashboardPage from "@/pages/DashboardPage";
import CasesListPage from "@/pages/CasesListPage";
import CaseDetailPage from "@/pages/CaseDetailPage";
import SearchPage from "@/pages/SearchPage";
import CitizensPage from "@/pages/CitizensPage";
import CitizenProfilePage from "@/pages/CitizenProfilePage";
import NetworkGraphPage from "@/pages/NetworkGraphPage";
import OfficersPage from "@/pages/OfficersPage";
import StationsPage from "@/pages/StationsPage";
import AnalyticsPage from "@/pages/AnalyticsPage";
import AssistantPage from "@/pages/AssistantPage";
import AuditPage from "@/pages/AuditPage";
import UsersPage from "@/pages/UsersPage";
import SettingsPage from "@/pages/SettingsPage";

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/cases" element={<CasesListPage />} />
            <Route path="/cases/:caseId" element={<CaseDetailPage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/citizens" element={<CitizensPage />} />
            <Route path="/citizens/:citizenId" element={<CitizenProfilePage />} />
            <Route path="/network" element={<NetworkGraphPage />} />
            <Route path="/network/:citizenId" element={<NetworkGraphPage />} />
            <Route path="/officers" element={<OfficersPage />} />
            <Route path="/officers/:officerId" element={<OfficersPage />} />
            <Route path="/stations" element={<StationsPage />} />
            <Route path="/stations/:stationId" element={<StationsPage />} />
            <Route path="/analytics" element={<AnalyticsPage />} />
            <Route path="/assistant" element={<AssistantPage />} />
            <Route path="/audit" element={<AuditPage />} />
            <Route path="/users" element={<UsersPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>

          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
