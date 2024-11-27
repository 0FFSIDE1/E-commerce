import React from 'react';
import { FaShoppingCart, FaUserCircle } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

function NavBar() {
  const navigate = useNavigate();

  return (
    <nav className="bg-gradient-to-r from-[#F4F1F8] to-[#dac2cc] hover:from-[#EAE7F3] hover:to-[#D6D1E8] transition-all duration-700 ease-in-out text-gray-800 shadow-md flex items-center justify-between py-4 px-6">
      {/* Logo */}
      <div
        className="font-extrabold text-3xl cursor-pointer hover:text-gray-300"
        onClick={() => navigate("/")}
      >
        AlabaLine
      </div>

      {/* Search Bar */}
      <div className="flex-1 flex justify-center">
        <input
          type="text"
          placeholder="Search Products..."
          className="sm:w-10/12 lg:w-3/5 p-3 rounded-full border-none shadow-md outline-none text-gray-800 focus:ring-2 focus:ring-purple-400"
        />
      </div>

      {/* Icons */}
      <div className="flex gap-6">
        <FaShoppingCart
          className="text-2xl cursor-pointer hover:scale-110 transition-transform duration-300"
          title="Cart"
        />
        <FaUserCircle
          className="text-2xl cursor-pointer hover:scale-110 transition-transform duration-300"
          title="Profile"
        />
      </div>
    </nav>
  );
}

export default NavBar;
