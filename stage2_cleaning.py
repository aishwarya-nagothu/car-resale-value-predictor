import pandas as pd

df = pd.read_csv("spinny_suv_full.csv")

# 🔽 Create required columns
cols = [
    "Brand", "Model", "Price",
    "Make Year", "Registration Year",
    "Fuel Type", "Km Driven", "Transmission",
    "No. of Owner", "Insurance Validity", "Insurance Type",
    "Core System Rating", "Supporting System Rating",
    "Interiors & AC Rating", "Exteriors Rating", "Wear & Tear Parts Rating"
]

for col in cols:
    df[col] = ""

# 🔽 Extract Brand & Model from Name
def split_name(name):
    if pd.isna(name):
        return "", ""
    parts = name.split()
    return parts[0], " ".join(parts[1:])

# 🔽 Parse Overview (label -> next line value)
def parse_overview(text):
    data = {}
    if pd.isna(text):
        return data

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for i in range(len(lines)-1):
        key = lines[i]
        value = lines[i+1]

        data[key] = value

    return data

# 🔽 Parse Quality (label -> next line value)
def parse_quality(text):
    data = {}
    if pd.isna(text):
        return data

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    for i in range(len(lines)-1):
        key = lines[i]
        value = lines[i+1]

        data[key] = value

    return data


# 🔽 PROCESS EACH ROW
for i in range(len(df)):

    # Brand + Model
    brand, model = split_name(df.loc[i, "Name"])
    df.loc[i, "Brand"] = brand
    df.loc[i, "Model"] = model

    # Price
    df.loc[i, "Price"] = df.loc[i, "Price"]

    # Overview parsing
    ov = parse_overview(df.loc[i, "Overview"])

    df.loc[i, "Make Year"] = ov.get("Make Year", "")
    df.loc[i, "Registration Year"] = ov.get("Registration Year", "")
    df.loc[i, "Fuel Type"] = ov.get("Fuel Type", "")
    df.loc[i, "Km Driven"] = ov.get("KM Driven", "")
    df.loc[i, "Transmission"] = ov.get("Transmission", "")
    df.loc[i, "No. of Owner"] = ov.get("Ownership", "")
    df.loc[i, "Insurance Validity"] = ov.get("Insurance Validity", "")
    df.loc[i, "Insurance Type"] = ov.get("Insurance Type", "")

    # Quality parsing
    qt = parse_quality(df.loc[i, "Quality Report"])

    df.loc[i, "Core System Rating"] = qt.get("Core Systems", "")
    df.loc[i, "Supporting System Rating"] = qt.get("Supporting Systems", "")
    df.loc[i, "Interiors & AC Rating"] = qt.get("Interiors & AC", "")
    df.loc[i, "Exteriors Rating"] = qt.get("Exterior", "")
    df.loc[i, "Wear & Tear Parts Rating"] = qt.get("Wear & Tear Parts", "")


# 🔽 Save clean file
df_final = df[cols]
df_final.to_csv("spinny_cleaned.csv", index=False)

print("✅ DONE: Clean structured file ready")