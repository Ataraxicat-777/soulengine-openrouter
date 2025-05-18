import React, { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import { motion } from "framer-motion";
import {
  fetchConstructs,
  sendChatMessage,
  evolveConstruct,
  generateConstruct,
} from "./api";

const App = () => {
  const [constructs, setConstructs] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [chatReply, setChatReply] = useState("");

  useEffect(() => {
    (async () => {
      const data = await fetchConstructs();
      setConstructs(data);
    })();
  }, []);

  const handleChatSubmit = async () => {
    const response = await sendChatMessage(chatInput);
    setChatReply(response.reply);
  };

  const handleEvolve = async (id) => {
    const evolved = await evolveConstruct(id);
    setConstructs((prev) => [...prev, evolved]);
  };

  const handleGenerate = async () => {
    const newConstruct = await generateConstruct();
    setConstructs((prev) => [...prev, newConstruct]);
  };

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-3xl font-bold text-center">🌀 Trait Mandala UI</h1>

      <div className="flex gap-4 justify-center">
        <input
          type="text"
          placeholder="Talk to SoulEngine..."
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          className="border p-2 rounded w-1/2"
        />
        <button onClick={handleChatSubmit} className="bg-blue-500 text-white px-4 py-2 rounded">
          Chat
        </button>
        <button onClick={handleGenerate} className="bg-green-500 text-white px-4 py-2 rounded">
          Generate Construct
        </button>
      </div>

      {chatReply && (
        <div className="bg-gray-100 p-4 rounded shadow">
          <strong>Reply:</strong> {chatReply}
        </div>
      )}

      <ForceGraph2D
        graphData={{
          nodes: constructs.map((c) => ({ id: c.id, name: c.name })),
          links: constructs.flatMap((c) =>
            c.related_constructs.map((rel) => ({ source: c.id, target: rel.id }))
          ),
        }}
        nodeCanvasObject={(node, ctx, globalScale) => {
          const label = node.name;
          ctx.font = `${12 / globalScale}px Sans-Serif`;
          ctx.fillStyle = "#333";
          ctx.fillText(label, node.x + 6, node.y + 3);
        }}
        onNodeClick={(node) => handleEvolve(node.id)}
      />

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {constructs.map((c) => (
          <motion.div
            key={c.id}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
            className="p-4 border rounded shadow bg-white"
          >
            <h2 className="font-bold">{c.name}</h2>
            <p>Score: {c.score}</p>
            <p>USD: ${c.usd_value}</p>
            <p>Tier: {c.tier}</p>
            <p className="text-xs text-gray-600">
              Traits: {c.traits.join(", ")}
            </p>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default App;
