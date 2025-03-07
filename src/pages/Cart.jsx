import React, { useState } from "react";
import PageContainer from "../components/General/PageContainer";

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);

  const handleAddItem = () => {
    const newItem = {
      id: Date.now(),
      name: "Sample Product",
      quantity: 1,
      size: "M",
      price: 20,
    };
    setCartItems([...cartItems, newItem]);
  };

  const handleUpdateItem = (id, key, value) => {
    const updatedItems = cartItems.map((item) =>
      item.id === id ? { ...item, [key]: value } : item
    );
    setCartItems(updatedItems);
  };

  const handleDeleteItem = (id) => {
    setCartItems(cartItems.filter((item) => item.id !== id));
  };

  return (
    <PageContainer showNav={true} showFooter={true} >
        <div className="min-h-screen bg-gradient-to-br from-gray-200 via-gray-400 to-gray-600 p-6">
        <div className="max-w-4xl mx-auto bg-white shadow-lg rounded-xl p-6">
            <h1 className="text-2xl font-bold text-gray-800 mb-4 text-center">
            Shopping Cart
            </h1>
            {cartItems.length === 0 ? (
            <div className="text-center p-10">
                <p className="text-lg text-gray-700">Your cart is empty.</p>
                <button
                onClick={handleAddItem}
                className="mt-4 bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition"
                >
                Add an Item
                </button>
            </div>
            ) : (
            <div className="space-y-6">
                {cartItems.map((item) => (
                <div
                    key={item.id}
                    className="flex flex-col lg:flex-row items-center justify-between bg-gray-100 p-4 rounded-lg shadow-sm"
                >
                    <div className="flex items-center space-x-4">
                    <img
                        src="https://via.placeholder.com/80"
                        alt={item.name}
                        className="w-20 h-20 object-cover rounded-md"
                    />
                    <div>
                        <h2 className="font-semibold text-gray-800">{item.name}</h2>
                        <p className="text-sm text-gray-600">Size: {item.size}</p>
                        <p className="text-sm text-gray-600">
                        Price: ${item.price.toFixed(2)}
                        </p>
                    </div>
                    </div>
                    <div className="flex items-center space-x-4">
                    {/* Quantity Update */}
                    <div className="flex items-center">
                        <button
                        onClick={() =>
                            handleUpdateItem(
                            item.id,
                            "quantity",
                            Math.max(1, item.quantity - 1)
                            )
                        }
                        className="bg-red-500 text-white px-3 py-1 rounded-l-lg hover:bg-red-600"
                        >
                        -
                        </button>
                        <input
                        type="number"
                        value={item.quantity}
                        onChange={(e) =>
                            handleUpdateItem(item.id, "quantity", e.target.value)
                        }
                        className="w-12 text-center border-t border-b border-gray-300"
                        />
                        <button
                        onClick={() =>
                            handleUpdateItem(item.id, "quantity", item.quantity + 1)
                        }
                        className="bg-green-500 text-white px-3 py-1 rounded-r-lg hover:bg-green-600"
                        >
                        +
                        </button>
                    </div>
                    {/* Size Update */}
                    <select
                        value={item.size}
                        onChange={(e) =>
                        handleUpdateItem(item.id, "size", e.target.value)
                        }
                        className="border border-gray-300 rounded-lg px-4 py-1"
                    >
                        <option value="S">S</option>
                        <option value="M">M</option>
                        <option value="L">L</option>
                        <option value="XL">XL</option>
                    </select>
                    {/* Delete Button */}
                    <button
                        onClick={() => handleDeleteItem(item.id)}
                        className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
                    >
                        Delete
                    </button>
                    </div>
                </div>
                ))}
                {/* Add More Items */}
                <button
                onClick={handleAddItem}
                className="block w-full bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition"
                >
                Add More Items
                </button>
            </div>
            )}
        </div>
        </div>
    </PageContainer>
  );
};

export default Cart;
