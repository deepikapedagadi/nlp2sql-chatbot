from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.utilities import SQLDatabase
import os
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_openai import ChatOpenAI
#from langchain.agents import AgentType
from langsmith import traceable

from dotenv import load_dotenv
load_dotenv()

#flask app init
app = Flask(__name__)
CORS(app) #allows frontend to call backend

#env  var
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY =  os.getenv("LANGSMITH_API_KEY")
LANGCHAIN_PROJECT = "nlp2-sql-chatbot"
LANGCHAIN_TRACING_V2 = True
#create db obj
#db = SQLDatabase.from_uri(pg_uri) # type: ignore

#connect to PostgreSQL
pg_uri = os.getenv("POSTGRES_URI",
                   "postgresql+psycopg2://postgres:welcome@localhost:5432/testdb"
                   )

#create db obj
db = SQLDatabase.from_uri(pg_uri) # type: ignore

#load llm n sql agent
llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature = 0,
)

sql_agent = create_sql_agent(
    llm=llm,
    db=db, # type: ignore
    #agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

#chatbot logic
@traceable(name="backend_chatbot_handler")
def run_agent_query(query):
    return sql_agent.run(query)

#api route
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        question = data.get("question")
        if not question:
            return jsonify({"error": "Missing 'question' field"}), 400
        #run sql agent
        answer = run_agent_query(question)

        return jsonify({
            "question": question,
            "answer": answer
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


#root check
@app.route("/", methods=["GET"])
def home():
    return "SQL CHATBOT BACKEND RUNNING"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)