import { motion } from "framer-motion";
import './style_hero.css';
import { useNavigate } from "react-router-dom";

function Hero() {
    const navigate = useNavigate();

    return (
        <div className="home-container slider">
            {/* Overlay */}
            <div className="overlay"></div>

            {/* Main Content */}
            <div className="main-content flex flex-col justify-center items-start h-full px-8 text-white relative z-20">
                <motion.div
                    className="glow-text space-y-4"
                    initial={{ opacity: 0, x: -50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 1.2, ease: "easeOut" }}
                >
                    <h1 className="text-4xl md:text-6xl font-bold">
                        Explore Our Collection
                    </h1>
                    <p className="text-lg md:text-2xl">
                        Discover amazing deals and the latest trends in fashion, beauty, and more.
                    </p>
                    <motion.button
                        onClick={() => navigate("/products")}
                        className="bg-blue-600 hover:bg-blue-700 text-white py-3 px-8 rounded-lg text-lg shadow-md transition-all duration-300"
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        Shop Now
                    </motion.button>
                </motion.div>
            </div>
        </div>
    );
}

export default Hero;
