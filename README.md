#  The Digital Chimera

**The Digital Chimera** is a full-stack, asynchronous collaborative drawing game. Artists contribute one segment—a Head, a Torso, or Legs—without seeing the rest of the character, leading to hilariously bizarre final results.

###  Key Features
* **Asynchronous Multiplayer:** A global relay race of creativity.
* **The Sliver:** A 20px connection guide ensures seamless character alignment.
* **Automated Stitching:** Python (Pillow) engine merges PNGs into a final 500x1500px image.
* **Concurrency Control:** Redis-backed locking prevents duplicate turns.

###  Tech Stack
* **Frontend:** Next.js 14, TypeScript, Tailwind CSS, Fabric.js.
* **Backend:** FastAPI, Python, Pillow, PostgreSQL, Redis.
* **Cloud:** AWS S3 (Storage) and Docker (Orchestration).

###  Quick Start
1. `docker-compose up -d` (Spin up DB & Redis).
2. `cd backend && uvicorn app.main:app --reload` (Start API).
3. `cd frontend && npm run dev` (Start UI).

---
**Build for scale. Designed for weirdness.**
