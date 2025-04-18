    import React, { useState, useEffect } from 'react';
    import { useLocation } from 'react-router-dom';
    import { Train, Clock, Calendar } from 'lucide-react';

    const trainData = [
      {
        id: 1,
        name: "S14-Udarata Menike",
        type: "Express",
        platform: "1",
        route: [
          { station: "Colombo Fort", arrivalTime: null, departureTime: "06:00" },
          { station: "Maradana", arrivalTime: "06:10", departureTime: "06:12" },
          { station: "Ragama", arrivalTime: "06:30", departureTime: "06:32" },
          { station: "Gampaha", arrivalTime: "06:45", departureTime: "06:47" },
          { station: "Polgahawela", arrivalTime: "07:45", departureTime: "07:47" },
          { station: "Kandy", arrivalTime: "09:00", departureTime: null }
        ]
      },
      {
        id: 2,
        name: "S14-Podi Menike",
        type: "Express",
        platform: "2",
        route: [
          { station: "Colombo Fort", arrivalTime: null, departureTime: "07:30" },
          { station: "Maradana", arrivalTime: "07:40", departureTime: "07:42" },
          { station: "Kelaniya", arrivalTime: "07:55", departureTime: "07:57" },
          { station: "Ragama", arrivalTime: "08:10", departureTime: "08:12" },
          { station: "Gampaha", arrivalTime: "08:30", departureTime: "08:32" },
          { station: "Veyangoda", arrivalTime: "09:00", departureTime: null }
        ]
      },
      {
        id: 3,
        name: "Intercity",
        type: "Intercity",
        platform: "3",
        route: [
          { station: "Gampaha", arrivalTime: null, departureTime: "08:15" },
          { station: "Ragama", arrivalTime: "08:35", departureTime: "08:37" },
          { station: "Kelaniya", arrivalTime: "08:50", departureTime: "08:52" },
          { station: "Dematagoda", arrivalTime: "09:10", departureTime: "09:12" },
          { station: "Maradana", arrivalTime: "09:25", departureTime: "09:27" },
          { station: "Colombo Fort", arrivalTime: "09:45", departureTime: null }
        ]
      },
      {
        id: 4,
        name: "S12-Tikiri Menike",
        type: "Intercity",
        platform: "1",
        route: [
          { station: "Colombo Fort", arrivalTime: null, departureTime: "09:00" },
          { station: "Maradana", arrivalTime: "09:10", departureTime: "09:12" },
          { station: "Gampaha", arrivalTime: "09:45", departureTime: "09:47" },
          { station: "Polgahawela", arrivalTime: "10:30", departureTime: null }
        ]
      }
    ];

    const ScheduleResults = () => {
      const location = useLocation();
      const { startStation, endStation, selectedDate } = location.state || {};

      const [predictedArrivals, setPredictedArrivals] = useState<any[]>([]);

      // Function to get relevant trains
      const getRelevantTrains = () => {
        return trainData.filter(train => {
          const startStationIndex = train.route.findIndex(stop => stop.station === startStation);
          const endStationIndex = train.route.findIndex(stop => stop.station === endStation);
          return startStationIndex !== -1 && endStationIndex !== -1 && startStationIndex < endStationIndex;
        }).map(train => {
          const startStationStop = train.route.find(stop => stop.station === startStation);
          const endStationStop = train.route.find(stop => stop.station === endStation);
          return {
            ...train,
            departureTime: startStationStop?.departureTime || startStationStop?.arrivalTime,
            arrivalTime: endStationStop?.arrivalTime || endStationStop?.departureTime
          };
        });
      };

      const relevantTrains = getRelevantTrains();

      // Fetch predicted arrival times from Flask API
      const fetchPredictedArrival = async (train: any, selectedDate: string) => {
        const payload = {
          "Train ID": train.name,
          "Station Name": endStation,
          "Arrival Time": train.arrivalTime,
          "Date": selectedDate,
        };

        try {
          const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
          });

          const data = await response.json();
          if (data.predicted_arrival_time) {
            return data.predicted_arrival_time;
          } else {
            throw new Error("Prediction failed");
          }
        } catch (error) {
          console.error('Error fetching prediction:', error);
          return 'N/A';
        }
      };

      // Update predicted arrivals when relevantTrains changes
      useEffect(() => {
        const updatePredictedArrivals = async () => {
          const updatedPredictions = await Promise.all(
            relevantTrains.map(async (train) => {
              const predictedArrival = await fetchPredictedArrival(train, selectedDate);
              return { trainId: train.id, predictedArrival };
            })
          );
          setPredictedArrivals(updatedPredictions);
        };

        updatePredictedArrivals();
      }, [relevantTrains, selectedDate]);

      return (
        <div className="min-h-[calc(100vh-64px)] bg-gradient-to-r from-blue-300 to-green-300 p-8">
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <h2 className="text-2xl font-bold">Train Schedule</h2>
                </div>
                <div className="flex items-center space-x-2 text-gray-600">
                  <Calendar size={20} />
                  <span>{new Date(selectedDate).toLocaleDateString()}</span>
                </div>
              </div>

              <div className="flex items-center justify-between bg-gray-50 p-4 rounded-lg">
                <div>
                  <p className="text-sm text-gray-500">From</p>
                  <p className="text-lg font-semibold">{startStation}</p>
                </div>
                <div className="text-blue-600">
                  <Train size={24} />
                </div>
                <div>
                  <p className="text-sm text-gray-500">To</p>
                  <p className="text-lg font-semibold">{endStation}</p>
                </div>
              </div>
            </div>

            {relevantTrains.length === 0 ? (
              <div className="bg-white rounded-xl shadow-lg p-6 text-center">
                <p className="text-xl text-gray-600">No direct trains found for this route.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {relevantTrains.map((train) => {
                  const predictedArrival = predictedArrivals.find(p => p.trainId === train.id)?.predictedArrival;
                  return (
                    <div key={train.id} className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
                      <div className="flex justify-between items-center">
                        <div>
                          <h3 className="text-xl font-bold text-gray-800">{train.name}</h3>
                          <span className="text-sm text-gray-500">Type: {train.type}</span>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-gray-500">Platform</p>
                          <p className="text-lg font-bold text-blue-600">{train.platform}</p>
                        </div>
                      </div>

                      <div className="mt-4 flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          <div>
                            <p className="text-sm text-gray-500">Departure</p>
                            <div className="flex items-center space-x-1">
                              <Clock size={16} className="text-gray-400" />
                              <p className="font-semibold">{train.departureTime}</p>
                            </div>
                          </div>
                          <div>
                            <p className="text-sm text-gray-500">Arrival</p>
                            <div className="flex items-center space-x-1">
                              <Clock size={16} className="text-gray-400" />
                              <p className="font-semibold">{train.arrivalTime}</p>
                            </div>
                          </div>
                          <div>
                            <p className="text-sm text-gray-500">Predicted Arrival</p>
                            <div className="flex items-center space-x-1">
                              <Clock size={16} className="text-gray-400" />
                              <p className="font-semibold">{predictedArrival || 'Loading...'}</p>
                            </div>
                          </div>
                        </div>
                        <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
                          Book Now
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      );
    };

    export default ScheduleResults;