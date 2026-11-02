# 🇮🇳 Indian Dropshipping & Open Dots Multi-Agent Operations Manual

Welcome to your complete, autonomous Indian Dropshipping operations setup powered by **Open Dots** (`https://github.com/Anil-matcha/open-dots`).

---

## 1. Quick Launch: Open Dots Multi-Agent Workspace

Your Open Dots environment has been fully installed, configured, and seeded in `f:\Dropshipping\open-dots`.

### How to Start the System
You can launch both the backend API and frontend web client using the provided one-click launchers:
- **One-Click Full Launch**: Double-click `f:\Dropshipping\open-dots\start_all.bat`
- **Or start individually**:
  - Backend: Run `f:\Dropshipping\open-dots\start_backend.bat` (serves on `http://127.0.0.1:8000`)
  - Frontend: Run `f:\Dropshipping\open-dots\start_frontend.bat` (serves on `http://127.0.0.1:3000`)

### Access & Login Credentials
1. Open your browser and navigate to: **`http://127.0.0.1:3000`**
2. When prompted for the owner access token, enter:
   ```text
   opendots-india-dropshipping-secret
   ```
3. Once logged in, your 5 specialized Indian Dropshipping agents will be available in the sidebar.

---

## 2. NVIDIA NIM Free API Integration

Open Dots has been configured to use **NVIDIA NIM** free API endpoints (`https://integrate.api.nvidia.com/v1`).

### To Add Your Free NVIDIA API Key:
1. Visit [build.nvidia.com](https://build.nvidia.com) and click **Sign In** (free developer account).
2. Generate an API Key under any model (e.g., `meta/llama-3.3-70b-instruct`). You get **1,000 free inference credits**.
3. Open `f:\Dropshipping\open-dots\server\.env` in any text editor and paste your key:
   ```env
   MODEL_API_KEY=nvapi-your_actual_key_here
   ```
   *(Alternatively, you can paste it directly in the Open Dots Web UI under **Settings → Model Provider**).*

---

## 3. Your 5-Agent Specialist Team

| Agent | Name & Avatar | Role | Primary Focus in India |
| :--- | :--- | :--- | :--- |
| **Orchestrator** | 👑 **Director-Dot** | Master COO & Strategist | Breaks down business targets into daily sprints; evaluates cross-agent outputs; monitors ROAS, RTO, and net margins. |
| **Product Scout** | 🎯 **Hunter-Dot** | Sourcing & Trend Analyst | Identifies viral problem-solving products; checks margins on **Roposo Clout** and **GlowRoad** (sourcing < ₹350, selling ₹899-₹1,499). |
| **Ad Copywriter** | ✍️ **Creative-Dot** | Meta Ads & UGC Specialist | Writes high-energy **Hinglish** hooks, 30s UGC video storyboards for Instagram Reels, and pain-point ad copy. |
| **Store Architect**| 🛍️ **Store-Dot** | Shopify CRO & Listing Lead | Formats mobile-first Shopify pages, bundle pricing tiers (Buy 1 for ₹899, Buy 2 for ₹1,499), trust badges, and FAQ sections. |
| **Risk Guard** | 🛡️ **Shield-Dot** | COD Verification & RTO Shield | Filters incomplete addresses, scripts WhatsApp order confirmation bots, and manages NDR (Non-Delivery Report) recovery to keep RTO < 18%. |

### How to Run an Orchestration Sprint:
1. Select **Director-Dot** in the web chat.
2. Prompt:
   > *"Director-Dot, let's start a product sprint for kitchen gadgets or car utility tools under ₹350 on Roposo Clout. Please coordinate with Hunter-Dot for product vetting, Creative-Dot for Hinglish Meta scripts, and Shield-Dot for COD risk guidelines."*
3. Switch between agents as needed to refine specific assets.

---

## 4. Zero-to-One Indian Dropshipping Blueprint

### Phase 1: Legal Registration & Banking (Days 1–5)
1. **MSME / Udyam Registration** (Free):
   - Visit [udyamregistration.gov.in](https://udyamregistration.gov.in).
   - Register under your Sole Proprietorship using your personal Aadhaar and PAN card. Takes 10 minutes; certificate arrives in 24-48 hours.
2. **GST Registration** (Mandatory for Interstate E-commerce):
   - In India, Section 24 of the CGST Act mandates GST registration for anyone making supply through an e-commerce operator, regardless of turnover.
   - Apply at [gst.gov.in](https://www.gst.gov.in) under Sole Proprietorship. Use your electricity bill and rent agreement/property tax receipt for address proof.
3. **Current Bank Account**:
   - Open a digital current account with **HDFC, ICICI, or IDFC First Bank** using your GST certificate and Udyam registration. This is required to receive daily COD remittances from Shiprocket/Roposo.

---

### Phase 2: Store Setup & Domestic Suppliers (Days 6–8)
1. **Shopify Store Setup**:
   - Sign up on Shopify (₹20/month trial).
   - Use clean, fast mobile themes: **Sense** or **Dawn**.
2. **Connect Domestic Indian Suppliers**:
   - **GlowRoad (by Amazon)**: Install the GlowRoad Shopify app. Offers reliable 3-5 day delivery across Tier 1, 2, and 3 pin codes with unbranded packaging.
   - **DeoDap (Rajkot B2B Dropshipping)**: Browse 12,000+ trending wholesale SKUs with high profit margins and 24-48h dispatch SLA.
   - *Note on Roposo Clout*: Roposo Clout marketplace discontinued service on April 1, 2026. Use GlowRoad or DeoDap for all active operations.
   - *Why NOT AliExpress / China?* Shipping takes 15-25 days. In India, 70% of orders are COD; if delivery takes more than 5 days, customers reject the parcel at the doorstep, resulting in immediate 40%+ RTO disaster.
3. **Checkout Optimization**:
   - Install **GoKwik**, **Shopflo**, or **Fastrr Checkout**.
   - These apps autofill customer addresses from a network of 100M+ Indian online shoppers and score pin-codes for COD fraud risk.

---

### Phase 3: Logistics & RTO Shield (Days 9–10)
1. **Logistics Aggregator**:
   - Sign up on **Shiprocket** or **NimbusPost**.
   - Connect your Shopify store. Configure automated courier assignment (Delhivery, Blue Dart, Xpressbees) based on delivery performance score.
2. **The Golden RTO Formula**:
   - Industry average COD RTO is 30-40%. Your goal is to keep it **strictly under 18%**.
   - **WhatsApp Order Confirmation**: Send an automated message with quick reply buttons within 2 minutes of checkout. Only ship confirmed orders.
   - **Prepaid Conversion**: In the WhatsApp message, offer: *"Pay online via UPI now and get Flat ₹50 instant discount + Priority Dispatch!"* (converts 20-30% of COD orders into non-cancelable prepaid sales).
   - **NDR (Non-Delivery Report) Handling**: When a delivery fails on day 1 (e.g., "Customer not available"), trigger an immediate automated WhatsApp follow-up asking for a preferred re-delivery date.

---

### Phase 4: Meta Ads & Marketing (Days 11+)
1. **Ad Account Setup**:
   - Set up **Meta Business Manager** (business.facebook.com).
   - Connect your Facebook Page and Instagram Business handle.
   - Install the Meta Pixel on Shopify.
2. **Campaign Structure**:
   - **Campaign Type**: Sales (Conversion: Purchase).
   - **Targeting**: Broad (Age 21–50, Pan India).
   - **Exclusions**: Exclude Andaman & Nicobar, Lakshadweep, and remote hilly areas with unreliable courier networks.
   - **Creatives**: 3 UGC-style 9:16 vertical videos created using Creative-Dot's Hinglish scripts.
3. **Target Unit Economics**:
   - Sourcing Price: ₹250
   - Selling Price: ₹899 – ₹999
   - Target Cost Per Purchase (CPP): ₹250 – ₹320
   - Break-even ROAS: ~2.2x
   - Target Scaling ROAS: 3.0x+

---

## 5. Summary of Workspace Files

- Launcher: `f:\Dropshipping\open-dots\start_all.bat`
- Verification Test: `f:\Dropshipping\open-dots\verify_team.py`
- Agent Seeder: `f:\Dropshipping\open-dots\seed_agents.py`
- Server Environment: `f:\Dropshipping\open-dots\server\.env`
- Frontend Client: `f:\Dropshipping\open-dots\client\.env.local`
- Local Data Directory: `f:\Dropshipping\open-dots\data`
