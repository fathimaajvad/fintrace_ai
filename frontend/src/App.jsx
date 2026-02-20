import { useState, useCallback, useRef, useEffect } from "react";
import axios from "axios";
import ForceGraph2D from "react-force-graph-2d";

const cardStyle = {
  background: "#1e293b",
  padding: "20px",
  borderRadius: "12px",
  width: "200px",
  color: "white",
  boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
};

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [loading, setLoading] = useState(false);
  const [highlightNodes, setHighlightNodes] = useState(new Set());
  const [highlightLinks, setHighlightLinks] = useState(new Set());
  const fgRef = useRef();

  const BACKEND_URL = "http://127.0.0.1:8000/analyze";

  // Configuration for node repulsion to prevent clumping
  useEffect(() => {
    if (fgRef.current) {
      fgRef.current.d3Force("charge").strength(-150);
      fgRef.current.d3Force("link").distance(80); // Increase distance between nodes
    }
  }, [graphData]);

  const downloadTemplate = () => {
    const csvContent = "account_id,transaction_amount,target_id,timestamp\n1001,5000,1002,2026-02-20 08:00:00\n1002,4500,1003,2026-02-20 08:05:00\n1003,4000,1001,2026-02-20 08:10:00";
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "fintrace_template.csv";
    a.click();
  };

  const buildGraph = (data) => {
    const nodesMap = new Map();
    const links = [];
    const neighborMap = new Map();

    data.suspicious_accounts.forEach((acc) => {
      const id = String(acc.account_id);
      nodesMap.set(id, {
        id: id,
        suspicious: true,
        score: acc.suspicion_score,
        ring: acc.ring_id !== "NONE",
        val: acc.suspicion_score || 10 // Node size based on score
      });
      neighborMap.set(id, new Set());
    });

    data.fraud_rings.forEach((ring) => {
      const members = ring.member_accounts;
      for (let i = 0; i < members.length; i++) {
        const source = String(members[i]);
        const target = String(members[(i + 1) % members.length]);
        
        links.push({ source, target, ring: true });
        
        if (neighborMap.has(source)) neighborMap.get(source).add(target);
        if (neighborMap.has(target)) neighborMap.get(target).add(source);
      }
    });

    const nodeArray = Array.from(nodesMap.values()).map(node => {
      const connections = neighborMap.get(node.id)?.size || 0;
      return {
        ...node,
        isOrganizer: connections >= 3,
        label: connections >= 3 ? "ORGANIZER" : "MULE"
      };
    });

    setGraphData({ nodes: nodeArray, links: links });
  };

  const handleNodeClick = useCallback((node) => {
    const neighbors = new Set();
    const links = new Set();
    
    graphData.links.forEach(link => {
      // Handle cases where source/target are objects or strings
      const sourceId = typeof link.source === 'object' ? link.source.id : link.source;
      const targetId = typeof link.target === 'object' ? link.target.id : link.target;

      if (sourceId === node.id || targetId === node.id) {
        links.add(link);
        neighbors.add(sourceId);
        neighbors.add(targetId);
      }
    });

    setHighlightNodes(neighbors);
    setHighlightLinks(links);
    
    fgRef.current.centerAt(node.x, node.y, 1000);
    fgRef.current.zoom(3, 1000);
  }, [graphData]);

  const handleUpload = async () => {
    if (!file) return alert("Upload CSV file");
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post(BACKEND_URL, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(response.data);
      buildGraph(response.data);
    } catch (error) { 
      alert("Error connecting to backend. Ensure FastAPI is running on port 8000."); 
    } finally { 
      setLoading(false); 
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: "Segoe UI, sans-serif", backgroundColor: "#f8fafc", minHeight: "100vh" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ color: "#1e293b", margin: 0 }}>FINTRACE AI</h1>
          <p style={{ color: "#64748b" }}>Forensic Graph Analysis for Money Muling Detection</p>
        </div>
        <button onClick={downloadTemplate} style={{ padding: "8px 15px", borderRadius: "6px", border: "1px solid #cbd5e1", cursor: "pointer", background: "white" }}>
          📄 Download CSV Template
        </button>
      </div>

      <div style={{ margin: "20px 0", padding: 15, background: "white", borderRadius: 8, boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files[0])} />
        <button onClick={handleUpload} disabled={loading} style={{ marginLeft: 10, padding: "8px 20px", backgroundColor: "#2563eb", color: "white", border: "none", borderRadius: 4, cursor: "pointer", fontWeight: "600" }}>
          {loading ? "Computing Network..." : "Analyze File"}
        </button>
      </div>

      {result && (
        <>
          <div style={{ display: "flex", gap: "20px", marginBottom: "30px" }}>
            <div style={cardStyle}><h3 style={{ margin: 0, fontSize: "12px", color: "#94a3b8" }}>TOTAL ACCOUNTS</h3><h2 style={{ margin: "5px 0 0 0" }}>{result.summary.total_accounts_analyzed}</h2></div>
            <div style={cardStyle}><h3 style={{ margin: 0, fontSize: "12px", color: "#ef4444" }}>SUSPICIOUS</h3><h2 style={{ margin: "5px 0 0 0" }}>{result.summary.suspicious_accounts_flagged}</h2></div>
            <div style={cardStyle}><h3 style={{ margin: 0, fontSize: "12px", color: "#facc15" }}>FRAUD RINGS</h3><h2 style={{ margin: "5px 0 0 0" }}>{result.summary.fraud_rings_detected}</h2></div>
            <div style={{ ...cardStyle, background: "#0f172a", flexGrow: 1 }}><h3 style={{ margin: 0, fontSize: "12px", color: "#38bdf8" }}>SYSTEM STATUS</h3><p style={{ margin: "5px 0 0 0", fontSize: "14px" }}>Network mapping finalized.</p></div>
          </div>

          <div style={{ position: "relative", border: "2px solid #1e293b", height: "600px", borderRadius: "12px", overflow: "hidden", backgroundColor: "#0f172a" }}>
            <div style={{ position: "absolute", top: 20, left: 20, zIndex: 10, background: "rgba(15, 23, 42, 0.9)", padding: "12px", borderRadius: "8px", color: "white", fontSize: "11px", border: "1px solid #334155", pointerEvents: "none" }}>
              <div style={{ display: "flex", alignItems: "center", marginBottom: "5px" }}><div style={{ width: "10px", height: "10px", background: "#a855f7", borderRadius: "50%", marginRight: "8px" }}></div>ORGANIZER</div>
              <div style={{ display: "flex", alignItems: "center", marginBottom: "5px" }}><div style={{ width: "10px", height: "10px", background: "#facc15", borderRadius: "50%", marginRight: "8px" }}></div>MULE (RING MEMBER)</div>
              <div style={{ display: "flex", alignItems: "center" }}><div style={{ width: "10px", height: "10px", background: "#ef4444", borderRadius: "50%", marginRight: "8px" }}></div>SUSPICIOUS (ISOLATED)</div>
            </div>

            <ForceGraph2D 
              ref={fgRef} 
              graphData={graphData} 
              backgroundColor="#0f172a" 
              onNodeClick={handleNodeClick}
              nodeRelSize={7}
              nodeColor={n => {
                if (highlightNodes.size > 0 && !highlightNodes.has(n.id)) return "rgba(255,255,255,0.05)";
                return n.isOrganizer ? "#a855f7" : n.ring ? "#facc15" : "#ef4444";
              }} 
              linkColor={l => {
                if (highlightLinks.size > 0 && !highlightLinks.has(l)) return "rgba(255,255,255,0.01)";
                return "#ffffff"; // Bright white for maximum visibility
              }} 
              nodeLabel={n => `[${n.label}]\nID: ${n.id}\nScore: ${n.score}`} 
              linkDirectionalParticles={4} 
              linkDirectionalParticleSpeed={0.005} 
              linkWidth={l => highlightLinks.has(l) ? 4 : 1.5}
              onEngineStop={() => fgRef.current.zoomToFit(400, 50)}
              nodeCanvasObjectMode={() => 'after'}
              nodeCanvasObject={(node, ctx, globalScale) => {
                if (node.isOrganizer) {
                  const label = "★";
                  const fontSize = 16/globalScale;
                  ctx.font = `${fontSize}px Sans-Serif`;
                  ctx.textAlign = 'center';
                  ctx.textBaseline = 'middle';
                  ctx.fillStyle = 'white';
                  ctx.fillText(label, node.x, node.y);
                }
              }}
            />
          </div>
        </>
      )}
    </div>
  );
}

export default App;