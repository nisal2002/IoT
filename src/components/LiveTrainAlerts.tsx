import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Train } from 'lucide-react';

const LiveTrainAlerts = () => {
  const navigate = useNavigate();

  return (
    <div className="flex h-[calc(100vh-64px)]">
      <div 
        className="w-1/4 bg-cover bg-center bg-opacity-50"
        style={{
          backgroundImage: "url('https://static2.tripoto.com/media/filter/tst/img/38619/TripDocument/1641540662_img_20211224_165331.jpg')"
        }}
      >
        <div className="h-full flex items-center justify-center">
          <h1 className="text-3xl font-bold text-white bg-black bg-opacity-75 p-5 rotate-[-90deg] rounded-lg">
            Live Train Alerts
          </h1>
        </div>
      </div>
      <div className="w-3/4 bg-gradient-to-r from-blue-300 to-green-300 p-10 flex flex-col justify-center space-y-5">
        <button
          onClick={() => navigate('/main-line-alerts')}
          className="bg-red-600 hover:bg-red-700 text-white p-4 rounded-lg text-xl transition-all w-full max-w-md mx-auto"
        >
          <span className="text-xl">Main Line</span> <br/>
          <span className="text-sm text-yellow-400">Colombo Fort to Badulla</span>
        </button>
        <button
          className="bg-red-600 hover:bg-red-700 text-white p-4 rounded-lg text-xl transition-all w-full max-w-md mx-auto"
        >
          <span className="text-xl">Puttalam Line</span> <br/>
          <span className="text-sm text-yellow-400">Colombo Fort to Puttalama and Noornagar</span>
        </button>
        <button
          className="bg-red-600 hover:bg-red-700 text-white p-4 rounded-lg text-xl transition-all w-full max-w-md mx-auto"
        >
          <span className="text-xl">Coastal Line</span> <br/>
          <span className="text-sm text-yellow-400">Colombo Fort to Galle / Mathara and Beliaththa</span>
        </button>
        <button
          className="bg-red-600 hover:bg-red-700 text-white p-4 rounded-lg text-xl transition-all w-full max-w-md mx-auto"
        >
          <span className="text-xl">Kelani Valley Line</span> <br/>
          <span className="text-sm text-yellow-400">Colombo Fort to Awissawella</span>
        </button>
        <button
          className="bg-red-600 hover:bg-red-700 text-white p-4 rounded-lg text-xl transition-all w-full max-w-md mx-auto"
        >
          <span className="text-xl">Other Lines</span> <br/>
          <span className="text-sm text-yellow-400">Colombo Fort to Matale / Madakalapuwa / Trincomalee</span>
        </button>
      </div>
    </div>
  );
};

export default LiveTrainAlerts;