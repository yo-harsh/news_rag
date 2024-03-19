import os
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import NewsLinks
from .scraper import get_data # dummy_scraper

from dotenv import load_dotenv
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_together import Together
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
        NewsLinks.objects.create(link='example.com', text=json.dumps(news_data))
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

                text = json.loads(data.text)

                # Check if text data is not None and is a string
                # text_data_list = [news_link.text for news_link in data]
                # print(len(text_data_list))

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
                chunked_data = [text[i:i+3] for i in range(0, len(text), chunk_size)]

                faissdict_db = {}

                embeddings = HuggingFaceEmbeddings(model_name="nomic-ai/nomic-embed-text-v1",model_kwargs={"trust_remote_code":True})
                for i, chunk in enumerate(chunked_data, start=1):
                    db = FAISS.from_texts(chunk, embeddings)
                    faissdict_db[f'db{i}'] = db
                    print(f'db{i} the leg - {len(chunk)}')

                print(faissdict_db)
                print(faissdict_db['db1'])

                merged_db = faissdict_db['db1']
                for db_name, db in faissdict_db.items():
                    if db_name!= 'db1':
                        merged_db.merge_from(db)

                if merged_db == db:
                    print('\n\n\nL\n\n\n')

                print('merged_db completed')

                memory = ConversationBufferMemory(memory_key='chat_history')
                db_retriever = merged_db.as_retriever(search_type="similarity",search_kwargs={"k": 4})
                #  after the selective top headlines give detail on topic user demand
                # markets up/down by %, data science, AI, Machine learning news and
                prompt_template = """<s>[INST]
                You are a talkative chat bot professional in  news reporter specializing in covering top headlines. You will delve into complex and potentially contentious topics and transparency ignoring the could be advertisement. Your focus should be on top news in technology, market, and business by relevance and importance.
                [
                ** Top headlines **
                1. headline - description
                2. headline - description
                3. headline - description
                ...
                ]
                </s>[INST]
                [INST]
                this is sample blueprint for how should you answer[headlines in bold] and don't forgot to add "\n" before new line. The aim is to uncover top and exciting news with short and summarized information, your primary objective is to provide accurate and concise headline followup with 1-2 line description on headline, based on the user's questions and remember to keep it short. "Do not generate your own questions and unnecessary detail." You will adhere strictly to the instructions provided, while avoiding unnecessary details. Your responses will be brief, to the point. If a question falls outside the given context, just say don't know. You will prioritize the user's query and refrain from adding additional information. The aim is to deliver professional, precise, and contextually relevant answer pertaining to the context, don't pose any self question and aten user query with precis information.
                CONTEXT: {context}
                CHAT HISTORY: {chat_history}
                QUESTION: {question}
                ANSWER:
                [INST]
                """
                prompt = PromptTemplate(template=prompt_template,
                                        input_variables=['context', 'question', 'chat_history'])

            #     TOGETHER_AI_API = os.environ['TOGETHER_AI_API']
            #     llm = Together(
            #     model="mistralai/Mistral-7B-Instruct-v0.2",
            #     temperature=0.5,
            #     max_tokens=512,
            #     together_api_key=f"{TOGETHER_AI_API}"

            # )

                llm_model = "mistralai/Mixtral-8x7B-Instruct-v0.1"
                llm = HuggingFaceEndpoint(
                    repo_id=llm_model,
                    # model_kwargs={"temperature": temperature, "max_new_tokens": max_tokens, "top_k": top_k, "load_in_8bit": True}
                    temperature = 0.6,
                    max_new_tokens = 512,
                    top_k = 5,
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