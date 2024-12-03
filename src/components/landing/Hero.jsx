import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "./style_hero.css";

function Hero() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 mb-3 bg-gradient-to-br from-blue-700 via-gray-500 to-red-900 shadow-lg animate-gradient">
      {/* Left Side - Welcome Text & Button */}
      <motion.div
        className="bg-white/10 backdrop-blur-md rounded-2xl m-10 shadow-[0_0_10px_black] animate-gradient relative text-white flex flex-col justify-center items-start px-8 space-y-8 bg-gradient-to-br from-blue-700 via-gray-700 to-red-800"
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 1.2, ease: "easeOut" }}
      >
        {/* Background Glow */}
        <div className="absolute top-0 left-0 w-full h-full opacity-50 z-0">
          <div className="futuristic-glow"></div>
        </div>

        {/* Text Content */}
        <motion.div
          className="relative  z-10 space-y-4 text-center lg:text-left"
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 1.2, ease: "easeOut" }}
        >
          <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-red-400 via-yellow-500 to-red-400 bg-clip-text text-transparent animate-gradient">
            Welcome to the Future
          </h1>
          <p className="text-lg md:text-2xl">
            Explore a world of possibilities with our cutting-edge products and
            exclusive deals.
          </p>
          <motion.button
            onClick={() => navigate("/product")}
            className="bg-red-600 hover:bg-red-700 text-white py-3 px-8 rounded-lg text-lg shadow-md transition-all duration-300"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
          >
            Shop Now
          </motion.button>
        </motion.div>
      </motion.div>

      {/* Desktop View - Slider */}
      <motion.div
        className="relative slider rounded-3xl shadow-[0_0_15px_black] mt-1 py-8"
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        {/* <div className="absolute w-full h-full top-0 left-0 bg-black/50 z-10"></div> */}
        <div className="slider-images relative z-0">
          {/* Add your desktop slider images or content here */}
          
        </div>
      </motion.div>

      {/* Mobile View - Slide
      <motion.div
        className="relative slider lg:hidden rounded-3xl shadow-[0_0_15px_black] mt-1 py-8"
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        <div className="absolute w-full h-full top-0 left-0 bg-black/50 z-10"></div>
        <div className="slider-images relative z-0 text-center text-white space-y-4">
          <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-red-400 via-yellow-500 to-red-400 bg-clip-text text-transparent animate-gradient">
            Welcome to the Future
          </h1>
          <p className="text-lg md:text-2xl">
            Explore a world of possibilities with our cutting-edge products and
            exclusive deals.
          </p>
          <motion.button
            onClick={() => navigate("/products")}
            className="bg-red-600 hover:bg-red-700 text-white py-3 px-8 rounded-lg text-lg shadow-md transition-all duration-300"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
          >
            Shop Now
          </motion.button>
        </div>
      </motion.div> */}
    </div>
  );
}

export default Hero;
