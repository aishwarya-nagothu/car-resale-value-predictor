import pandas as pd
from openai import OpenAI
import time

# ✅ Initialize Groq client
client = OpenAI()

# ✅ Load dataset
df = pd.read_csv("spinny_suv_cleaned.csv")

# ✅ Add new columns (if not exist)
for col in ["Depriciation_Category", "Value_Score", "Country Of Origin"]:
    if col not in df.columns:
        df[col] = ""

# ✅ Step 1: Unique brands only
unique_brands = df["Brand"].dropna().unique()
print(f"Total unique brands: {len(unique_brands)}")

brand_data = {}

# ✅ Step 2: Call Groq once per brand
for brand in unique_brands:
    prompt = f"""
    You are an automotive expert.

    For the brand: {brand}

    Give:
    1. Depriciation_Category(1-10)
    2. Value_Score(1-10)
    3. Country Of Origin

    STRICT FORMAT:
    Depriciation_Category: X
    Value_Score: X
    Country Of Origin: X
    """

    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}],
            temperature=0  # more consistent output
        )

        text = response.choices[0].message.content.strip()

        depriciation_category, value_score, country_of_origin = "", "", ""

        for line in text.split("\n"):
            line = line.strip()
            if line.lower().startswith("popularity"):
                pop = line.split(":")[1].strip()
            elif line.lower().startswith("country"):
                country = line.split(":")[1].strip()
            elif line.lower().startswith("segment"):
                segment = line.split(":")[1].strip()

        # ✅ fallback if parsing fails
        if pop == "" or country == "" or segment == "":
            print(f"⚠️ Format issue for {brand}, retrying once...")

            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            text = response.choices[0].message.content.strip()

            for line in text.split("\n"):
                if "Popularity" in line:
                    pop = line.split(":")[1].strip()
                elif "Country" in line:
                    country = line.split(":")[1].strip()
                elif "Segment" in line:
                    segment = line.split(":")[1].strip()

        brand_data[brand] = {
            "depriciation_category": depriciation_category,
            "value_score": value_score,
            "country_of_origin": country_of_origin
        }

        print(f"✅ Done brand: {brand}")

        time.sleep(1)  # avoid rate limit

    except Exception as e:
        print(f"❌ Error for {brand}: {e}")

# ✅ Step 3: Map back to full dataset
for i in range(len(df)):
    brand = df.loc[i, "Brand"]

    if brand in brand_data:
        df.loc[i, "Depriciation_Category"] = brand_data[brand]["depriciation_category"]
        df.loc[i, "Value_Score"] = brand_data[brand]["value_score"]
        df.loc[i, "Country Of Origin"] = brand_data[brand]["country_of_origin"]

print("✅ Mapping complete")

# ✅ Save final dataset
df.to_csv("enhanced_dataset.csv", index=False)

print("🎉 DONE: Enhanced dataset ready")