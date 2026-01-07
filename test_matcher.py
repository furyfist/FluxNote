from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model (downloads ~80MB first time)
print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample data
topics = [
    "Introduction to Machine Learning",
    "Linear Regression",
    "Neural Networks"
]

lectures = [
    "Lecture 1: Welcome to ML",
    "Lecture 2: Regression Models Explained",
    "Lecture 3: Deep Learning Basics",
    "Lecture 4: Statistics Review",
    "Lecture 5: Advanced Neural Nets"
]

# Generate embeddings
print("Generating embeddings...")
topic_embeddings = model.encode(topics)
lecture_embeddings = model.encode(lectures)

# Match each topic to lectures
print("\nMathching topics to lectures...\n")
for i, topic in enumerate(topics):
    similarities = cosine_similarity(
        [topic_embeddings[i]],
        lecture_embeddings
    )[0]
    top_indices = similarities.argsort()[-2:][::-1]
    print(f"Topic: {topic}")
    for idx in top_indices:
        print(f" -> {lectures[idx]} (Score: {similarities[idx]:2f})")

    print()
