# HerdSim 🐑

**HerdSim** is an interactive, agent-based research platform designed to simulate, visualize, and evaluate sheep herding algorithms. 

Herding behavior—where a small group of "shepherds" (like dogs or robots) controls and guides a much larger group of "sheep" to a target—is a complex problem with applications in robotics, crowd control, and collective animal behavior. HerdSim provides a standardized environment to easily compare different herding algorithms against various scenarios.

## Motivation

Researchers and developers building flocking or herding algorithms often face several core challenges:

- **Live Visualization:** Seeing how algorithms perform in real-time.
- **Standardized Benchmarking:** Running apples-to-apples comparisons of different herding models under identical, reproducible conditions.
- **Extensibility:** Easily integrating custom environments, constraints, and driving algorithms without rewriting the core engine.

HerdSim provides a plug-and-play architecture. You can select an algorithm, choose a scenario (e.g., "drive to goal", "split flock", "obstacle course"), and immediately watch the simulation unfold in a live, interactive web interface.

## Getting Started

You can run HerdSim locally on your machine. You'll need Python and Node.js installed.

1. **Install the backend dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```
2. **Install the frontend dependencies:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```
3. **Start the simulation server:**
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```
4. **Start the visual interface:** (Open a new terminal window)
   ```bash
   cd frontend
   npm run dev
   ```

Once everything is running, open your browser and go to **http://localhost:5173** to start simulating!

## Documentation

Want to dive deeper into the science or the code? 
- **Research & Theory:** Check out the in-app "Guide" tab or browse the [`docs/research/`](docs/research/) folder to learn about the specific algorithms, scenarios, and metrics included.
- **Developer Guide:** Interested in how the engine works or want to write your own algorithm plugin? Read our [Developer Documentation](docs/developer/README.md).
- **Papers:** Original research papers are available in [`docs/papers/`](docs/papers/).
