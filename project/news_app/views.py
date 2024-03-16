import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import NewsLinks
from .scraper import get_data

from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceEndpoint
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

Token = []

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
        Token.append(key)
        print('saved')
        return response
    except Exception as e:
        return JsonResponse({'error not saved': str(e)}, status=400)

@csrf_exempt
def chat_with_bot(request):

    if request.method == 'POST':
        msg_data = json.loads(request.body.decode('utf-8'))
        question = msg_data.get('message')

        if question:
            try:
                print(Token)
                HUGGINGFACEHUB_API_TOKEN = Token[0]
                print(HUGGINGFACEHUB_API_TOKEN)
                print('done')
                import torch
                # Free up GPU memory
                data = get_latest_news()
                text_data = data.text
                text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1100,
                chunk_overlap=200,
                length_function=len
                )
                print('yo')
                chunks = text_splitter.split_text(text_data)
                embeddings = HuggingFaceEmbeddings(model_name="nomic-ai/nomic-embed-text-v1",model_kwargs={"trust_remote_code":True})
                print('go')
                db = FAISS.from_texts(texts=chunks, embedding=embeddings)
                print('fin')
                torch.cuda.empty_cache()
                memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
                db_retriever = db.as_retriever(search_type="similarity",search_kwargs={"k": 4})

                prompt_template = """<s>[INST]
                This is a chat template and As a professional news reporter specializing in giving top headlines.
                You will delve into complex and potentially contentious topics and transparency ignoring the could be advertisement.
                Your focus could be on markets up down by %, data science, AI, Machine learning news with top news in technology,
                corporate and business top headlines. The aim is to uncover top and exciting news with transparency without adding anything irrelevant,
                your primary objective is to provide accurate and concise answer based on the user's questions.
                Do not generate your own questions and unnecessary detail. You will adhere strictly to the instructions provided,
                offering relevant context from the knowledge base while avoiding unnecessary details. Your responses will be brief,
                to the point, and in compliance with the established format. If a question falls outside the given context,
                you will refrain from utilizing the chat history and instead rely on your own knowledge base to generate an appropriate response.
                You will prioritize the user's query and refrain from adding additional information. The aim is to deliver professional,
                precise, and contextually relevant question answer pertaining to the context,
                don't pose any self question and only aten user query with precis information.
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
                qa = ConversationalRetrievalChain.from_llm(
                llm=llm,
                memory=memory,
                retriever=db_retriever,
                combine_docs_chain_kwargs={'prompt': prompt}
                )
                print('done')
                result = qa.invoke(input=question)
                print(result)

                # use the result
                output = result["answer"]
                return JsonResponse({'output': output})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No message provided'}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")