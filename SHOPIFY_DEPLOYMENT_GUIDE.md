# Rozmiso Official Shopify Launch Guide (dev.shopify.com)

This step-by-step operational guide explains how to connect and deploy **Rozmiso** (`rozmiso.com`) directly on your Shopify Partner / Dev account at [https://dev.shopify.com/dashboard/234984661](https://dev.shopify.com/dashboard/234984661).

---

## 📦 What Has Been Built & Prepared For You

| Asset | Location | Purpose |
| :--- | :--- | :--- |
| **Shopify Theme Zip** | `f:\Dropshipping\rozmiso-shopify-store\rozmiso-theme.zip` | Complete Online Store 2.0 CRO theme with sticky COD bar, PIN code checker, bundle pricing & trust badges |
| **1-Click Products CSV** | `f:\Dropshipping\rozmiso-shopify-store\rozmiso_products.csv` | 5 pre-configured winning products with high-res photos, SEO descriptions & bundle variants |
| **Interactive Prototype** | `f:\Dropshipping\rozmiso-shopify-store\preview\index.html` | Live standalone browser preview of the mobile customer journey |

---

## 🚀 Step 1: Create or Open Your Store in Shopify Dev Dashboard

1. Navigate to your Shopify Partner Dashboard: [https://dev.shopify.com/dashboard/234984661](https://dev.shopify.com/dashboard/234984661).
2. Click **Stores** on the left menu $\rightarrow$ Click **Add store** $\rightarrow$ **Create development store**.
3. Choose **Create a store for a client** (or **Create a store to test and build**).
4. Enter store details:
   - **Store name**: `Rozmiso Lifestyle` (or `rozmiso-india`)
   - **Store URL**: `rozmiso-india.myshopify.com`
   - **Country/Region**: India (sets INR ₹ currency by default).
5. Click **Create development store**.

---

## 🎨 Step 2: Upload the Rozmiso Theme Zip

1. Inside your Shopify Store Admin, go to **Online Store** $\rightarrow$ **Themes**.
2. Scroll to the **Theme library** section and click **Add theme** $\rightarrow$ **Upload zip file**.
3. Click **Add file** and select:
   ```
   f:\Dropshipping\rozmiso-shopify-store\rozmiso-theme.zip
   ```
4. Click **Upload file**. Shopify will process the theme in ~10 seconds.
5. Once uploaded, click **Actions** $\rightarrow$ **Publish** (to make it the active live theme).

---

## 🛒 Step 3: Import the 5 Winning Products in 1 Click

1. In Shopify Admin, click **Products** on the left navigation bar.
2. In the top right corner, click **Import**.
3. Click **Add file** and select:
   ```
   f:\Dropshipping\rozmiso-shopify-store\rozmiso_products.csv
   ```
4. Check the box *"Overwrite any current products that have the same handle"* (optional).
5. Click **Upload and continue** $\rightarrow$ Click **Import products**.
6. All 5 winning products with high-margin bundle tiers (1 unit, 2 units, 3 units) will instantly populate!

---

## 💳 Step 4: Configure Cash On Delivery (COD) & UPI Prepaid Discounts

### 1. Enable Native Cash on Delivery
1. Go to **Settings** (bottom left) $\rightarrow$ **Payments**.
2. Scroll down to **Manual payment methods** $\rightarrow$ Click **Add manual payment method** $\rightarrow$ Choose **Cash on Delivery (COD)**.
3. In **Additional details**, write:
   > *"Pay cash or UPI to the delivery executive when the parcel arrives at your doorstep."*
4. Click **Activate Cash on Delivery**.

### 2. Enable Prepaid Payment Gateway (Razorpay / Cashfree / PhonePe)
1. In **Settings** $\rightarrow$ **Payments**, click **Choose a provider**.
2. Search and select **Razorpay** or **Cashfree Payments**.
3. Enter your API Key and Secret to enable UPI, Google Pay, PhonePe, and Cards.
4. *(Optional Indian CRO App)*: Install **GoKwik** or **Shopflo** from the Shopify App Store for an ultra-fast 1-click checkout with automated OTP address autofill and RTO fraud blocking.

### 3. Create the ₹50 Prepaid UPI Discount Code
1. In Shopify Admin, go to **Discounts** $\rightarrow$ Click **Create discount**.
2. Select **Amount off products** (or **Amount off order**).
3. Code: `PREPAID50`.
4. Value: Fixed amount $\rightarrow$ `₹50`.
5. Minimum purchase requirements: No minimum requirement.
6. Click **Save discount**.

---

## 🌐 Step 5: Connect `rozmiso.com` Domain

1. Go to **Settings** $\rightarrow$ **Domains**.
2. Click **Connect existing domain**.
3. Enter `rozmiso.com` and click **Next**.
4. In your GoDaddy DNS Manager, set:
   - **A Record**: Host `@` $\rightarrow$ Points to `23.227.38.65`
   - **CNAME Record**: Host `www` $\rightarrow$ Points to `shops.myshopify.com`
5. Click **Verify connection** in Shopify. SSL will automatically provision in 15–30 minutes.

---

## 📱 Step 6: Test Customer Checkout Experience

1. Open your live store URL on your smartphone.
2. Select the **2-in-1 Cordless Car Vacuum** product page.
3. Verify:
   - Live delivery date calculated upon typing your 6-digit PIN code.
   - Bundle selector switches between 1-Unit and 2-Unit packs with automatic discount.
   - Sticky **Order Cash on Delivery** button follows smooth scrolling.
   - WhatsApp floating icon opens customer support chat directly.
