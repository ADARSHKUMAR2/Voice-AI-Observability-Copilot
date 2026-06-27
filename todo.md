## Phase 1: Environment Setup & Infrastructure Foundations
- [ ] Initialize Git repository matching architectural guidelines (`/backend`, `/frontend`).
- [ ] Set up HighLevel Developer Marketplace account and configure a Sandbox sub-account.
- [ ] Scaffold Node.js backend (`Express`, `dotenv`, `cors`, database connectivity frameworks).
- [ ] Scaffold Vue.js frontend application (`Vue 3`, `Vite`, Tailwind CSS/UI framework matching GHL styling parameters).
- [ ] Establish environment files (`.env.example`) covering API keys, database URLs, and port bindings.

## Phase 2: Ingestion & Backend Core Pipeline (Monitor)
- [ ] Design robust `/api/webhook/ghl-call-completed` processing route.
- [ ] Connect database layer schemas (`agent_profiles`, `call_evaluations`, `use_actions`).
- [ ] Build LLM evaluation client using structured outputs (JSON formatting schemas for analytical safety).
- [ ] Write integration unit tests mapping mock transcripts onto the analysis engine.
- [ ] Implement signature validation handling on webhook requests to protect system endpoints.

## Phase 3: Analytics Dashboard & UI Construction (Analyze)
- [ ] Build core Vue routing framework scoping views by incoming `location_id`.
- [ ] Implement Executive Analytics layout tracking aggregate script adherence matrices.
- [ ] Create the **"Use Actions"** component rendering pinpointed call fragments alongside contextual failure flags.
- [ ] Construct the **Prompt Strategy Sandbox** component displaying current vs. optimized system prompts.
- [ ] Add state management routines for seamless asynchronous polling or update dispatching.

## Phase 4: Marketplace Integration & Loop Optimization (Flywheel)
- [ ] Set up interactive triggers linking prompt patches back to agent profile configurations.
- [ ] Deploy frontend system to highly-scalable environments (e.g., Vercel, Netlify, Amplify).
- [ ] Deploy backend framework to accessible web spaces (e.g., Render, Heroku, AWS).
- [ ] Register custom iframe applications or Custom Menu Links pointing directly to the live frontend bundle inside the GHL Developer portal.
- [ ] Conduct end-to-end operational dry-runs within the live HighLevel Sandbox account interface.
"""