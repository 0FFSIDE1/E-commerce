import React, { useState } from 'react';
import PageContainer from './PageContainer';

function Productpage () {
  const sectionChoices = [
    'New Arrivals', 'Black Friday', 'Flashsales', 
    'Special Offers', 'Sponsored products', 'Deals of the day'
  ];

  const categoryChoices = [
    'Appliances', 'Outdoor & Sports', 'Electrical and Electronics', 
    'Kitchen Appliances', 'Books & Education', 'Interior Decorations', 
    'Lightings & Chandeliers', 'Exterior Decorations', 'Phone Accessories', 
    'Phones & Tablets', 'Foodstuffs', 'Health & Beauty', 'Home & Office', 
    'Gaming', 'Computing', 'Kids and Toys', 'Fitness and Exercise', 
    'Gadget and Accessories', 'Baby Care', 'Men Fashion', 'Men Accessories', 
    'Men Skincare', 'Women Fashion', 'Women Accessories', 'Women Skincare', 
    'Kids Skincare', 'Kids Fashion', 'Kids Accessories'
  ];

  const [formData, setFormData] = useState({
    name: '',
    description: '',
    price: '',
    previousPrice: '',
    productType: '',
    brand: '',
    inStock: true,
    quantity: '',
    section: 'New Arrivals',
    category: '',
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form Data Submitted:', formData);
    // Add your form submission logic here
  };

  return (
    <PageContainer showNav={true} showFooter={true}>
        <div className="p-6 bg-gray-50 min-h-screen flex items-center justify-center">
        <form onSubmit={handleSubmit} className="bg-white shadow-lg rounded-lg p-8 w-full max-w-2xl">
            <h1 className="text-2xl font-semibold text-gray-800 mb-4">Add a New Product</h1>

            <div className="mb-4">
            <label className="block text-gray-600 font-medium mb-1">Product Name</label>
            <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="w-full border rounded px-4 py-2 text-gray-700"
                placeholder="Enter product name"
                required
            />
            </div>

            <div className="mb-4">
            <label className="block text-gray-600 font-medium mb-1">Description</label>
            <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                className="w-full border rounded px-4 py-2 text-gray-700"
                placeholder="Enter product description"
            ></textarea>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
                <label className="block text-gray-600 font-medium mb-1">Price</label>
                <input
                type="text"
                name="price"
                value={formData.price}
                onChange={handleChange}
                className="w-full border rounded px-4 py-2 text-gray-700"
                placeholder="Enter price"
                required
                />
            </div>
            <div>
                <label className="block text-gray-600 font-medium mb-1">Previous Price</label>
                <input
                type="text"
                name="previousPrice"
                value={formData.previousPrice}
                onChange={handleChange}
                className="w-full border rounded px-4 py-2 text-gray-700"
                placeholder="Enter previous price (optional)"
                />
            </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
                <label className="block text-gray-600 font-medium mb-1">Section</label>
                <select
                name="section"
                value={formData.section}
                onChange={handleChange}
                className="w-full border rounded px-4 py-2 text-gray-700"
                >
                {sectionChoices.map((section) => (
                    <option key={section} value={section}>{section}</option>
                ))}
                </select>
            </div>
            <div>
                <label className="block text-gray-600 font-medium mb-1">Category</label>
                <select
                name="category"
                value={formData.category}
                onChange={handleChange}
                className="w-full border rounded px-4 py-2 text-gray-700"
                required
                >
                <option value="">Select a category</option>
                {categoryChoices.map((category) => (
                    <option key={category} value={category}>{category}</option>
                ))}
                </select>
            </div>
            </div>

            <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
                <label className="block text-gray-600 font-medium mb-1">Brand</label>
                <input
                type="text"
                name="brand"
                value={formData.brand}
                onChange={handleChange}
                className="w-full border rounded px-4 py-2 text-gray-700"
                placeholder="Enter brand name"
                />
            </div>
            <div>
                <label className="block text-gray-600 font-medium mb-1">Quantity</label>
                <input
                type="number"
                name="quantity"
                value={formData.quantity}
                onChange={handleChange}
                className="w-full border rounded px-4 py-2 text-gray-700"
                placeholder="Enter quantity in stock"
                required
                />
            </div>
            </div>

            <div className="flex items-center mb-6">
            <input
                type="checkbox"
                name="inStock"
                checked={formData.inStock}
                onChange={handleChange}
                className="mr-2"
            />
            <label className="text-gray-600 font-medium">In Stock</label>
            </div>

            <button
            type="submit"
            className="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded transition"
            >
            Add Product
            </button>
        </form>
        </div>
    </PageContainer>
  );
};

export default Productpage;
