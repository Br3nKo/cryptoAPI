import React from "react";

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: "create" | "update" | "delete";
}

const Button: React.FC<ButtonProps> = ({ label, onClick, variant = "primary" }) => {
  const getVariantStyles = () => {
    switch (variant) {
      case "update":
        return "bg-gray-700 hover:bg-gray-600 text-gray-300";
      case "delete":
        return "bg-gray-800 hover:bg-gray-700 text-gray-300";
      default:
        return "bg-gray-600 hover:bg-gray-500 text-gray-300";
    }
  };

  return (
    <button
      className={`px-4 py-2 rounded-lg font-medium transition ${getVariantStyles()}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
};

export default Button;