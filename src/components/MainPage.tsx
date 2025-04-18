import React from 'react';
import { useNavigate } from 'react-router-dom';

const MainPage = () => {
  const navigate = useNavigate();

  return (
    <div className="flex h-[calc(100vh-64px)]">
      <div 
        className="w-1/4 bg-cover bg-center"
        style={{
          backgroundImage: "url('https://static.toiimg.com/thumb/114038991/114038991.jpg?height=746&width=420&resizemode=76&imgsize=126926')"
        }}
      />
      <div className="w-3/4 bg-gradient-to-r from-blue-300 to-green-300 p-10">
        <div className="grid grid-cols-3 gap-6 h-full place-content-center">
          <button
            className="bg-green-800 hover:bg-gray-700 text-white p-8 rounded-lg flex flex-col items-center transition-all overflow-hidden"
          >
            <div 
              className="w-full h-40 bg-cover bg-center mb-4 rounded-lg"
              style={{
                backgroundImage: "url('https://img.freepik.com/premium-vector/content-creators-illustration-clip-art-template-set-digital-development-multimedia-recording-design_609667-611.jpg')"
              }}
            />
            <span className="text-xl">Main News Feed</span>
          </button>
          <button
            onClick={() => navigate('/live-alerts')}
            className="bg-green-800 hover:bg-gray-700 text-white p-8 rounded-lg flex flex-col items-center transition-all overflow-hidden"
          >
            <div 
              className="w-full h-40 bg-cover bg-center mb-4 rounded-lg"
              style={{
                backgroundImage: "url('https://www.shutterstock.com/shutterstock/photos/2180859535/display_1500/stock-vector-important-announcement-attention-or-warning-information-breaking-news-or-urgent-message-2180859535.jpg')"
              }}
            />
            <span className="text-xl">Live Train Alerts</span>
          </button>
          <button
            onClick={() => navigate('/live-train-schedule')}
            className="bg-green-800 hover:bg-gray-700 text-white p-8 rounded-lg flex flex-col items-center transition-all overflow-hidden"
          >
            <div 
              className="w-full h-40 bg-cover bg-center mb-4 rounded-lg"
              style={{
                backgroundImage: "url('https://img.freepik.com/free-vector/schedule-concept-illustration_114360-1531.jpg')"
              }}
            />
            <span className="text-xl">Live Train Schedule </span>
          </button>
          <button
            className="bg-green-800 hover:bg-gray-700 text-white p-8 rounded-lg flex flex-col items-center transition-all overflow-hidden"
          >
            <div 
              className="w-full h-40 bg-cover bg-center mb-4 rounded-lg"
              style={{
                backgroundImage: "url('https://cdn1.vectorstock.com/i/1000x1000/99/05/radar-vector-21989905.jpg')"
              }}
            />
            <span className="text-xl">Live Train Radar</span>
          </button>
          <button
            className="bg-green-800 hover:bg-gray-700 text-white p-8 rounded-lg flex flex-col items-center transition-all overflow-hidden"
          >
            <div 
              className="w-full h-40 bg-cover bg-center mb-4 rounded-lg"
              style={{
                backgroundImage: "url('https://media.istockphoto.com/id/1394558163/vector/three-multiracial-women-passengers-enjoy-airplane-flight-while-reading-and-using-smartphone.webp?b=1&s=612x612&w=0&k=20&c=kjtphE1KpBWbXlUAjTijvFK7FPD77RHpbcv4qleIaRw=')"
              }}
            />
            <span className="text-xl">Seat Reservation</span>
          </button>
          <button
            className="bg-green-800 hover:bg-gray-700 text-white p-8 rounded-lg flex flex-col items-center transition-all overflow-hidden"
          >
            <div 
              className="w-full h-40 bg-cover bg-center mb-4 rounded-lg"
              style={{
                backgroundImage: "url('https://media.istockphoto.com/id/2014869742/vector/hand-with-passport-and-ticket-vector-illustration.jpg?s=612x612&w=0&k=20&c=R-SHkvKhpT91Mfml4UIWt0nI1UT_-LBvDLBHis_zklo=')"
              }}
            />
            <span className="text-xl">Ticket Prices</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default MainPage;