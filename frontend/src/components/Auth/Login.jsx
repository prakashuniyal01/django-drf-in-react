
const Login = () => {
  return (
    <div className="p-4">
      <h1 className="text-xl font-bold text-center">Login</h1>
      <form className="max-w-md mx-auto mt-4">
        <label className="block mb-2">
          Email:
          <input
            type="email"
            className="w-full p-2 border rounded"
            placeholder="Enter your email"
          />
        </label>
        <label className="block mb-2">
          Password:
          <input
            type="password"
            className="w-full p-2 border rounded"
            placeholder="Enter your password"
          />
        </label>
        <button className="px-4 py-2 mt-2 text-white bg-blue-500 rounded">
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
