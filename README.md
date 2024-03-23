# News_RAG

The project uses RAG(Retrieval Augmented Generation) for content generation chat bot.

- RAG is ... before knowing rag you must know about llms which comes under GEN AI and used for text generation, RAG is just adding your layer off context to llms in that way that llms uses provided context to answer any query not the data they trained on.


```
![App](https://github.com/[yo-harsh]/[news_rag]/blob/[dev]/news_app.png?raw=true)
```


## Docker Installation [🔗](https://docs.docker.com/engine/install/)

Use the this link to install docker desktop.

### Clone the Repository

To get started, clone this Git repository to your local machine:

```bash
git clone https://github.com/yo-harsh/voice_summary.git
cd voice_summary
```

## Build and Run with Django

Run django server with manage.py:

```bash
virtualenv -p python3.11 news_rag(you can try with different python version)
pip install --upgrade pip
pip install -r requirements.txt
cd project
python manage.py runserver
```

please note that i'm having trouble installing faiss and other libraries so i have not included them in requirements.

This command will run the project, the database and start the services.

## Usage

The project mainly focus on custom chatbot whcih provide personalized news to user.

- In this project i have used Django for creating a NEWS APP.
- NEWS APP takes news link and huggingface token for using inference API at huggingface endpoint.
- Project uses a scraper, faiss db, and langchain for completing the task.
- Embeddings and llm are both open source (i have also used another llm for testing purpose).
- API was made with docker and developed using AWS EC2 but later then i stoped the service.

### Access NEWS APP

Visit [localhost:8080/app]() to access the NEWS APP. Here, you can chat with chat bot.

### Access django admin

The [localhost:8080/admin](). Use this to interact with Database.

## Feedback and Suggestions

Feel free to provide feedback and suggestions.
