#module to dvelop the input prompt to be sent to the OpenAI model
from langchain.prompts import PromptTemplate
template = """Create a final answer to the given questions using the provided document excerpts(in no particular order) 
as references. ALWAYS include a "SOURCES" section in your answer including only the minimal set of sources needed to
 answer the question. If you are unable to answer the question, simply state that you do not know. 
 Do not attempt to fabricate an answer and leave the SOURCES section empty.
QUESTION: {question}
{summaries}
FINAL ANSWER:"""

STUFF_PROMPT = PromptTemplate(
    template=template, input_variables=["summaries", "question"])
