import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "./style_hero.css";

function Hero() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen grid grid-cols-1 md:grid-cols-2 bg-gray-100">
      {/* Left Side - Welcome Text & Button */}
      <motion.div
        className="p-10 flex flex-col justify-center items-start space-y-8"
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 1.2, ease: "easeOut" }}
      >
        {/* Text Content */}
        <motion.div
          className="space-y-4 text-center lg:text-left "
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 1.2, ease: "easeOut" }}
        >
          <div className="shadow-xl shadow-black p-5  rounded-xl animate-gradient">
            <h1 className="text-4xl md:text-6xl font-bold p-5 text-gray-900">
              Welcome to the Future
            </h1>
            <p className="text-lg md:text-2xl text-gray-600 p-2">
              Explore a world of possibilities with our cutting-edge products and
              exclusive deals.
            </p>
            <motion.button
              onClick={() => navigate("/product")}
              className="bg-red-600 hover:bg-red-700 text-white py-3 px-8 rounded-lg text-lg shadow-lg transition-all duration-300"
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
            >
              Shop Now
            </motion.button>
          </div>
        </motion.div>
      </motion.div>

      {/* Right Side - Slider */}
      <motion.div
        className="relative flex justify-center items-center m-5"
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        <div className="slider w-5/6 h-3/4 bg-gray-100 rounded-3xl shadow-xl shadow-black flex justify-center items-center">
          
        </div>
      </motion.div>
    </div>
  );
}

export default Hero;
