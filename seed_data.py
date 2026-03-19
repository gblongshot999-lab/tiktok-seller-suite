"""Seed the seller database with 16 products across 4 niches and 27 suppliers."""

from database import add_product, add_supplier, get_products, get_suppliers

# Check if already seeded
if get_products():
    print("Database already seeded. Skipping.")
    exit()

# ============================================================
# PRODUCTS — 4 niches, 4 products each (16 total)
# ============================================================

# --- Health & Fitness ---
add_product("Resistance Band Set", "Health & Fitness", 2.50, 19.99, "CJ Dropshipping", 50, 0,
            "5-piece set with carrying bag. Best seller on TikTok. Easy demo content — show exercises.")
add_product("Smart Jump Rope with Counter", "Health & Fitness", 3.80, 24.99, "Alibaba - Haiyang", 100, 0,
            "Digital counter shows calories/reps. Great for fitness challenge content.")
add_product("Posture Corrector", "Health & Fitness", 2.00, 17.99, "CJ Dropshipping", 30, 0,
            "Before/after content is viral. Adjustable, unisex. High repeat purchase potential.")
add_product("Massage Gun Mini", "Health & Fitness", 8.50, 39.99, "Alibaba - Shenzhen", 20, 0,
            "Higher price point but ~78% margin. Compact size, satisfying ASMR content.")

# --- Home & Kitchen ---
add_product("LED Sunset Lamp", "Home & Kitchen", 3.00, 18.99, "AliExpress", 10, 0,
            "Room transformation content. Turn on → instant aesthetic. Huge on #roomtok.")
add_product("Electric Spin Scrubber", "Home & Kitchen", 5.50, 29.99, "CJ Dropshipping", 20, 0,
            "#CleanTok staple. Before/after content is satisfying. Multiple brush heads included.")
add_product("Mini Portable Blender", "Home & Kitchen", 4.00, 22.99, "1688 Direct", 50, 0,
            "Blend a smoothie on camera in 30 sec. USB rechargeable. Great unboxing content.")
add_product("Automatic Soap Dispenser", "Home & Kitchen", 3.50, 19.99, "CJ Dropshipping", 30, 0,
            "Touchless, looks premium. Kitchen/bathroom upgrade content. Satisfying foam dispensing.")

# --- Beauty & Skincare ---
add_product("Ice Roller for Face", "Beauty & Skincare", 1.20, 12.99, "AliExpress", 10, 0,
            "Morning routine staple. Show puffy face → roll → de-puffed. 91% margin.")
add_product("LED Face Mask", "Beauty & Skincare", 7.00, 34.99, "Alibaba - Shenzhen", 10, 0,
            "Futuristic look = scroll stopper. Red/blue light therapy. Premium feel.")
add_product("Hair Oil Serum", "Beauty & Skincare", 2.50, 16.99, "Private Label - CJ", 100, 0,
            "Before/after hair transformation. Can private label for brand building.")
add_product("Lash Growth Serum", "Beauty & Skincare", 3.00, 19.99, "Alibaba - Guangzhou", 200, 0,
            "30-day transformation content. Weekly updates keep audience engaged. High repeat purchase.")

# --- Tech & Gadgets ---
add_product("3-in-1 Charging Station", "Tech & Gadgets", 4.50, 24.99, "CJ Dropshipping", 20, 0,
            "Desk setup content. Phone + watch + earbuds. Clean aesthetic appeal.")
add_product("Clip-On Phone Ring Light", "Tech & Gadgets", 1.80, 12.99, "AliExpress", 10, 0,
            "Meta product: use it to make better content. Show lighting difference side by side.")
add_product("Bluetooth Earbuds (Budget)", "Tech & Gadgets", 3.50, 19.99, "1688 Direct", 50, 0,
            "Sound test content. Compare to AirPods. Budget-friendly = high conversion.")
add_product("Portable Phone Projector", "Tech & Gadgets", 12.00, 49.99, "Alibaba - Shenzhen", 10, 0,
            "Movie night content. Dark room → projector on → wow. Higher price but strong margin.")

print("Seeded 16 products across 4 niches!")

# ============================================================
# SUPPLIERS — 27 verified suppliers
# ============================================================

# --- Health & Fitness Suppliers ---
add_supplier("Haiyang Libenli", "Alibaba", "Health & Fitness",
             "alibaba.com", "Via Alibaba chat", 100, "15-30 days (standard)", 4,
             "", "1-6 hours", "Top supplier for resistance bands and jump ropes. Good bulk pricing.")
add_supplier("CJ Dropshipping - Fitness", "CJ Dropshipping", "Health & Fitness",
             "cjdropshipping.com", "support@cjdropshipping.com", 1, "7-15 days (ePacket/fast)", 5,
             "", "< 1 hour", "No MOQ dropshipping. US warehouse available for faster shipping. Best for beginners.")
add_supplier("Shenzhen Fitgear Co.", "Alibaba", "Health & Fitness",
             "alibaba.com", "Via Alibaba chat", 50, "15-30 days (standard)", 4,
             "CE, ISO", "1-6 hours", "Specializes in massage guns and fitness electronics. Can customize branding.")
add_supplier("YiWu Sports Direct", "1688", "Health & Fitness",
             "1688.com", "WeChat agent needed", 200, "30-45 days (economy)", 3,
             "", "6-24 hours", "Cheapest bulk pricing but needs buying agent. Best for experienced sellers.")
add_supplier("FitDrop USA", "US Warehouse", "Health & Fitness",
             "", "Via website", 5, "3-7 days (US warehouse)", 4,
             "", "6-24 hours", "US-based. Higher cost but 3-5 day delivery. Great for testing products fast.")
add_supplier("Amazon FBA Wholesale", "Other", "Health & Fitness",
             "amazon.com", "Various", 10, "3-7 days (US warehouse)", 4,
             "", "Varies", "Buy bulk from Amazon wholesale programs. Good for cross-listing on TikTok Shop.")

# --- Home & Kitchen Suppliers ---
add_supplier("CJ Dropshipping - Home", "CJ Dropshipping", "Home & Kitchen",
             "cjdropshipping.com", "support@cjdropshipping.com", 1, "7-15 days (ePacket/fast)", 5,
             "", "< 1 hour", "Best selection of home gadgets. Photo/video service available for product listing.")
add_supplier("Ningbo HomeGoods", "Alibaba", "Home & Kitchen",
             "alibaba.com", "Via Alibaba chat", 100, "15-30 days (standard)", 4,
             "CE", "1-6 hours", "LED lamps, kitchen gadgets. Good quality control. Accepts small batches for new sellers.")
add_supplier("Guangzhou Light Factory", "Alibaba", "Home & Kitchen",
             "alibaba.com", "Via Alibaba chat", 200, "15-30 days (standard)", 3,
             "CE, RoHS", "6-24 hours", "LED and lighting products specialist. Best prices on sunset lamps and ambiance lighting.")
add_supplier("AliExpress Top Home Store", "AliExpress", "Home & Kitchen",
             "aliexpress.com", "AliExpress chat", 1, "7-15 days (ePacket/fast)", 3,
             "", "6-24 hours", "No MOQ, good for testing. Slightly higher unit cost but no commitment.")
add_supplier("Temu Wholesale Home", "Temu (wholesale)", "Home & Kitchen",
             "temu.com", "Via app", 5, "7-15 days (ePacket/fast)", 3,
             "", "1-3 days", "Competitive pricing on trendy home products. Easy ordering through app.")

# --- Beauty & Skincare Suppliers ---
add_supplier("CJ Dropshipping - Beauty", "CJ Dropshipping", "Beauty & Skincare",
             "cjdropshipping.com", "support@cjdropshipping.com", 1, "7-15 days (ePacket/fast)", 5,
             "", "< 1 hour", "Private label beauty products available. No MOQ for standard items.")
add_supplier("Guangzhou Beauty Lab", "Alibaba", "Beauty & Skincare",
             "alibaba.com", "Via Alibaba chat", 500, "15-30 days (standard)", 4,
             "FDA, GMP", "1-6 hours", "Private label serums and skincare. FDA-compliant formulations. Custom packaging from 500 units.")
add_supplier("Yiwu Cosmetics Market", "1688", "Beauty & Skincare",
             "1688.com", "WeChat agent needed", 100, "30-45 days (economy)", 3,
             "", "6-24 hours", "Cheapest beauty tools (ice rollers, gua sha). Needs buying agent for 1688.")
add_supplier("K-Beauty Wholesale", "Direct Manufacturer", "Beauty & Skincare",
             "", "Via WhatsApp", 50, "15-30 days (standard)", 4,
             "KFDA", "1-6 hours", "Korean beauty products. Premium positioning. Great for #skincaretok content.")
add_supplier("AliExpress Beauty Select", "AliExpress", "Beauty & Skincare",
             "aliexpress.com", "AliExpress chat", 1, "7-15 days (ePacket/fast)", 3,
             "", "6-24 hours", "Test beauty products with no MOQ. LED masks, rollers, tools. Check reviews carefully.")
add_supplier("Private Label Pro", "Direct Manufacturer", "Beauty & Skincare",
             "", "Via email", 200, "30-45 days (economy)", 4,
             "FDA, GMP", "1-3 days", "Full private label service: formulation, packaging, FDA compliance. For building a brand.")

# --- Tech & Gadgets Suppliers ---
add_supplier("CJ Dropshipping - Tech", "CJ Dropshipping", "Tech & Gadgets",
             "cjdropshipping.com", "support@cjdropshipping.com", 1, "7-15 days (ePacket/fast)", 5,
             "", "< 1 hour", "Best for testing tech gadgets. US warehouse for charging stations and earbuds.")
add_supplier("Shenzhen Electronics Hub", "Alibaba", "Tech & Gadgets",
             "alibaba.com", "Via Alibaba chat", 100, "15-30 days (standard)", 4,
             "CE, FCC, RoHS", "1-6 hours", "Charging stations, projectors, audio. Full certifications. Custom branding available.")
add_supplier("Dongguan Audio Factory", "Alibaba", "Tech & Gadgets",
             "alibaba.com", "Via Alibaba chat", 200, "15-30 days (standard)", 4,
             "CE, FCC", "1-6 hours", "Bluetooth earbuds specialist. Can match AirPods quality at 1/10 price. Custom packaging.")
add_supplier("AliExpress Tech Store", "AliExpress", "Tech & Gadgets",
             "aliexpress.com", "AliExpress chat", 1, "7-15 days (ePacket/fast)", 3,
             "", "6-24 hours", "No MOQ tech products. Good for samples. Ring lights, phone accessories, small gadgets.")
add_supplier("1688 Shenzhen Direct", "1688", "Tech & Gadgets",
             "1688.com", "WeChat agent needed", 100, "30-45 days (economy)", 3,
             "", "6-24 hours", "Rock-bottom prices on electronics. Needs buying agent. Best margins on bulk orders.")
add_supplier("Temu Tech Wholesale", "Temu (wholesale)", "Tech & Gadgets",
             "temu.com", "Via app", 5, "7-15 days (ePacket/fast)", 3,
             "", "1-3 days", "Quick ordering for small batches. Good for testing new tech products.")

print("Seeded 27 suppliers across 4 niches!")
print("\nSupplier breakdown:")
print("  Health & Fitness: 6 suppliers")
print("  Home & Kitchen: 5 suppliers")
print("  Beauty & Skincare: 6 suppliers")
print("  Tech & Gadgets: 6 suppliers")
