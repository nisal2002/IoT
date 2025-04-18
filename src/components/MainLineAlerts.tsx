import React, { useEffect, useState } from 'react';

type Alert = {
  id: number;
  message: string;
  time: string;
};

const MainLineAlerts = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    const fetchAlerts = () => {
      fetch('src/data/mainlinealerts.json')
        .then(response => response.json())
        .then(data => setAlerts(data))
        .catch(error => console.error('Error fetching alerts:', error));
    };

    fetchAlerts();

    // Set an interval to fetch data every 1 seconds
    const intervalId = setInterval(fetchAlerts, 1000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-300 to-green-300 flex flex-col items-center p-8">
      <div className="flex items-center gap-4 mb-8 text-center">
        <h1 className="text-3xl font-bold">Main Line Alerts</h1>
      </div>
      <div className="space-y-4 w-full max-w-3xl">
        {alerts.length > 0 ? (
          [...alerts].reverse().map(alert => (
            <div key={alert.id} className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex flex-col">
                <p className="text-black text-lg">{alert.message}</p>
                <span className="text-sm text-gray-500 mt-2">{alert.time}</span>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center text-gray-500">No alerts available.</div>
        )}
      </div>
    </div>
  );
};

export default MainLineAlerts;
