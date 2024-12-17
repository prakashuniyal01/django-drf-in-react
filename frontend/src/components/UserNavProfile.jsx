import { ChevronDown, LayoutDashboard, LogOut, Settings, User } from 'lucide-react';
import { Fragment, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const UserNavProfile = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [loggedInUserInfo, setLoggedInUserInfo] = useState({
    full_name: '',
    role: '',
    email: '',
  });

  const navigator = useNavigate();

  useEffect(() => {
    const userInfo = JSON.parse(localStorage.getItem('userInfo'));
    if (!userInfo) {
      navigator('/login');
    }
    setLoggedInUserInfo(userInfo);

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="relative">
      {/* Profile Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 p-2 rounded-lg hover:bg-gray-200 bg-gray-100 transition-colors duration-200"
      >
        <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
          <span className="text-white text-sm font-medium">
            {loggedInUserInfo.full_name.split(' ').map(n => n[0]).join('')}
          </span>
        </div>
        <div className="hidden md:block text-left">
          <p className="text-sm font-medium text-gray-700">{loggedInUserInfo.full_name}</p>
          <p className="text-xs text-gray-500">{loggedInUserInfo.role}</p>
        </div>
        <ChevronDown className="h-4 w-4 text-gray-500" />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <Fragment>
          {/* Backdrop for clicking away */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setIsOpen(false)}
          />

          {/* Dropdown content */}
          <div className="absolute right-0 mt-2 w-48 py-2 bg-white rounded-lg shadow-lg border border-gray-100 z-20">
            {/* User Info Section */}
            <div className="px-4 py-2 border-b border-gray-100">
              <p className="text-sm font-medium text-gray-700">{loggedInUserInfo.full_name}</p>
              <p className="text-xs text-gray-500 truncate">{loggedInUserInfo.email}</p>
            </div>

            {/* Menu Items */}
            <button
              className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2"
              onClick={() => console.log('Profile clicked')}
            >
              <User className="h-4 w-4" />
              Profile
            </button>

            {loggedInUserInfo.role === 'admin' && (
              <button
                className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                onClick={() => navigator('/admin')}
              >
                <LayoutDashboard className="h-4 w-4" />
                Admin Dashboard
              </button>
            )}

            <button
              className="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 flex items-center gap-2"
              onClick={() => console.log('Settings clicked')}
            >
              <Settings className="h-4 w-4" />
              Settings
            </button>

            <div className="border-t border-gray-100 my-1" />

            <button
              className="w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-gray-100 flex items-center gap-2"
              onClick={() => console.log('Logout clicked')}
            >
              <LogOut className="h-4 w-4" />
              Log out
            </button>
          </div>
        </Fragment>
      )}
    </div>
  );
};

export default UserNavProfile;