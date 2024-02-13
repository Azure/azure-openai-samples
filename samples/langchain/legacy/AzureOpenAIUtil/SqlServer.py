import urllib, os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAIChat
from langchain.agents import AgentExecutor

class SqlServer:
    def __init__(self, Server, Database, Username, Password, port=1433, odbc_ver=18, topK=10) -> None:
        
        odbc_conn = 'Driver={ODBC Driver '+ str(odbc_ver) + ' for SQL Server};Server=tcp:' + \
            Server + f',{port};Database={Database};Uid={Username};Pwd={Password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        params = urllib.parse.quote_plus(odbc_conn)
        self.conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)

        db = SQLDatabase.from_uri(self.conn_str)
        self.toolkit = SQLDatabaseToolkit(db=db)

        self.SQL_PREFIX = """You are an agent designed to interact with a Microsoft Azure SQL database.
        Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results using SELECT TOP in SQL Server syntax.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.
        You have access to tools for interacting with the database.
        Only use the below tools. Only use the information returned by the below tools to construct your final answer.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

        If the question does not seem related to the database, just return "I don't know" as the answer.
        """

        deploy_name = os.getenv('CHAT_COMPLETION_NAME')
        # print(deploy_name)
        self.agent_executor = create_sql_agent(
                llm=OpenAIChat(temperature=0,  engine=deploy_name),
                toolkit=self.toolkit,
                verbose=True,
                prefix=self.SQL_PREFIX, 
                topK = topK
            )
        
    def run(self, text: str):
        return self.agent_executor.run(text)
        