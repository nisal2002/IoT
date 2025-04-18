import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation, useNavigate } from 'react-router-dom';
import { Train, ArrowLeft } from 'lucide-react';
import LoadingScreen from './components/LoadingScreen';
import MainPage from './components/MainPage';
import LiveTrainAlerts from './components/LiveTrainAlerts';
import MainLineAlerts from './components/MainLineAlerts';
import LiveTrainSchedule from './components/LiveTrainSchedule';
import ScheduleResults from './components/ScheduleResults';

function NavigationHeader() {
  const location = useLocation();
  const navigate = useNavigate();
  const showBackButton = location.pathname !== '/';

  // State to store current date and time
  const [dateTime, setDateTime] = useState({
    date: new Date().toLocaleDateString(),
    time: new Date().toLocaleTimeString(),
  });

  // Update the time every second
  useEffect(() => {
    const interval = setInterval(() => {
      setDateTime({
        date: new Date().toLocaleDateString(),
        time: new Date().toLocaleTimeString(),
      });
    }, 1000); // Update every second

    return () => clearInterval(interval); // Cleanup interval on component unmount
  }, []);

  return (
    <header className="bg-black text-white p-4 flex justify-between items-center">
      <div className="flex items-center gap-4">
        {showBackButton && (
          <button onClick={() => navigate(-1)} className="hover:text-gray-300">
            <ArrowLeft size={24} />
          </button>
        )}
        <Link to="/" className="flex items-center gap-2 hover:text-gray-300">
          <Train size={50} />
          <span className="font-bold">Network of Railway Passengers Sri Lanka</span>
        </Link>
      </div>
      <div className="text-center">
        {dateTime.date} <br />
        {dateTime.time}
      </div>
    </header>
  );
}

function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(false);
    }, 3000);

    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <NavigationHeader />
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route path="/live-alerts" element={<LiveTrainAlerts />} />
          <Route path="/main-line-alerts" element={<MainLineAlerts />} />
          <Route path="/live-train-schedule" element={<LiveTrainSchedule />} />
          <Route path="/schedule-results" element={<ScheduleResults />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
