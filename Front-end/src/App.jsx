import { BrowserRouter, Routes, Route } from 'react-router-dom'
import LandingPage from './pages/merchant/landing/LandingPage'
import RegisterPage from './pages/Register'
import RegisterStep2Page from './pages/RegisterStep2'
import RegisterStep3Page from './pages/RegisterStep3'
import SignInPage from './pages/SignIn'
import AIDiagnosticPage from './pages/AIDiagnostic'
import BuildingAssistantPage from './pages/BuildingAssistant'
import Dashboard from './pages/merchant/dashboard/Dashboard'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/register/step-2" element={<RegisterStep2Page />} />
        <Route path="/register/step-3" element={<RegisterStep3Page />} />
        <Route path="/signin" element={<SignInPage />} />
        <Route path="/onboarding" element={<AIDiagnosticPage />} />
        <Route path="/diagnostic" element={<AIDiagnosticPage />} />
        <Route path="/building-assistant" element={<BuildingAssistantPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
