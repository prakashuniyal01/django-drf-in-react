import  { useState } from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="p-4 text-white bg-blue-600">
      <div className="container flex items-center justify-between mx-auto">
        {/* Logo */}
        <h1 className="text-xl font-bold">Article Management</h1>

        {/* Toggle Button */}
        <button
          className="block text-white md:hidden focus:outline-none"
          onClick={toggleMenu}
        >
          {isOpen ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth="2"
              stroke="currentColor"
              className="w-6 h-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth="2"
              stroke="currentColor"
              className="w-6 h-6"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          )}
        </button>

        {/* Navigation Links */}
        <ul
          className={`${
            isOpen ? "block" : "hidden"
          } md:flex md:space-x-4 absolute md:relative top-16 md:top-0 left-0 md:left-auto w-full md:w-auto bg-blue-600 md:bg-transparent`}
        >
          <li className="p-2 text-center md:p-0 md:text-left">
            <Link to="/" className="hover:text-yellow-300">
              Home
            </Link>
          </li>
          <li className="p-2 text-center md:p-0 md:text-left">
            <Link to="/login" className="hover:text-yellow-300">
              Login
            </Link>
          </li>
          <li className="p-2 text-center md:p-0 md:text-left">
            <Link to="/signup" className="hover:text-yellow-300">
              Signup
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
