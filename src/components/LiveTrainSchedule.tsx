import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Train, ArrowUpDown, Search, Calendar } from 'lucide-react';

const stations = [
  'Colombo Fort',
  'Maradana',
  'Dematagoda',
  'Kelaniya',
  'Ragama',
  'Gampaha',
  'Veyangoda',
  'Polgahawela',
  'Kandy'
];

const LiveTrainSchedule = () => {
  const navigate = useNavigate();
  const [startStation, setStartStation] = useState('');
  const [endStation, setEndStation] = useState('');
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);

  const handleExchange = () => {
    const temp = startStation;
    setStartStation(endStation);
    setEndStation(temp);
  };
    

  const handleSearch = () => {
    navigate('/schedule-results', {
      state: {
        startStation,
        endStation,
        selectedDate
      }
    });
  };
  

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
            Live Train Schedule
          </h1>
        </div>
      </div>
      <div className="w-3/4 bg-gradient-to-r from-blue-300 to-green-300 p-10 flex flex-col items-center justify-center">
        <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-2xl">
          <div className="flex flex-col space-y-6">
            <div className="flex items-center space-x-4">
              <div className="flex-1">
                <label className="block text-sm font-bold mb-2" htmlFor="startStation">
                  Start Station
                </label>
                <select
                  id="startStation"
                  value={startStation}
                  onChange={(e) => setStartStation(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select Station</option>
                  {stations.map((station) => (
                    <option key={station} value={station}>{station}</option>
                  ))}
                </select>
              </div>
              
              <button
                onClick={handleExchange}
                className="bg-blue-500 hover:bg-blue-600 text-white p-3 rounded-full mt-6 transition-all duration-200 transform hover:scale-110"
              >
                <ArrowUpDown size={24} />
              </button>
              
              <div className="flex-1">
                <label className="block text-sm font-bold mb-2" htmlFor="endStation">
                  End Station
                </label>
                <select
                  id="endStation"
                  value={endStation}
                  onChange={(e) => setEndStation(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select Station</option>
                  {stations.map((station) => (
                    <option key={station} value={station}>{station}</option>
                  ))}
                </select>
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-bold mb-2" htmlFor="date">
                Date
              </label>
              <div className="relative">
                <Calendar className="absolute left-3 top-3 text-gray-400" size={20} />
                <input
                  type="date"
                  id="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  className="w-full p-3 pl-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>
            
            <button
              onClick={handleSearch}
              disabled={!startStation || !endStation || startStation===endStation}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-lg text-xl transition-all duration-200 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Search size={24} />
              <span>Search Trains</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LiveTrainSchedule;