import React, { useEffect, useRef } from "react";

function Footer() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    // Set canvas dimensions
    canvas.width = window.innerWidth;
    canvas.height = 150; // Adjust the height as needed

    // Draw the wave shape
    ctx.fillStyle = "#1F2937"; // Background color of the wave
    ctx.beginPath();
    ctx.moveTo(0, 100); // Start at the bottom left
    ctx.quadraticCurveTo(canvas.width / 2, -50, canvas.width, 100); // Create wave
    ctx.lineTo(canvas.width, canvas.height); // Bottom-right corner
    ctx.lineTo(0, canvas.height); // Bottom-left corner
    ctx.closePath();
    ctx.fill();
  }, []);

  return (
    <div className="relative bg-gray-800 text-white">
      {/* Canvas for the wavy background */}
      <canvas
        ref={canvasRef}
        className="absolute top-0 left-0 w-full h-full"
        style={{ zIndex: -1 }}
      ></canvas>

      {/* Footer Content */}
      <div className="container mx-auto px-4 py-8">
        {/* Newsletter Section */}
        <div className="text-center md:flex md:justify-between md:items-center mb-8">
          <h3 className="text-lg font-semibold mb-4 md:mb-0">
            Subscribe to our newsletter
          </h3>
          <div className="flex items-center justify-center">
            <input
              type="email"
              placeholder="Input your email"
              className="px-4 py-2 rounded-l-lg text-gray-900 focus:outline-none"
            />
            <button className="bg-red-700 hover:bg-red-600 text-white py-2 px-4 rounded-r-lg transition-all">
              Subscribe
            </button>
          </div>
        </div>

        {/* Branding and Navigation */}
        <div className="flex flex-col md:flex-row md:justify-between md:items-start">
          <div className="mb-6 md:mb-0">
            <h2 className="text-2xl font-bold">AlabaLine</h2>
          </div>
          <div className="flex flex-wrap justify-center space-x-4 md:space-x-8">
            <a href="#" className="text-sm hover:underline">
              Pricing
            </a>
            <a href="#" className="text-sm hover:underline">
              About us
            </a>
            <a href="#" className="text-sm hover:underline">
              Features
            </a>
            <a href="#" className="text-sm hover:underline">
              Help Center
            </a>
            <a href="#" className="text-sm hover:underline">
              Contact us
            </a>
            <a href="#" className="text-sm hover:underline">
              FAQs
            </a>
            <a href="#" className="text-sm hover:underline">
              Careers
            </a>
          </div>
        </div>

        {/* Language Selector */}
        <div className="mt-6 md:mt-8 flex justify-center md:justify-between items-center">
          <select className="bg-gray-800 text-sm text-white py-2 px-3 rounded">
            <option value="en">English</option>
          </select>
          <p className="text-xs px-5 mt-4 md:mt-0 text-gray-400">
            &copy; 2024 Brand, Inc. • Privacy • Terms • Sitemap
          </p>
        </div>

        {/* Social Media */}
        <div className="flex justify-center space-x-4 mt-4">
          <a href="#" className="text-gray-400 hover:text-white">
            <i className="fab fa-twitter"></i>
          </a>
          <a href="#" className="text-gray-400 hover:text-white">
            <i className="fab fa-facebook"></i>
          </a>
          <a href="#" className="text-gray-400 hover:text-white">
            <i className="fab fa-linkedin"></i>
          </a>
          <a href="#" className="text-gray-400 hover:text-white">
            <i className="fab fa-youtube"></i>
          </a>
        </div>
      </div>
    </div>
  );
}

export default Footer;
