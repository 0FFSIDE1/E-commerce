import React, { useState } from "react";
import PageContainer from "../components/General/PageContainer";

function VendorPage () {
  // Sample data for vendors, their ratings, and images
  const vendors = [
    {
      id: 1,
      name: "Vendor A",
      product: "Appliances",
      rating: 4.5,
      image: "https://via.placeholder.com/100?text=Vendor+A",
    },
    {
      id: 2,
      name: "Vendor B",
      product: "Appliances",
      rating: 3.8,
      image: "https://via.placeholder.com/100?text=Vendor+B",
    },
    {
      id: 3,
      name: "Vendor C",
      product: "Phones & Tablets",
      rating: 4.9,
      image: "https://via.placeholder.com/100?text=Vendor+C",
    },
    {
      id: 4,
      name: "Vendor D",
      product: "Books & Education",
      rating: 4.0,
      image: "https://via.placeholder.com/100?text=Vendor+D",
    },
    {
      id: 5,
      name: "Vendor E",
      product: "Books & Education",
      rating: 4.7,
      image: "https://via.placeholder.com/100?text=Vendor+E",
    },
    {
      id: 6,
      name: "Vendor F",
      product: "Phones & Tablets",
      rating: 3.5,
      image: "https://via.placeholder.com/100?text=Vendor+F",
    },
  ];

  const [selectedProduct, setSelectedProduct] = useState("");
  const [filteredVendors, setFilteredVendors] = useState([]);
  const [orderedByRating, setOrderedByRating] = useState(false);

  const productChoices = [
    "Appliances",
    "Phones & Tablets",
    "Books & Education",
    "Health & Beauty",
    "Gaming",
  ];

  const handleProductChange = (e) => {
    const product = e.target.value;
    setSelectedProduct(product);

    // Filter vendors by the selected product
    const filtered = vendors.filter((vendor) => vendor.product === product);
    setFilteredVendors(filtered);
    setOrderedByRating(false); // Reset order
  };

  const handleOrderByRating = () => {
    // Sort vendors by rating in descending order
    const sortedVendors = [...filteredVendors].sort((a, b) => b.rating - a.rating);
    setFilteredVendors(sortedVendors);
    setOrderedByRating(true);
  };

  return (
    <PageContainer showFooter={true} showNav={true}>
        <div className="p-6 bg-gray-50 min-h-screen flex items-center justify-center">
        <div className="bg-white shadow-lg rounded-xl p-8 w-full max-w-3xl">
            <h1 className="text-2xl font-bold text-gray-800 mb-6">
            VENDORS
            </h1>

            {/* Product Dropdown */}
            <div className="mb-6">
            <label className="block text-gray-600 font-medium mb-2">
                Select Product Category
            </label>
            <select
                value={selectedProduct}
                onChange={handleProductChange}
                className="w-full border rounded px-4 py-2 text-gray-700"
            >
                <option value="">-- Select a Product --</option>
                {productChoices.map((product) => (
                <option key={product} value={product}>
                    {product}
                </option>
                ))}
            </select>
            </div>

            {/* Vendors Section */}
            <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Vendors for {selectedProduct || "Selected Product"}
            </h2>

            {filteredVendors.length > 0 ? (
                <>
                <button
                    onClick={handleOrderByRating}
                    className="bg-red-700 text-white px-4 py-2 rounded mb-4 hover:bg-blue-600 transition"
                >
                    Order by Rating
                </button>
                <ul className="space-y-4">
                    {filteredVendors.map((vendor) => (
                    <li
                        key={vendor.id}
                        className="flex items-center bg-gray-100 p-4 rounded shadow space-x-4"
                    >
                        <img
                        src={vendor.image}
                        alt={`${vendor.name} Image`}
                        className="w-16 h-16 rounded-full object-cover border"
                        />
                        <div className="flex-1">
                        <span className="block text-gray-800 font-medium">
                            {vendor.name}
                        </span>
                        <span className="text-sm text-gray-500">
                            Product: {vendor.product}
                        </span>
                        </div>
                        <span className="text-red-500 font-semibold">
                        {vendor.rating} ★
                        </span>
                    </li>
                    ))}
                </ul>
                </>
            ) : (
                <p className="text-gray-500">
                {selectedProduct
                    ? "No vendors available for this product."
                    : "Select a product to view vendors."}
                </p>
            )}
            </div>
        </div>
        </div>
    </PageContainer>
  );
};

export default VendorPage;
