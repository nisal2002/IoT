import React from 'react';
import { Train } from 'lucide-react';

const LoadingScreen = () => {
  return (
    <div 
      className="min-h-screen flex items-center justify-center"
      style={{
        backgroundImage: "url('https://static.independent.co.uk/2023/06/09/11/iStock-1433450737.jpg')",
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      }}
    >
      {/* Black overlay */}
      <div className="absolute inset-0 bg-black opacity-75 z-0"></div>

      {/* Loading box */}
      <div className="z-10 p-8 rounded-lg flex flex-col items-center">
        <Train className="text-white w-16 h-16 animate-bounce" />
        <h1 className="text-white text-3xl mt-4 font-bold">Loading...</h1>
      </div>
    </div>
  );
};

export default LoadingScreen;