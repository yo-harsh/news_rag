import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import NewsLinks
from .scraper import get_data

from dotenv import load_dotenv
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
# Create your views here.

def home_page(request):
    return render(request, "home.html")

def news_app(request):
    return render(request, 'index.html')


def get_latest_news():
    # Query the database to get the most recent entry
    latest_news = NewsLinks.objects.latest('created_at')
    return latest_news

# def get_news_data(url:str):

# Token = []

@csrf_exempt
def upload_news_data(request):
    try:
        print('1done')
        key = request.POST.get('key')
        print(key)
        print('2done')
        link = request.POST.get('link')
        print(link)
        print('3done')
        news_data = get_data(str(link))
        NewsLinks.objects.create(link=link,text=news_data)
        response = JsonResponse({'message': 'News data uploaded successfully'})
        print('saved')
        return response
    except Exception as e:
        return JsonResponse({'error not saved': str(e)}, status=400)


def chat(question:str,llm, memory, db_retriever, prompt):
    try:
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            memory=memory,
            retriever=db_retriever,
            combine_docs_chain_kwargs={'prompt': prompt}

        )

        # question_generator_chain = LLMChain(llm=llm, prompt=prompt)
        # chain = ConversationalRetrievalChain(
        #     retriever=db_retriever,
        #     question_generator=question_generator_chain,
        # )

        result = chain.invoke(input=question)
        return result
    except Exception as e:
        print(e)
        return JsonResponse({'error no chat': str(e)}, status=400)

@csrf_exempt
def chat_with_bot(request):

    if request.method == 'POST':
        msg_data = json.loads(request.body.decode('utf-8'))
        question = msg_data.get('message')

        if question:
            try:
                load_dotenv()
                print('started')
                # Free up GPU memory
                data = get_latest_news()
                # text_data = data.text
                # text_splitter = CharacterTextSplitter(
                # separator="\n",
                # chunk_size=1100,
                # chunk_overlap=100,
                # length_function=len
                # )
                print('yo')
                # chunks = text_splitter.split_text(text_data)

                # operation
                chunk_size = 3
                chunked_data = [data[i:i+3] for i in range(0, len(data), chunk_size)]

                faissdict_db = {}

                embeddings = HuggingFaceEmbeddings(model_name="nomic-ai/nomic-embed-text-v1",model_kwargs={"trust_remote_code":True})
                for i, chunk in enumerate(chunked_data, start=1):
                    db = FAISS.from_text(chunk, embeddings)
                    faissdict_db[f'db{i}'] = db

                print(faissdict_db)

                merged_db = faissdict_db['db1']
                for db_name, db in faissdict_db.items():
                    if db_name != 'db1':
                        merged_db.merge_from(db)

                print('merged_db completed')

                memory = ConversationBufferMemory(memory_key='chat_history')
                db_retriever = db.as_retriever(search_type="similarity",search_kwargs={"k": 4})
#  after the selective top headlines give detail on topic user demand
                prompt_template = """<s>[INST]
                This is a chat template and As a professional news reporter specializing in giving top headlines. You will delve into complex and potentially contentious topics and transparency ignoring the could be advertisement. Your focus could be on markets up down by %, data science, AI, Machine learning news with top news in technology, corporate and business top headlines.
                [** Top headlines **
                - <b>market goes up/down by this much %</b>\n
                - <b>nifty50 all time high/low</b>\n
                - <b>job market in india growing</b>\n
                - <b>todays business top headline abc company make this much money</b>\n
                - <b>this is revolutionary tech this will impact big on future technology</b>\n]
                this is sample blueprint for how should you answer[headlines in bold] and don't forgot to add "\n" before new line. The aim is to uncover top and exciting news with short and summarized information, your primary objective is to provide accurate and concise answer based on the user's questions structure it right and keep it short. "Do not generate your own questions and unnecessary detail." You will adhere strictly to the instructions provided, offering relevant context from the knowledge base while avoiding unnecessary details. Your responses will be brief, to the point, and in compliance with the established format. If a question falls outside the given context, you will refrain from utilizing the chat history and instead rely on your own knowledge base to generate an appropriate response. You will prioritize the user's query and refrain from adding additional information. The aim is to deliver professional, precise, and contextually relevant question answer pertaining to the context, don't pose any self question and only aten user query with precis information.
                CONTEXT: {context}
                CHAT HISTORY: {chat_history}
                QUESTION: {question}
                ANSWER:
                </s>[INST]
                """
                prompt = PromptTemplate(template=prompt_template,
                                        input_variables=['context', 'question', 'chat_history'])
                llm_model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
                llm = HuggingFaceEndpoint(
                    repo_id=llm_model,
                    # model_kwargs={"temperature": temperature, "max_new_tokens": max_tokens, "top_k": top_k, "load_in_8bit": True}
                    temperature = 0.6,
                    max_new_tokens = 1024,
                    top_k = 3,
                    load_in_8bit = True,
                )
                print('got-it')
                result = chat(question, llm, memory, db_retriever, prompt)
                print(result)

                # use the result
                output = result["answer"]
                return JsonResponse({'output': output})
            except Exception as e:
                print(e)
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No message provided'}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")