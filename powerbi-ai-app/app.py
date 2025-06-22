import streamlit as st
from openai import OpenAI
import fitz  # For PDFs
import docx  # For Word Docs
import requests
from io import BytesIO

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="AI Power BI Report Generator", page_icon="📊")
st.title("📊 AI-Powered Power BI Report Generator from BRD")

uploaded_file = st.file_uploader("📄 Upload your BRD / Requirement document", type=["pdf", "docx", "txt"])

# 📘 Extract text from uploaded document
def extract_text(file):
    if file.name.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    return ""

# 🤖 Generate multiple dashboard layouts
def generate_multiple_layouts(text):
    system_prompt = (
        "You are a Power BI expert. Based on the provided BRD (business requirement document), generate 3 unique layout plans for Reports. "
        "Each layout must include:\n"
        "- Summary of business goals\n"
        "- Exactly 5 to 6 visuals using ONLY: KPI card, Table, Pie Chart, Line Chart, Area Chart, Cluster Bar Chart, Area Line Chart, or any advanced chart relevant to the requirement.\n"
        "- A prompt for DALL·E that must generate a FULL Power BI Reports screen/image with only the specified visuals.\n"
        "- All visual titles should be shown in 'Times New Roman' font in the image and use fresh and profesional colours combination \n"
        "- The Reports must be clean, well-aligned, and modern.\n"
        "⚠️ Do NOT include human body parts for ex : hands , maps, or waterfall visuals unless absolutely required and do not include any other that images than visuals\n"
        "Use this format for each layout:\n"
        "1. Objective:\n2. Visuals Used:\n3. Justification:\n4. Prompt:\n\n"
        "Separate each layout using '---'."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Requirement document:\n{text}"}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content.strip().split('---')
    except Exception as e:
        return [f"Error: {e}"]

# 🎨 Generate Power BI dashboard image
def generate_dashboard_image(prompt):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response.data[0].url
    except Exception as e:
        return f"Image generation failed: {e}"

# 🧠 Extract prompt for DALL·E
def extract_prompt_from_response(response_text):
    lower = response_text.lower()
    if "prompt:" in lower:
        parts = response_text.split("prompt:")
        return parts[-1].strip()
    return response_text.strip()

# 🚀 Main Application Flow
if uploaded_file:
    with st.spinner("🔍 Extracting text from document..."):
        doc_text = extract_text(uploaded_file)
        st.success("✅ Text extracted from uploaded document!")

    with st.spinner("🤖 Generating 3 dashboard layout combinations..."):
        dashboard_layouts = generate_multiple_layouts(doc_text)

    for idx, layout in enumerate(dashboard_layouts, start=1):
        st.markdown(f"## 📊 Dashboard Layout Option {idx}")
        st.markdown(layout)

        image_prompt = extract_prompt_from_response(layout)

        with st.spinner(f"🖼️ Generating Power BI Screen/image for Layout {idx}..."):
            image_url = generate_dashboard_image(
                image_prompt + 
                " | Full-screen Power BI report layout, visuals titled in Times New Roman font. Reports must be clean, professional, with clear alignment."
            )

        if image_url.startswith("http"):
            st.image(image_url, caption=f"🖼️ Layout {idx} - Power BI Reports Mockup", use_column_width=True)

            try:
                img_data = requests.get(image_url).content
                st.download_button(
                    label=f"📥 Download Layout {idx} Screenshot",
                    data=img_data,
                    file_name=f"powerbi_layout_{idx}.png",
                    mime="image/png"
                                    )
            except Exception as e:
                st.error(f"Download error: {e}")
        else:
            st.error(image_url)
