from loaders import load_pdf, load_docx, load_website
from splitter import split_text
from embeddings import embed_chunks, get_embedding_model
from vectorstore import VectorStore
from rag import generate_answer
text = load_pdf("../documents/test.pdf")

print("----- PDF FIRST 500 CHARACTERS -----")
print(text[:500])
print("----- PDF TOTAL LENGTH -----")
print(len(text))

docx_text = load_docx("C:/Users/recha/Downloads/ai_engineer_roadmap (1).docx")

print("----- DOCX FIRST 500 CHARACTERS -----")
print(docx_text[:500])
print("----- DOCX TOTAL LENGTH -----")
print(len(docx_text))
web_text = load_website("https://en.wikipedia.org/wiki/Artificial_intelligence")

print("----- WEBSITE FIRST 500 CHARACTERS -----")
print(web_text[:500])
print("----- WEBSITE TOTAL LENGTH -----")
print(len(web_text))
chunks = split_text(text)

print("----- NUMBER OF CHUNKS -----")
print(len(chunks))
print("----- FIRST CHUNK -----")
print(chunks[0])
print("----- SECOND CHUNK -----")
print(chunks[1])
vectors = embed_chunks(chunks)

print("----- NUMBER OF VECTORS -----")
print(len(vectors))
print("----- LENGTH OF ONE VECTOR -----")
print(len(vectors[0]))
print("----- FIRST 10 NUMBERS OF FIRST VECTOR -----")
print(vectors[0][:10])
# Build the vector store from our resume chunks
store = VectorStore()
store.build(chunks, vectors)

# Ask a question
question = "What AWS experience does this person have?"
model = get_embedding_model()
question_vector = model.encode(question)

results = store.search(question_vector, top_k=3)

print("----- QUESTION -----")
print(question)
print("----- TOP MATCHING CHUNKS -----")
for i, chunk in enumerate(results):
    print(f"\nResult {i+1}:")
    print(chunk)
answer = generate_answer(question, results)

print("----- FINAL AI ANSWER -----")
print(answer)