import Link from "next/link";
// import { redirect } from "next/navigation";

export default function Home() {
  // redirect("/tasks");

  return (
    <main className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white overflow-hidden">

      {/* Hero Section */}
      <section className="flex flex-col items-center text-center px-4 sm:px-6 lg:px-8 pt-12 sm:pt-16 md:pt-20">

        <div className="bg-blue-600 p-3 sm:p-4 rounded-xl mb-6 text-xl sm:text-2xl">
          ✅
        </div>

        <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-extrabold mb-4 leading-tight">
          Stay organized, <br className="hidden sm:block" /> get things done
        </h2>

        <p className="text-gray-400 text-sm sm:text-base md:text-lg max-w-md sm:max-w-xl mb-8 px-2">
          A simple and elegant task management app to help you
          focus on what matters most.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
          <Link
            href="/tasks"
            className="w-full sm:w-auto text-center bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold text-sm sm:text-base transition"
          >
            Get Started Free
          </Link>

          {/* <Link
            href="/login"
            className="w-full sm:w-auto text-center border border-white/20 px-6 py-3 rounded-lg hover:bg-white/5 text-sm sm:text-base transition"
          >
            Sign In
          </Link> */}
        </div>
      </section>

      {/* Features Section */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8 max-w-6xl mx-auto mt-20 sm:mt-24 md:mt-28 px-4 sm:px-6 lg:px-8 pb-16 sm:pb-20">
        <Feature
          title="Simple & Fast"
          desc="Create and manage tasks in seconds with an intuitive interface."
        />
        <Feature
          title="Secure"
          desc="Your tasks are private and protected."
        />
        <Feature
          title="Responsive"
          desc="Works beautifully on desktop and mobile devices."
        />
      </section>

    </main>
  );
}

function Feature({ title, desc }: { title: string; desc: string }) {
  return (
    <div className="bg-white/5 p-5 sm:p-6 rounded-xl border border-white/10 hover:border-white/20 transition backdrop-blur-sm">
      <h3 className="text-base sm:text-lg font-semibold mb-2">
        {title}
      </h3>
      <p className="text-gray-400 text-xs sm:text-sm">
        {desc}
      </p>
    </div>
  );
}
