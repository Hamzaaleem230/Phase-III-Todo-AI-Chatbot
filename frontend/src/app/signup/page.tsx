"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { setToken } from "@/lib/auth";
import { API_BASE_URL } from "@/lib/api";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/signup`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setError(data?.detail?.message || data?.message || "Signup failed");
        return;
      }

      setToken(data.access_token, data.user_id);
      router.push("/login");
    } catch {
      setError("Network error or server unreachable");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black flex items-center justify-center px-4 sm:px-6 lg:px-8 text-white">

      {/* Card */}
      <div className="
        w-full
        max-w-sm
        sm:max-w-md
        md:max-w-lg
        bg-white/5
        backdrop-blur-xl
        border border-white/10
        rounded-2xl
        p-6
        sm:p-8
        md:p-10
        shadow-2xl
      ">
        
        {/* Header */}
        <div className="text-center mb-6 sm:mb-8">
          <div className="
            bg-blue-600
            w-12 h-12
            sm:w-14 sm:h-14
            md:w-16 md:h-16
            mx-auto
            rounded-xl
            flex
            items-center
            justify-center
            mb-4
            text-lg sm:text-xl
          ">
            ✨
          </div>

          <h1 className="text-xl sm:text-2xl md:text-3xl font-bold">
            Create Account
          </h1>

          <p className="text-gray-400 text-xs sm:text-sm mt-1">
            Start managing your tasks smarter
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4 sm:space-y-5">
          
          {/* Email */}
          <div>
            <label className="text-xs sm:text-sm text-gray-300 mb-1 block">
              Email
            </label>

            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="you@example.com"
              className="
                w-full
                px-3 sm:px-4
                py-2.5 sm:py-3
                text-sm sm:text-base
                rounded-lg
                bg-black/40
                border border-white/10
                focus:border-blue-500
                focus:ring-2
                focus:ring-blue-500/30
                outline-none
              "
            />
          </div>

          {/* Password */}
          <div>
            <label className="text-xs sm:text-sm text-gray-300 mb-1 block">
              Password
            </label>

            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="••••••••"
                className="
                  w-full
                  px-3 sm:px-4
                  py-2.5 sm:py-3
                  pr-12
                  text-sm sm:text-base
                  rounded-lg
                  bg-black/40
                  border border-white/10
                  focus:border-blue-500
                  focus:ring-2
                  focus:ring-blue-500/30
                  outline-none
                "
              />

              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="
                  absolute
                  right-3
                  top-1/2
                  -translate-y-1/2
                  text-gray-400
                  hover:text-white
                  text-sm sm:text-base
                "
              >
                {showPassword ? "🙈" : "👁️"}
              </button>
            </div>
          </div>

          {error && (
            <p className="text-xs sm:text-sm text-red-400 text-center">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="
              w-full
              bg-blue-600
              hover:bg-blue-700
              py-2.5 sm:py-3
              text-sm sm:text-base
              rounded-lg
              font-semibold
              transition
              disabled:opacity-60
            "
          >
            {loading ? "Creating account..." : "Sign Up"}
          </button>
        </form>

        {/* Footer */}
        <p className="text-xs sm:text-sm text-center mt-6 text-gray-400">
          Already have an account?{" "}
          <span
            onClick={() => router.push("/login")}
            className="text-blue-500 hover:underline cursor-pointer"
          >
            Login
          </span>
        </p>

      </div>
    </main>
  );
}
