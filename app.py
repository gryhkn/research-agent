import requests
import json
from langchain.prompts import PromptTemplate
from langchain.agents import AgentType, Tool, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationSummaryBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.tools import Tool
import trafilatura
import streamlit as st
from langchain.schema import SystemMessage
import os
from dotenv import load_dotenv
from elevenlabs import generate

load_dotenv()
serper_api_key = os.getenv("SERP_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")


def web_search(search_term):
    api_endpoint = "https://google.serper.dev/search"

    # request parameters
    payload = json.dumps({
        "q": search_term
    })

    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    # search api
    response = requests.request("POST", api_endpoint, headers=headers, data=payload)

    if response.ok:
        search_results = response.json()
        print("Search Results:", search_results)

        return search_results
    else:
        print(f"Error occurred: {response.status_code}")
        return None


def extract_and_summarize_content(objective: str, website_url: str):
    print("Extracting content from website...")

    # web içeriğini al
    downloaded = trafilatura.fetch_url(website_url)

    # trafilatura ile text'i çıkar
    extracted_text = trafilatura.extract(downloaded)

    if extracted_text:
        print("Extracted Content:", extracted_text)

        # Check if the text length exceeds a certain threshold
        if len(extracted_text) > 10000:
            summarized_content = summary(objective, extracted_text)
            return summarized_content
        else:
            return extracted_text
    else:
        print(f"Failed to extract content from the URL: {website_url}")


def summary(objective, content):
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=10000, chunk_overlap=500)
    docs = text_splitter.create_documents([content])
    map_prompt = """
    Aşağıdaki metni {objective} için özetle:
    "{text}"
    ÖZET:
    """
    map_prompt_template = PromptTemplate(
        template=map_prompt, input_variables=["text", "objective"])

    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=map_prompt_template,
        verbose=True
    )

    output = summary_chain.run(input_documents=docs, objective=objective)

    return output


tools = [
    Tool.from_function(
        func=web_search,
        name="Search",

        description= "Mevcut olaylar ve veriler hakkında soruları yanıtlamak için kullanılır. Hedefe yönelik sorular sorun"
    ),
    Tool.from_function(
        func=lambda objective, url: extract_and_summarize_content(objective, url),
        name="ScrapeWebsite",
        description="Bir web sitesi URL'inden veri almak için kullanılır; hem URL'i hem de amacınızı bu fonksiyona yazın."
    )
]

system_message = SystemMessage(
    content="""
            Sen dünyanın en iyi araştırmacısısın. Sana verilen konuyu detaylıca araştırır ve gerçek verilere dayanarak
            sonuçlar üretirsin. Asla ama asla uydurma ve gerçek olmayan bilgiler vermez ve araştırmanı destekleyecek en gerçek verileri toplamaya çalışırsın.

            Lütfen yukarıdaki uyarıları dikkate al ve aşağıdaki kurallara uy:
            1/ Sana verilen göre hakkında mümkün olduğunca çok bilgi topla ve yeterince araştırma yap.
            2/ İlgili bağlantılar ve makalelerin URL'leri varsa, daha fazla bilgi toplamak için bunları da tara.
            3/ Tarama ve arama sonrasında, "Topladığım verilere dayanarak araştırma kalitesini artırmak için araştırmam ve taramam gereken yeni şeyler var mı?" diye düşün. Eğer cevap evetse devam et; Ancak bunu 3 kezden fazla yapma.
            4/ Kesinlikle uydurma bilgiler verme/yazma, sadece bulduğun ve topladığın gerçek bilgileri yaz.
            5/ Nihai çıktıda, araştırmanı desteklemek için tüm referans verileri ve bağlantıları da yaz. 
            6/ Her zaman açık, anlaşılır ve basit bir Türkçe ile cevap ver. """
)

agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
    "system_message": system_message,
}

llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")
memory = ConversationSummaryBufferMemory(
    memory_key="memory", return_messages=True, llm=llm, max_token_limit=1000)

agent_executor = initialize_agent(
    tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True, agent_kwargs=agent_kwargs,
    memory=memory,
)

# Agent'i çağır
# agent_executor.invoke(
#     {
#         "input": "Leonardo dicaprio'nun mevcut kız arkadaşı kim? Onunla ne zaman sevgili oldu? Kız kaç yaşında"
#     }
# )


def main():
    st.set_page_config(page_title="Araştırma Asistanı", page_icon="🔍")

    st.title("Araştırma Asistanı 🔍")
    st.markdown("""
        Merak ettiğiniz konuyu girin ve detaylı araştırma sonuçlarını hemen alın.
    """)
    st.markdown("""
        Bu uygulama arka tarafta Google Search ve Langchain kullanarak sorduğunuz veya araştırma konunusu için internette araştırma yapar, bulduğu sonuçlar aratılan konu ile ilgili
        değilse başka kaynakları tarar. Bu sayede sorduğunuz soruya birden fazla kaynaklı doğru cevaplar verir. Tüm bunları Langhcain ile oluşturulan iki farklı AI Agent ile yapar.
        Ayrıca eğer ElevenLabs API Key girerseniz, bulduğu sonucu seslendirir.     
        """)
    st.markdown("""
        Uygulamanın çalışabilmesi için OpenAI ve SERP API Key girmek zorunlu, seslendirme istemezseniz Elevenlabs kısmını boş bırakın.
        """)
    st.markdown("X'te bana ulaşın: [**:blue[Giray]**](https://twitter.com/gryhkn)")

    # örnek
    if 'init' not in st.session_state:
        st.session_state['init'] = True

        st.session_state['initial_text'] = """
        bir süredir resmen hayat felsefesi yapılacak iki cümle kafamda yankılanıp duruyor.
        ilki carl jung’tan:
        “dünya sana kim olduğunu soracak, eğer cevabı bilmiyorsan o söyleyecek.”
        ikincisi de david hume’dan:
        “eğer burada durup daha ileri gitmeyeceksek, niçin bu noktaya kadar geldik?”
        """
        st.session_state['initial_audio'] = "first wav carl.wav"  # Local ses dosyasının yolu

    query = st.text_input("Araştırma Konusu", help="Araştırmak istediğiniz konuyu buraya yazın.")
    search_button_clicked = st.button("Ara", key="search")
    st.divider()


    if search_button_clicked and query:
        # kullanıcı input
        with st.spinner(f"'{query}' için araştırma yapılıyor..."):
            result = agent_executor({"input": query})
            st.success("Araştırma tamamlandı!")
            st.info(result['output'])
            if elevenlabs_api_key:
                audio = generate(
                    text=result['output'],
                    voice="Bella",
                    model='eleven_multilingual_v2'
                )
                st.audio(audio, format='audio/wav')
        st.session_state['init'] = False
    elif st.session_state['init']:
        st.text("ÖRNEK:")
        # başlangıç değerlerini göster
        st.markdown(st.session_state['initial_text'])
        st.audio(st.session_state['initial_audio'], format='audio/wav')

    st.sidebar.image("assistant.jpg", caption='')
    st.sidebar.info("Overwatch")

if __name__ == "__main__":
    main()

#extract_and_summarize_content("Montgisard Muharebesini kim kazanmıştır?", "https://tr.wikipedia.org/wiki/Montgisard_Muharebesi#:~:text=Montgisard%20Muharebesi%2C%20Eyyubiler%20ile%20Kud%C3%BCs,ile%20Selahattin%20Eyyubi'yi%20yenmi%C5%9Ftir.")
# web_search("Meta'nın yeni Thread uygulaması nedir?")