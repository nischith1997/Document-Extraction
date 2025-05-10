import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Create OpenAI client using your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def smart_extract_with_llm(text: str) -> dict:
    prompt = f"""
You are an intelligent invoice parser. Extract the following fields from the OCR text below and return as JSON:

- Vendor Name
- Invoice Number
- Invoice Date
- Total Amount
- Fuel Quantity (include unit like gallons or litres)

Respond with a clean JSON. Only return the JSON.

OCR Text:
\"\"\"
{text}
\"\"\"
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You extract structured data from scanned fuel invoices."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=300
        )
        output = response.choices[0].message.content
        return eval(output) if isinstance(output, str) else output
    except Exception as e:
        return {"error": str(e)}
