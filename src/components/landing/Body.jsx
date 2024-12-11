import React from 'react';

function Body() {
  return (
    <div className="px-8 py-12 bg-gray-100">
      {/* Vendor Profiles Section */}
      <div className="text-center mb-12">
        <h2 className="text-4xl font-bold text-gray-800 mb-6">Top Vendor Profiles & Products</h2>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-12">
          {/* Vendor Profile Card */}
          {[...Array(9)].map((_, index) => (
            <div key={index} className="bg-white p-6 rounded-xl shadow-xl animate-gradient">
              <div className="flex items-center mb-4">
                <img
                  src={`https://randomuser.me/api/portraits/men/${index + 1}.jpg`}
                  alt="Vendor"
                  className="w-16 h-16 rounded-full mr-4"
                />
                <div>
                  <h3 className="font-semibold text-xl text-gray-700">Vendor {String.fromCharCode(65 + index)}</h3>
                  <p className="text-gray-500 text-sm">Best seller in {['electronics', 'home appliances', 'fashion', 'sports gear', 'books', 'toys', 'furniture', 'beauty products', 'groceries'][index]}</p>
                </div>
              </div>
              <p className="text-gray-400 text-sm">Date: {new Date().toLocaleDateString()}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Exclusive Offer Section */}
      <div className="bg-white/50 text-black text-center py-12 mt-12 rounded-xl shadow-black shadow-md">
        <h2 className="text-3xl font-bold mb-4">Exclusive Offer!</h2>
        <p className="text-lg mb-8">Don't miss out on our limited-time discounts. Upgrade your style with our exclusive collection at unbeatable prices.</p>
        <button className="bg-red-700 hover:bg-red-500 text-white py-3 px-8 rounded-lg text-lg transition-all duration-300">
          Shop Now
        </button>
      </div>
    </div>
  );
}

export default Body;
