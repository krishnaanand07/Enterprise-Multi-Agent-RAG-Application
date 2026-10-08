import pandas as pd
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy.future import select

from app.agents.state import AgentState
from app.database.database import AsyncSessionLocal
from app.models import Dataset, Document
from app.services.llm_service import llm_service


class DataAgent:
    """Analytical CSV Data Agent executing safe Pandas queries."""

    ANALYSIS_PROMPT = """You are an Enterprise Data Analyst.
Analyze the CSV dataset summary and sample data provided below to answer the user's analytical question accurately.

Question: {query}

CSV Summary & Sample Data:
{dataset_summary}

Provide a clear, executive response highlighting numerical stats, summaries, or key insights found:"""

    @classmethod
    async def process(cls, state: AgentState) -> AgentState:
        query = state["query"]
        user_id = state["user_id"]

        async with AsyncSessionLocal() as db:
            res = await db.execute(select(Dataset).where(Dataset.user_id == user_id).order_by(Dataset.created_at.desc()))
            datasets = res.scalars().all()

            if not datasets:
                state["response"] = "No uploaded CSV datasets found for your account. Please upload a CSV file in the Documents section."
                state["sources"] = []
                state["agent_used"] = "Data Agent"
                return state

            dataset = datasets[0]
            doc_res = await db.execute(select(Document).where(Document.id == dataset.document_id))
            doc = doc_res.scalars().first()

            if not doc or not doc.file_path or not doc.file_path.endswith(".csv"):
                state["response"] = "CSV dataset file is missing or invalid."
                state["sources"] = []
                state["agent_used"] = "Data Agent"
                return state

            try:
                df = pd.read_csv(doc.file_path)
                
                # Perform basic summary stats with Pandas
                summary = f"Columns: {list(df.columns)}\nTotal Rows: {len(df)}\n\n"
                summary += "Data Summary:\n" + df.describe(include='all').to_string() + "\n\n"
                summary += "First 20 Rows:\n" + df.head(20).to_string(index=False)
            except Exception as e:
                state["response"] = f"Failed to load CSV dataset: {str(e)}"
                state["sources"] = []
                state["agent_used"] = "Data Agent"
                return state

        try:
            llm = llm_service.get_llm(temperature=0.1)
            prompt = ChatPromptTemplate.from_template(cls.ANALYSIS_PROMPT)
            chain = prompt | llm
            res = await chain.ainvoke({
                "query": query,
                "dataset_summary": summary
            })

            state["response"] = str(res.content).strip()
            state["sources"] = [{
                "document_id": dataset.document_id,
                "document_name": doc.filename,
                "page_number": 1,
                "chunk_id": f"dataset_{dataset.id}",
                "source_type": "csv",
                "snippet": f"Analyzed CSV file '{doc.filename}' with {len(df)} rows across columns: {', '.join(df.columns)}"
            }]
            state["agent_used"] = "Data Agent"

        except Exception as e:
            state["response"] = f"Error performing data analysis: {str(e)}"
            state["sources"] = []
            state["agent_used"] = "Data Agent"

        return state
