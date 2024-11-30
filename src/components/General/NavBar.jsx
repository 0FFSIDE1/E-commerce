import React from 'react';
import { FaShoppingCart, FaUserCircle } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

function NavBar() {
  const navigate = useNavigate();

  return (
    <nav className="bg-gradient-to-r from-[#f9f8fb] to-[#f4d7e3] hover:from-[#EAE7F3] hover:to-[#D6D1E8] transition-all duration-700 ease-in-out text-gray-800 shadow-md flex flex-col sm:flex-row items-center justify-between py-4 px-6">
      {/* Logo */}
      <div
        className="font-extrabold text-2xl sm:text-3xl cursor-pointer hover:text-gray-600 text-red-700"
        onClick={() => navigate("/")}
      >
        AlabaLine
      </div>

      {/* Collections and Add Vendors */}
      <div className="px-4 mt-4 sm:mt-0 flex flex-row sm:flex-row gap-4 sm:gap-6 items-center">
        <button
          onClick={() => navigate("#")}
          className="px-4 py-2 font-bold rounded-lg shadow-lg text-white transition duration-300 bg-red-700 ring ring-red-700"
        >
          Collections
        </button>
        <button
          onClick={() => navigate("#")}
          className=" basis-1/2 px-4 py-2 text-white font-bold rounded-lg shadow-lg transition duration-300 ring ring-red-700"
        >
          Vendors
        </button>
      </div>

      {/* Search Bar */}
      <div className="w-full sm:flex-1 mt-4 sm:mt-0 flex justify-center">
        <input
          type="text"
          placeholder="Search Products..."
          className="w-full sm:w-10/12 lg:w-3/5 p-3 rounded-full border-none shadow-md outline-none text-gray-800 focus:ring-2 focus:ring-purple-400"
        />
      </div>

      {/* Icons */}
      <div className="mt-4 sm:mt-0 flex gap-6 items-center">
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
