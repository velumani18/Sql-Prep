import React from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import { Navbar } from './components/common/Navbar';
import { Footer } from './components/common/Footer';
import { LandingPage } from './pages/LandingPage';
import { DashboardPage } from './pages/DashboardPage';
import { RoadmapPage } from './pages/RoadmapPage';
import { LessonPage } from './pages/LessonPage';
import { WorkspacePage } from './pages/WorkspacePage';
import { InterviewPage } from './pages/InterviewPage';

const AppContent: React.FC = () => {
  const location = useLocation();
  const isWorkspace = location.pathname.startsWith('/practice');

  return (
    <div className="flex flex-col min-h-screen bg-dark-950 text-dark-100">
      <Navbar />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/curriculum" element={<RoadmapPage />} />
          <Route path="/topic/:topicSlug" element={<LessonPage />} />
          <Route path="/practice" element={<WorkspacePage />} />
          <Route path="/practice/:questionSlug" element={<WorkspacePage />} />
          <Route path="/interview" element={<InterviewPage />} />
        </Routes>
      </main>
      {/* Hide footer on full-screen workspace page */}
      {!isWorkspace && <Footer />}
    </div>
  );
};

export function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
