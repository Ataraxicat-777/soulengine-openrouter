const BASE_URL = import.meta.env.VITE_API_URL;

export async function fetchConstructs() {
  const res = await fetch(`${BASE_URL}/constructs`);
  if (!res.ok) throw new Error("Failed to fetch constructs.");
  return await res.json();
}

export async function sendChatMessage(message: string) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  return await res.json();
}

export async function evolveConstruct(id: string) {
  const res = await fetch(`${BASE_URL}/evolve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id }),
  });
  if (!res.ok) throw new Error("Failed to evolve construct.");
  return await res.json();
}

export async function generateConstruct() {
  const res = await fetch(`${BASE_URL}/generate`, {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to generate construct.");
  return await res.json();
}
