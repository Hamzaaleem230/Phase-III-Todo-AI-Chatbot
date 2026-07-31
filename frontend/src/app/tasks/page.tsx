"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getToken, getUserId } from "@/lib/auth";

interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  const fetchTasks = async () => {
    try {
      const token = getToken();
      const userId = getUserId();

      if (!token || !userId) {
        router.push("/login");
        return;
      }

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/${userId}/tasks`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!res.ok) {
        throw new Error("Failed to fetch tasks");
      }

      const data = await res.json();
      setTasks(data);
    } catch (err) {
      console.error("Fetch tasks error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const toggleComplete = async (id: number) => {
    const token = getToken();
    const userId = getUserId();

    if (!token || !userId) {
      router.push("/login");
      return;
    }

    await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/${userId}/tasks/${id}/complete`,
      {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    fetchTasks();
  };

  const deleteTask = async (id: number) => {
    const token = getToken();
    const userId = getUserId();

    if (!token || !userId) {
      router.push("/login");
      return;
    }

    await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/${userId}/tasks/${id}`,
      {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    fetchTasks();
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-black">
      
      {/* Page Header */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-10 sm:pt-12 pb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        
        <h1 className="text-xl sm:text-2xl md:text-3xl font-bold text-gray-900 dark:text-white text-center sm:text-left">
          My Tasks
        </h1>

        <button
          onClick={() => {
            const token = getToken();
            if (!token) {
              router.push("/login");
            } else {
              router.push("/tasks/create");
            }
          }}
          className="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm sm:text-base cursor-pointer"
        >
          + New Task
        </button>
      </div>

      {/* Content */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        {loading ? (
          <p className="text-center text-gray-500">Loading tasks...</p>
        ) : tasks.length === 0 ? (
          <p className="text-center text-gray-500">
            No tasks yet. Create one!
          </p>
        ) : (
          <div className="grid gap-4">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="
                  bg-white dark:bg-zinc-900
                  p-4 sm:p-5
                  rounded-lg
                  shadow
                  flex
                  flex-col
                  sm:flex-row
                  sm:items-center
                  sm:justify-between
                  gap-4
                "
              >
                {/* Task Info */}
                <div className="flex-1">
                  <h2
                    className={`text-base sm:text-lg font-semibold ${
                      task.completed
                        ? "line-through text-gray-400"
                        : "text-gray-900 dark:text-white"
                    }`}
                  >
                    {task.title}
                  </h2>
                  {task.description && (
                    <p className="text-sm text-gray-500 mt-1">
                      {task.description}
                    </p>
                  )}
                </div>

                {/* Buttons */}
                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => toggleComplete(task.id)}
                    className="cursor-pointer flex-1 sm:flex-none px-3 py-1.5 text-xs sm:text-sm rounded bg-green-600 text-white hover:bg-green-700"
                  >
                    {task.completed ? "Undo" : "Done"}
                  </button>

                  <button
                    onClick={() => router.push(`/tasks/${task.id}/edit`)}
                    className="cursor-pointer flex-1 sm:flex-none px-3 py-1.5 text-xs sm:text-sm rounded bg-yellow-500 text-white hover:bg-yellow-600"
                  >
                    Edit
                  </button>

                  <button
                    onClick={() => deleteTask(task.id)}
                    className="cursor-pointer flex-1 sm:flex-none px-3 py-1.5 text-xs sm:text-sm rounded bg-red-500 text-white hover:bg-red-600"
                  >
                    Delete
                  </button>
                </div>

              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
