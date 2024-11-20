export const BASE_URL = "http://localhost:8000/api";

export async function apiFetch(endpoint: string, options?: RequestInit) {
  // Prepare headers
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  // Check if token exists in local storage
  const token = localStorage.getItem("token");
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Merge provided options with our base fetch configuration
  const fetchOptions: RequestInit = {
    ...options,
    headers: {
      ...headers,
      ...options?.headers,
    },
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, fetchOptions);

  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  return response.json();
}
