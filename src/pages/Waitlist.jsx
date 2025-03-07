import React, { useState } from "react";
import axios from "axios";
import { Facebook, Instagram, Twitter } from 'lucide-react'

function Waitlist() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Reset previous messages
    setMessage('');
    setMessageType('');

    // Check if email is empty
    if (!email.trim()) {
      setMessage('Please enter an email address');
      setMessageType('error');
      setTimeout(() => setMessage(''), 5000);
      return;
    }

    // Validate email format
    if (!validateEmail(email)) {
      setMessage('Please enter a valid email address');
      setMessageType('error');
      setTimeout(() => setMessage(''), 5000);
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/v1/vendor/waitlist", {
        email: email.trim(),
      });

      // Handle successful submission
      setMessage(response.data?.message || 'Thank you for joining our waitlist!');
      setMessageType('success');
      setEmail('');

      setTimeout(() => setMessage(''), 5000);
    } catch (error) {
      // Handle error from backend
      let errorMsg = "Email already exist. Please try another.";

      if (error.response && error.response.data) {
        // If the backend provides an error message, use it
        errorMsg = error.response.email?.message|| errorMsg;
      } else if (error.request) {
        // No response from server
        errorMsg = "Please check your connection.";
      }

      setMessage(errorMsg);
      setMessageType('error');
      
      setTimeout(() => setMessage(''), 5000);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header Section */}
      <div className="absolute top-0 left-0 right-0 z-50 p-4 md:p-6 flex justify-between items-center">
        {/* Logo at Top Left */}
        <img 
          className="h-5 w-auto object-contain"
          src="../Goods/Alaba_Line.png" 
          alt="AlabaLine" 
          loading="lazy"
        />

        {/* Contact Us Button at Top Right */}
        <button className="px-3 py-1 md:px-4 md:py-2 rounded-lg text-sm md:text-base text-white font-semibold hover:bg-red-700 ring-1 ring-yellow-600 transition-all duration-200 active:scale-100">
          Contact Us
        </button>
      </div>

      {/* Hero Section */}
      <div
        className="relative w-full min-h-screen bg-cover bg-center flex items-center justify-start"
        style={{ backgroundImage: "url('../Goods/waitlist.jpeg')" }}
      >
        {/* Dark Overlay at Bottom and Left */}
        <div className="absolute inset-0 bg-black opacity-80">
          {/* Left Dark Overlay */}
          <div className="absolute top-0 left-0 w-1/3 h-full bg-gradient-to-r from-black to-transparent"></div>
          {/* Bottom Dark Overlay */}
          <div className="absolute bottom-0 left-0 w-full h-1/3 bg-gradient-to-t from-black to-transparent"></div>
        </div>
        <div className="absolute top-0 left-0 w-full h-40 bg-gradient-to-b from-red-600 to-transparent opacity-70"></div>
        <div className="absolute bottom-0 left-0 w-full h-5 opacity-70" style={{ background: "radial-gradient(circle at center, rgba(185, 28, 28, 1), transparent)" }}></div>
        
        {/* Hero Content (Text on the Left) */}
        <div className="relative text-left px-4 md:px-6 w-full lg:w-3/5 xl:w-1/2 z-10 py-20 md:py-0">
          {/* Main Heading */}
          <p className="mt-4 text-base md:text-lg">Your Ultimate Marketplace for</p>
          <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-bold text-yellow-300 mb-6">
            Business Visibility, Smart and Exciting Shopping
          </h1>

          {/* Email Input & Button */}
          <form onSubmit={handleSubmit} className="mt-6 flex flex-col sm:flex-row justify-start gap-6 sm:gap-4 w-full max-w-xl">
            <div className="flex-grow relative w-full">
              <input
                type="email"
                placeholder="Email Address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="px-4 py-2 md:px-4 md:py-3 w-full rounded-lg bg-black bg-opacity-50 text-white 
                          placeholder-gray-300 border border-gray-600 focus:outline-none focus:border-white 
                          border-yellow-500"
              />
              {/* Message Container - Fixed Height to Prevent Button Shift */}
              <div className="absolute left-0 mt-1 w-full min-h-[18px]">
                {message && (
                  <p className={`text-sm ${messageType === 'error' ? 'text-red-500' : 'text-green-500'}`}>
                    {message}
                  </p>
                )}
              </div>
            </div>

            <button 
              type="submit"
              className="bg-red-600 px-4 py-2 md:px-6 md:py-3 rounded-lg text-white font-semibold 
                        hover:bg-red-700 border border-yellow-600 transition-colors duration-200 
                        sm:w-auto w-full whitespace-nowrap">
              Get Early Access
            </button>
          </form>
        </div>
      </div>

      {/* Why Choose Us */}
      <div className="relative py-16 px-4 bg-black text-center">
        {/* Reddish-Brown Glow Light at the Top */}
        <div className="absolute top-0 left-0 w-full h-20 bg-gradient-to-b from-[#992626] to-transparent opacity-90"></div>
        
        {/* Section Title */}
        <div className="text-center mb-10">
          <h2 className="text-yellow-400 text-3xl md:text-4xl font-bold">Why Choose Us</h2>
          <div className="border-t border-gray-700 w-48 sm:w-64 md:w-96 mx-auto mt-2"></div>
        </div>
        
        {/* Content Cards */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-[#1d0606a8] ring-1 ring-white rounded-xl p-4 md:p-8">
            <div className="flex flex-col md:flex-row items-start">
              {/* Left Column - For Vendors */}
              <div className="flex-1 pr-0 md:pr-8">
                <div className="bg-yellow-500 rounded-md py-2 px-4 w-fit mb-3">
                  <h3 className="font-bold text-black">For Vendors:</h3>
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
        <div className="max-w-5xl px-5 py-6 mx-auto flex flex-col md:flex-row justify-between items-center px-4 md:px-0">
          <img 
            className="h-10 w-auto object-contain"
            src="../Goods/Alaba_lines.png" 
            alt="AlabaLine" 
            loading="lazy"
          />
          <div className="flex space-x-4 mt-3">
            <a href="#" className="text-white hover:text-gray-400 transition-colors duration-200">
              <Facebook size={28} />
            </a>
            <a href="#" className="text-white hover:text-gray-400 transition-colors duration-200">
              <Instagram size={28} />
            </a>
            <a href="#" className="text-white hover:text-gray-400 transition-colors duration-200">
              <Twitter size={28} />
            </a>
          </div>
          <div className="mt-2 md:mt-0">
            <p>Contact Us:</p>
            {/* <p className="text-sm md:text-base">Phone: [Your Phone] | Email: [Your Email] | Address: [Your Address]</p> */}
          </div>
        </div>
      </footer>
    </div>
  );
}

export default Waitlist;