import psycopg
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import DATABASE_URL, GEMINI_MODEL

with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM quotations")
    print("Quotations in DB:", cur.fetchone()[0])      # expect 15

llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL)
print("Gemini says:", llm.invoke("Reply with the word OK").content)