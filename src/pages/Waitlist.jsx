import React from "react";
// import axios from "axios"
import { useState } from "react";

function Waitlist() {
  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header Section */}
      <div className="absolute top-0 left-0 right-0 z-50 p-4 md:p-6 flex justify-between items-center">
        {/* Logo at Top Left */}
        <img className="h-5 w-25 object-contain"
          src="../Goods/Alaba_Line.png" alt="AlabaLine" loading = "lazy"/>

        {/* Contact Us Button at Top Right */}
        <button className="px-3 py-1 md:px-4 md:py-2 rounded-lg text-sm md:text-base text-white font-semibold hover:bg-red-700 ring-1 ring-yellow-600">
          Contact Us
        </button>
      </div>

      {/* Hero Section */}
      <div
        className="relative w-full h-screen bg-cover bg-center flex items-center justify-start"
        style={{ backgroundImage: "url('../Goods/waitlist.jpeg')" }}
      >
        {/* Dark Overlay at Bottom and Left */}
        <div className="absolute inset-0 bg-black opacity-80">
          {/* Left Dark Overlay */}
          <div className="absolute top-0 left-0 w-1/3 h-full bg-gradient-to-r from-black to-transparent"></div>
          {/* Bottom Dark Overlay */}
          <div className="absolute bottom-0 left-0 w-full h-1/3 bg-gradient-to-t from-black to-transparent"></div>
        </div>
        <div className="absolute top-0 left-0 w-full  h-40 bg-gradient-to-b from-red-600 to-transparent opacity-70"></div>
        <div className="absolute bottom-0 left-0 w-full h-5 opacity-70" style={{ background: "radial-gradient(circle at center, rgba(185, 28, 28, 1), transparent)" }}></div>
        {/* Hero Content (Text on the Left) */}
        <div className="relative text-left px-4 md:px-6 w-full md:w-1/2 z-10">
          {/* Main Heading */}
          <p className="mt-4 text-base md:text-lg">Your Ultimate Marketplace for</p>
          <h1 className="text-3xl md:text-6xl font-bold text-yellow-300">
            Business Visibility, Smart and Exciting Shopping
          </h1>

          {/* Email Input & Button */}
          <div className="mt-6 flex flex-col md:flex-row justify-start gap-2 md:gap-4">
            <input
              type="email"
              placeholder="Email Address"
              className="px-4 py-2 md:px-4 md:py-3 w-full md:w-96 rounded-lg bg-black bg-opacity-50 text-white placeholder-gray-300 border border-gray-600 focus:outline-none focus:border-white border-yellow-500"
            />
            <button className="bg-red-600 px-4 py-2 md:px-6 md:py-3 rounded-lg text-white font-semibold hover:bg-red-700 border-yellow-600">
              Get Early Access
            </button>
          </div>
        </div>
      </div>

      {/* Why Choose Us */}
      <div className="relative py-16 px-4 bg-black text-center">
        {/* Reddish-Brown Glow Light at the Top */}
        <div className="absolute top-0 left-0 w-full h-20 bg-gradient-to-b from-[#992626] to-transparent opacity-90"></div>
        
        {/* Section Title */}
        <div className="text-center mb-10">
          <h2 className="text-yellow-400 text-4xl font-bold">Why Choose Us</h2>
          <div className="border-t border-gray-700 w-96 mx-auto mt-2"></div>
        </div>
        
        {/* Content Cards */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-[#1d0606a8] ring-1 ring-white rounded-xl p-8">
            <div className="flex flex-col md:flex-row items-start">
              {/* Left Column - For Vendors */}
              <div className="flex-1 pr-0 md:pr-8">
              <div className="bg-yellow-500 rounded-md py-2 px-4 w-fit mb-3">
                <h3 className="font-bold text-black ">For Vendors:</h3>
              </div>
                <h4 className="text-white text-xl mb-4 text-left">Expand your reach</h4>
                <ul className="space-y-4 text-gray-400 text-left">
                  <li className="flex items-start">
                    <span className="text-yellow-400 mr-2">•</span>
                    <span>AI-driven recommendations connect you with buyers actively looking for your products.</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-yellow-400 mr-2">•</span>
                    <span>Get discovered by the right customers with our powerful SEO.</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-yellow-400 mr-2">•</span>
                    <span>Build your brand, manage your store, and drive more sales effortlessly.</span>
                  </li>
                </ul>
              </div>
              
              {/* Vertical Divider */}
              <div className="hidden md:flex h-auto self-stretch mx-4">
                <div className="w-px bg-gray-300"></div>
              </div>
              
              {/* Right Column - For Customers */}
              <div className="flex-1 mt-8 md:mt-0 pl-0 md:pl-8">
                <div className="bg-yellow-500 rounded-md py-2 px-4 w-fit mb-3">
                  <h3 className="font-bold text-black">For Customers:</h3>
                </div>
                <h4 className="text-white text-xl mb-4 text-left">Shop smarter & faster</h4>
                <ul className="space-y-4 text-gray-400 text-left">
                  <li className="flex items-start">
                    <span className="text-yellow-400 mr-2">•</span>
                    <span>Scan products with your device to find the best vendors instantly.</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-yellow-400 mr-2">•</span>
                    <span>AI-powered suggestions help you discover trusted businesses selling what you need.</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-yellow-400 mr-2">•</span>
                    <span>Connect directly with suppliers for bulk or retail purchases.</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="relative py-8 md:py-12 bg-black text-center">
        <h2 className="relative text-3xl md:text-3xl font-bold text-white z-10">
          How It Works?
        </h2>
        <div className="relative mt-4 md:mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 max-w-5xl mx-auto px-4 md:px-0 z-10">
          <div className="p-4 md:p-6 bg-[#1d0606a8] rounded-lg">
            <h3 className="font-bold text-2xl text-[#fbb661]">Vendors</h3>
            <p>Create your store, list products, and connect with buyers.</p>
          </div>
          <div className="p-4 md:p-6 bg-[#1d0606a8] rounded-lg">
            <h3 className="font-bold text-2xl text-[#fbb661]">Customers</h3>
            <p>Search for products, scan items, and find the best vendors.</p>
          </div>
          <div className="p-4 md:p-6 bg-[#1d0606a8] rounded-lg">
            <h3 className="font-bold text-2xl text-[#fbb661]">Connect & Buy</h3>
            <p>Engage with sellers, compare options, and purchase wisely.</p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="py-4 md:py-6 bg-red-700 text-center">
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row justify-between items-center px-4 md:px-0">
          <div className="text-lg md:text-xl font-bold">alabaline</div>
          <div className="mt-2 md:mt-0">
            <p>Contact Us:</p>
            <p>Phone: [Your Phone] | Email: [Your Email] | Address: [Your Address]</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Waitlist;