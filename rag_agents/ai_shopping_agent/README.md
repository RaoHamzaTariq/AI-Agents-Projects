# 🛒 AI Shopping Agents

**AI Shopping Agents** is a modular, intelligent assistant system designed to enhance the e-commerce experience with natural language interfaces. Built with modern AI tooling, this system uses multiple agents and tools to provide seamless product recommendations, handle customer inquiries, and triage user requests intelligently.

---

## 🧠 Overview

The AI Shopping Agents platform comprises multiple specialized agents working together to provide a responsive and helpful shopping experience:

### 🔹 Agents

1. **🛍️ Product Recommendation Agent**
   - Recommends products based on user preferences, search queries, and purchase history.
   - Leverages product embeddings and contextual understanding for tailored suggestions.

2. **🩺 Triage Agent**
   - Determines user intent and routes requests to the appropriate agent (e.g., recommendation, FAQ, human support).
   - Ensures faster and more accurate resolution of customer needs.

3. **❓ General FAQs Agent**
   - Answers common questions about orders, shipping, returns, and account issues.
   - Uses retrieval-based methods for accurate, up-to-date responses.

---

## 🧰 Tools

- **🔍 RAG (Retrieval-Augmented Generation)**  
  Augments responses with real-time product and policy information from a knowledge base.

- **📦 Get Product Data Tool**  
  Queries live product information such as pricing, inventory, and descriptions for enhanced recommendation quality.

---

## 🏗️ Tech Stack

| Component        | Stack / Frameworks Used                       |
|------------------|-----------------------------------------------|
| Interface        | `Chainlit`                                    |
| Agents SDK       | `OpenAI Agents SDK`                           |
| Agent Orchestration | `LangChain`                              |
| Vector Search    | `ChromaDB`                                    |
| Backend Logic    | `Python`                                      |


---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-org/ai-shopping-agents.git
cd ai-shopping-agents
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the Chainlit UI

```bash
chainlit run main.py
```
## 🧪 Example Use Cases
> "Show me summer dresses under $100." → Routed to Product Recommendation Agent.

> "Where's my order?" → Routed to FAQ Agent.

> "I need help choosing between two laptops." → Recommendation Agent assisted by product data.

## 📌 Future Enhancements
- Integration with live e-commerce APIs
- Multi-modal inputs (e.g., image-based search)
- Personalized recommendations via user profiles

