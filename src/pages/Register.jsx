import React from "react";
import { motion } from "framer-motion";
import PageContainer from "../components/General/PageContainer";
import "../components/landing/Style_hero.css"

function Register() {
  const fadeInVariant = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0, transition: { duration: 2.0 } },
  };

  return (
    <PageContainer showFooter={true} showNav={true}>
        <div className="flex flex-col md:flex-row items-center justify-center min-h-screen bg-gradient-to-r  from-white/50 to-[#f6b4cf] p-6 relative overflow-hidden animate-gradient">
        {/* Floating Background Elements */}
        <div className="absolute top-10 left-10 w-40 h-40 bg-white opacity-10 rounded-full blur-2xl"></div>
        <div className="absolute bottom-10 right-10 w-60 h-60 bg-purple-500 opacity-20 rounded-full blur-3xl"></div>

        {/* Header Text: AlabaLines */}
        <motion.h1
            className="absolute top-5 text-4xl md:text-6xl font-extrabold text-black drop-shadow-lg font-[calligraphic]"
            variants={fadeInVariant}
            initial="hidden"
            animate="visible"
        >
            AlabaLine
        </motion.h1>
    

        {/* Left Section: Form */}
        <motion.div
            className="bg-[rgba(255,255,255,0.9)] shadow-[0_0_10px] rounded-xl p-8 w-full md:w-1/2 space-y-4"
            variants={fadeInVariant}
            initial="hidden"
            animate="visible"
        >
            <h1 className="text-3xl font-bold text-gray-800">Vendor Registration</h1>
            <form className="space-y-4">
            {/* Form Inputs */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                type="text"
                placeholder="Title"
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <input
                type="text"
                placeholder="Name"
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <input
                type="text"
                placeholder="Address"
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <input
                type="email"
                placeholder="Email"
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <input
                type="url"
                placeholder="Company Website"
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <input
                type="tel"
                placeholder="Phone Number"
                className="border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
            </div>
            {/* Social Media Links */}
            <input
                type="text"
                placeholder="Social Media Links"
                className="border border-gray-300 rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
            {/* Checkbox */}
            <div className="flex items-center">
                <input
                type="checkbox"
                id="terms"
                className="w-4 h-4 text-purple-500 border-gray-300 rounded focus:ring-2 focus:ring-purple-500"
                />
                <label htmlFor="terms" className="ml-2 text-gray-600">
                I agree to the terms and conditions
                </label>
            </div>
            {/* Register Button */}
            <button
                type="submit"
                className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 w-full"
            >
                Register
            </button>
            </form>
        </motion.div>

        {/* Right Section: Image */}
        <motion.div
            className="hidden md:block w-full md:w-1/2 mt-10 ml-5 rounded-xl shadow-[0_0_15px]"
            variants={fadeInVariant}
            initial="hidden"
            animate="visible"
            transition={{ delay: 0.2 }} // Delay for the image animation
        >
            <img
            src="../Goods/vendor.jpg"
            alt="Vendor Registration"
            className="rounded-lg shadow-lg"
            loading="lazy"
            />
        </motion.div>
        </div>
    </PageContainer>
  );
}

export default Register;
