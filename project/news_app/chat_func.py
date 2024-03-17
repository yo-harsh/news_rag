# from dotenv import load_dotenv

# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.llms import HuggingFaceEndpoint
# from langchain.prompts import PromptTemplate
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationalRetrievalChain
# from langchain.text_splitter import CharacterTextSplitter





# def get_chat(msg:str):

#     load_dotenv()

#     data = get_latest_news()
#     text_data = data.text
#     text_splitter = CharacterTextSplitter(
#     separator="\n",
#     chunk_size=1100,
#     chunk_overlap=200,
#     length_function=len
#     )
#     print('yo')
#     chunks = text_splitter.split_text(text_data)

#     memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
#     embeddings = HuggingFaceEmbeddings(model_name="nomic-ai/nomic-embed-text-v1",model_kwargs={"trust_remote_code":True})
#     db = FAISS.from_texts(texts=chunks, embedding=embeddings)
#     db_retriever = db.as_retriever(search_type="similarity",search_kwargs={"k": 4})


#     prompt_template = """<s>[INST]This is a chat template and As a professional professor chat bot specializing in solving queries and making the question paper for students , your primary objective is to provide accurate and concise answer based on the user's questions. Do not generate your own questions and unnecessary detail. You will adhere strictly to the instructions provided, offering relevant context from the knowledge base while avoiding unnecessary details. Your responses will be brief, to the point, and in compliance with the established format. If a question falls outside the given context, you will refrain from utilizing the chat history and instead rely on your own knowledge base to generate an appropriate response. You will prioritize the user's query and refrain from adding additional information. The aim is to deliver professional, precise, and contextually relevant question answer pertaining to the context given for making test for student, don't pose any self question and only aten user query with precis information.
#     CONTEXT: {context}
#     CHAT HISTORY: {chat_history}
#     QUESTION: {question}
#     ANSWER:
#     </s>[INST]
#     """
#     prompt = PromptTemplate(template=prompt_template,
#                             input_variables=['context', 'question', 'chat_history'])

#     # TOGETHER_AI_API= os.environ['TOGETHER_API_KEY']
#     # llm = Together(
#     #     model="mistralai/Mistral-7B-Instruct-v0.2",
#     #     temperature=0.5,
#     #     max_tokens=1024,
#     #     together_api_key=f"{TOGETHER_AI_API}"

#     # )

#     llm_model = "mistralai/Mixtral-8x7B-Instruct-v0.1"#"mistralai/Mixtral-8x7B-Instruct-v0.1"
#     llm = HuggingFaceEndpoint(
#         repo_id=llm_model,
#         # model_kwargs={"temperature": temperature, "max_new_tokens": max_tokens, "top_k": top_k, "load_in_8bit": True}
#         temperature = 0.6,
#         max_new_tokens = 1024,
#         top_k = 3,
#         load_in_8bit = True,
#     )

#     question = """hello"""

#     qa = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         memory=memory,
#         retriever=db_retriever,
#         combine_docs_chain_kwargs={'prompt': prompt}

#     )


#     result = qa.run(input=question)
#     print(result)

# ans="***\n\n\n"
# result["answer"]:

