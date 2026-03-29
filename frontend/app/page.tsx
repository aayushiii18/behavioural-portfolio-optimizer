import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-900 to-indigo-900 flex items-center justify-center">
      <div className="text-center text-white p-8">
        <h1 className="text-5xl font-bold mb-4">
          Behavioural Portfolio Optimizer
        </h1>
        <p className="text-xl mb-8 text-blue-200">
          Detect your investment biases and optimize your portfolio
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/login"
            className="bg-white text-blue-900 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition"
          >
            Login
          </Link>
          <Link
            href="/register"
            className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-900 transition"
          >
            Register
          </Link>
        </div>
      </div>
    </main>
  );
}