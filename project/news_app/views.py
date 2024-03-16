from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home_page(request):
    return render(request, "home.html")

def news_app(request):
    return render(request, 'index.html')

@csrf_exempt
def upload_pdf(request):
    print(1)
    key1 = request.POST.get('key')
    print(key1)
    global global_vector_db, global_convo_chain
    if request.method == 'POST':

        obj = request.FILES['file']
        if obj:
            try:
                # load_dotenv()
                print(key1)
                OPENAI_API_KEY = key1
                print(OPENAI_API_KEY)
                doc = PdfFiles.objects.create(file=obj)
                doc.save()
                print('saved')
                file_list.append(doc.file.name)
                print(file_list[-1])
                print('start')

                # Update the global variables when a new PDF is uploaded
                pdf_path = os.path.join(settings.MEDIA_ROOT, file_list[-1])
                raw_text = get_pdf_text(pdf_path)
                print(0)
                chunks = get_text_chunks(raw_text)
                print(1)
                vector = get_vectordb(chunks,OPENAI_API_KEY)
                print(2)
                convo = memorydb(vector,OPENAI_API_KEY)
                print(3)

                # Lock the global variables while updating
                with vector_db_lock:
                    global_vector_db = vector
                    global_convo_chain = convo



                return JsonResponse({'message': 'CSV11 uploaded successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")

# View for chatting with the bot


@csrf_exempt
def chat_with_bot(request):
    if request.method == 'POST':
        msg_data = json.loads(request.body.decode('utf-8'))
        msg = msg_data.get('message')

        if msg:
            try:
                # load_dotenv()



                # Check if a PDF has been uploaded
                with vector_db_lock:
                    vector_db = global_vector_db
                    convo_chain = global_convo_chain

                if not vector_db or not convo_chain:
                    return JsonResponse({'error': 'No PDF file uploaded'}, status=400)

                # Use the stored vector database and conversation chain for chat
                output = convo_chain.run(msg)
                return JsonResponse({'output': output})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse({'error': 'No message provided'}, status=400)
    else:
        return HttpResponseBadRequest("Invalid request method")

