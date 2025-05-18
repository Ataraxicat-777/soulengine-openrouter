// frontend/src/api.ts

export async function fetchConstructs() {
  const res = await fetch("http://localhost:8000/constructs");
  if (!res.ok) throw new Error("Failed to fetch constructs.");
  return await res.json();
}

export async function sendChatMessage(message: string) {
  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error("Failed to send chat message.");
  return await res.json();
}

export async function evolveConstruct(id: string) {
  const res = await fetch("http://localhost:8000/evolve", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id }),
  });
  if (!res.ok) throw new Error("Failed to evolve construct.");
  return await res.json();
}

export async function generateConstruct() {
  const res = await fetch("http://localhost:8000/generate", {
    method: "POST",
  });
  if (!res.ok) throw new Error("Failed to generate construct.");
  return await res.json();
}
