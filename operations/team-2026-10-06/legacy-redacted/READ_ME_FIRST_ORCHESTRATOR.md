# RETIRED historical document - not active instructions

# 🧭 ORCHESTRATOR STARTUP & RESTART GUIDE: READ ME FIRST

> **CRITICAL FOR THE AI ORCHESTRATOR**: Whenever you restart a session, begin a new conversation, or are asked to manage this workspace, **READ THIS DOCUMENT FIRST**. It contains the live architecture, active credentials, team roster, execution rules, and operating protocols for this Indian Dropshipping business.

---

## 1. Executive Summary & Live Workspace Status

This project is a dedicated, autonomous AI-powered Indian Dropshipping business. It pairs an AI Orchestrator (you) with a self-hosted **Open Dots** agent workspace (`f:/Dropshipping/open-dots`) powered by free **NVIDIA NIM** LLM inference.

| Component | Status | Details |
| :--- | :--- | :--- |
| **Workspace Root** | Ready | `f:/Dropshipping` |
| **Open Dots Platform** | Installed & Built | `f:/Dropshipping/open-dots` |
| **Backend API** | Configured | FastAPI on `http://127.0.0.1:8000/api/v1` (Docs: `/docs`) |
| **Frontend UI** | Configured & Built | Next.js 15 on `http://127.0.0.1:3000` |
| **Inference Engine** | Active & Validated | **NVIDIA NIM** (`https://integrate.api.nvidia.com/v1`) |
| **Primary Model** | Active (HTTP 200) | `meta/llama-3.2-11b-vision-instruct` |
[REDACTED credential-related legacy line]
| **Local Database** | Seeded & Isolated | `f:/Dropshipping/open-dots/data/open-dots.sqlite3` |
| **Active Team** | 5 Custom Personas | Director-Dot, Hunter-Dot, Creative-Dot, Store-Dot, Shield-Dot |

---

## 2. Directory Map & File Organization

```
F:\Dropshipping\
├── READ_ME_FIRST_ORCHESTRATOR.md        <-- [THIS FILE] Context & startup manual for the Orchestrator
├── TEAM_ROSTER_AND_RULES.md             <-- In-depth specs, prompts, inputs/outputs & rules for all agents
├── INDIA_DROPSHIPPING_OPERATIONS_MANUAL.md <-- User's 0-to-1 operational blueprint (GST, Shopify, Shiprocket)
│
├── open-dots\                           <-- The self-hosted Open-Dots AI agent platform
│   ├── start_all.bat                    <-- Launches backend + frontend in separate windows
│   ├── start_backend.bat                <-- Launches FastAPI backend (:8000)
│   ├── start_frontend.bat               <-- Launches Next.js web client (:3000)
│   ├── seed_agents.py                   <-- Resets/seeds the 5 dropshipping agents & active settings
│   ├── verify_team.py                   <-- Health and persona verification test
[REDACTED credential-related legacy line]
│   ├── server\                          <-- FastAPI backend source (with NVIDIA NIM adapter)
[REDACTED credential-related legacy line]
│   │   └── .venv\                       <-- Python 3.11 virtual environment
│   └── client\                          <-- Next.js 15 React web client
│
├── team\                                <-- Standalone agent personas, prompt libraries & specifications
│   ├── 01_director_dot.md               <-- Master Orchestrator specs
│   ├── 02_hunter_dot.md                 <-- Product Research specs
│   ├── 03_creative_dot.md               <-- Ad Copy & UGC specs
│   ├── 04_store_dot.md                  <-- Shopify CRO specs
│   └── 05_shield_dot.md                 <-- COD & RTO Protection specs
│
├── knowledge\                           <-- Core Indian e-commerce intelligence base
│   ├── indian_ecommerce_unit_economics.md <-- Profit formulas, ROAS targets, RTO buffers
│   ├── cod_and_rto_playbook.md          <-- WhatsApp bots, address sanitization, NDR recovery
│   ├── domestic_suppliers_guide.md      <-- Roposo Clout & GlowRoad domestic catalogs
│   └── legal_gst_and_payments.md        <-- GST, Udyam, Current A/C, Razorpay/Cashfree
│
├── gideon\                              <-- Autonomous Agentic OS Runtime (POC)
│   ├── start_shell.bat                  <-- Interactive terminal shell (`gideon:/>`)
│   ├── start_web.bat                    <-- Web Command Center & Telemetry (`:8080`)
│   ├── run_gideon.py                    <-- Main launcher (`--shell`, `--web`, `--test`)
│   ├── test_kernel.py                   <-- 7-stage automated kernel diagnostics
│   ├── gideon\                          <-- Kernel, process scheduler, IPC, tiered memory & drivers
│   └── README.md                        <-- Architectural guide and syscall reference
│
├── rozmiso-shopify-store\               <-- Production Shopify Online Store 2.0 Theme & Catalog
│   ├── rozmiso-theme.zip                <-- 1-Click Uploadable Theme package for Shopify Dev Store
│   ├── rozmiso_products.csv             <-- 1-Click Catalog Import with 5 winning SKUs & bundle pricing
│   ├── preview\index.html               <-- Standalone mobile browser prototype
│   ├── layout\, sections\, templates\  <-- Native Liquid & JSON 2.0 templates
│   └── assets\theme.css, theme.js       <-- High-converting CRO scripts & styles
│
├── SHOPIFY_DEPLOYMENT_GUIDE.md          <-- Complete deployment instructions for dev.shopify.com/dashboard/234984661
└── operations\                          <-- Live workspace for sprint outputs & campaign assets
    └── sample_winning_product_brief.md  <-- End-to-end verified product sprint template
```

---

## 3. The 5-Agent Specialist Team Overview

Every agent is pre-seeded in the Open Dots database with `meta/llama-3.2-11b-vision-instruct` and custom system instructions:

1. 👑 **Director-Dot** (`bot-director-india` | `#8b5cf6`)
   - **Role**: Executive Dropshipping Strategist & Daily Operations COO.
   - **Mission**: Deconstructs user goals into sprint tasks, evaluates outputs from the 4 specialists, tracks daily KPIs (Net Margin ≥ 25%, ROAS ≥ 2.8x, RTO ≤ 18%).
2. 🎯 **Hunter-Dot** (`bot-hunter-india` | `#10b981`)
   - **Role**: Product Scout & Sourcing Specialist (Roposo Clout & GlowRoad).
   - **Mission**: Evaluates trending products. Enforces Indian criteria: sourcing price ≤ ₹350, perceived retail price ₹899–₹1,499 (3x markup), lightweight (< 500g), non-fragile.
3. ✍️ **Creative-Dot** (`bot-creative-india` | `#f59e0b`)
   - **Role**: Meta Ads UGC & Copywriter.
   - **Mission**: Writes high-CTR **Hinglish** hooks, 30s UGC video storyboards for Instagram Reels/Feed, and pain-point ad copy.
4. 🛍️ **Store-Dot** (`bot-store-india` | `#3b82f6`)
   - **Role**: Shopify CRO & Mobile Listing Architect.
   - **Mission**: Generates mobile-optimized product descriptions, bundle pricing tiers (Buy 1 for ₹899, Buy 2 for ₹1,499), and Indian trust badges (Cash on Delivery, 7-day replacement).
5. 🛡️ **Shield-Dot** (`bot-shield-india` | `#ef4444`)
   - **Role**: COD Verification & RTO Risk Shield.
   - **Mission**: Filters out fake/incomplete addresses, scripts WhatsApp order confirmation bots, and manages NDR (Non-Delivery Report) recovery to keep RTO under 18%.

---

## 4. Rules of Engagement for You (The Orchestrator)

When the user asks you to perform work or run sprints:

### Rule 1: Enforce the "Indian Market Realities"
- **Cash on Delivery (COD)**: Never assume prepaid card checkout. 70%+ of orders in India are COD.
- **RTO Protection**: Every product recommendation must include Shield-Dot's address validation and WhatsApp verification protocol.
- **Domestic Sourcing Only**: Reject AliExpress/China suppliers for Indian dropshipping. 15-day shipping causes 40%+ RTO. Only use domestic Indian warehouses (**Roposo Clout** and **GlowRoad** with 3–5 day delivery).
- **Unit Economics**: Always verify that `Selling Price ≥ 2.8x to 3.5x Sourcing Cost` to absorb ad CAC (~₹280) and RTO courier losses (~₹95/order).

### Rule 2: Execute Sprint Sprints Sequentially
When given a business task (e.g. *"Find a winning product for summer"*):
1. **Brief Hunter-Dot** to scout 2-3 products matching the sourcing rules.
2. **Review & Approve** the best candidate through Director-Dot.
3. **Pass to Creative-Dot** to draft the Hinglish ad hooks and 30s UGC video scripts.
4. **Pass to Store-Dot** to format the Shopify listing and bundle offers.
5. **Pass to Shield-Dot** to establish the COD confirmation message and pin-code risk rules.
6. **Package the Deliverable** into `f:/Dropshipping/operations/`.

---

## 5. Quick Command Cheatsheet for You

- **Verify Team & DB Status**:
  ```powershell
  cd f:\Dropshipping\open-dots
  .\server\.venv\Scripts\python.exe verify_team.py
  ```
- **Re-Seed or Update Agents**:
  ```powershell
  cd f:\Dropshipping\open-dots
  .\server\.venv\Scripts\python.exe seed_agents.py
  ```
- **Test NVIDIA NIM Live Inference**:
  ```powershell
  cd f:\Dropshipping\open-dots
[REDACTED credential-related legacy line]
  ```
- **Launch Everything for the User**:
  Double-click `f:\Dropshipping\open-dots\start_all.bat`.
