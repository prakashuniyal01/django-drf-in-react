import { ArrowRight } from 'lucide-react';
import React from 'react';

const HeroSection = () => {
  return (
    <React.Fragment>
      <div className="relative bg-gradient-to-br from-blue-900 to-indigo-900 overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute rotate-45 -top-20 -left-20 w-40 h-40 bg-white rounded-full" />
          <div className="absolute -bottom-20 -right-20 w-60 h-60 bg-white rounded-full" />
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-white rounded-full" />
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="py-12 sm:py-20 lg:py-24">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
              {/* Text Content */}
              <div className="text-center lg:text-left z-10">
                <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white leading-tight">
                  Transform Your Ideas Into
                  <span className="block text-blue-400">Powerful Solutions</span>
                </h1>

                <p className="mt-6 text-lg sm:text-xl text-gray-300 max-w-2xl mx-auto lg:mx-0">
                  Empower your business with cutting-edge technology solutions that drive growth and innovation. Join thousands of satisfied customers worldwide.
                </p>

                {/* CTA Buttons */}
                <div className="mt-8 sm:mt-10 flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                  <button className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 transition-colors duration-200">
                    Get Started
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </button>
                  <button className="inline-flex items-center justify-center px-6 py-3 border-2 border-white text-base font-medium rounded-lg text-white hover:bg-white hover:text-blue-900 transition-colors duration-200">
                    Learn More
                  </button>
                </div>

                {/* Social Proof */}
                <div className="mt-8 pt-8 border-t border-gray-700">
                  <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 sm:gap-8">
                    <div className="flex -space-x-2">
                      {[...Array(4)].map((_, i) => (
                        <div key={i} className="w-10 h-10 rounded-full bg-gray-300 border-2 border-blue-900" />
                      ))}
                    </div>
                    <div className="text-gray-300">
                      <span className="font-semibold">1000+</span> customers
                      <span className="block text-sm">trust our solutions</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Image/Illustration */}
              <div className="relative z-10 hidden lg:block">
                <div className="relative">
                  {/* Placeholder for hero image */}
                  <div className="w-full h-96 bg-gradient-to-tr from-blue-400 to-indigo-400 rounded-2xl shadow-2xl">
                    <img
                      src="https://i.pinimg.com/736x/04/90/95/049095647369a34c0d9c4d1ba3569e7a.jpg"
                      alt="Hero illustration"
                      className="w-full h-full object-cover rounded-2xl"
                    />
                  </div>

                  {/* Floating Elements */}
                  <div className="absolute -top-6 -right-6 w-24 h-24 bg-yellow-400 rounded-xl transform rotate-12" />
                  <div className="absolute -bottom-6 -left-6 w-32 h-32 bg-blue-400 rounded-full" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </React.Fragment>
  );
};

export default HeroSection;