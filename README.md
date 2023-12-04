# Araştırma Asistanı

## Genel Bakış

Araştırma Asistanı, Langchain ve çeşitli API'ler kullanarak kullanıcıların detaylı araştırmalar yapmasını sağlayan bir Streamlit uygulamasıdır. Bu uygulama, OpenAI GPT-4 modeli, Google SERP ve ElevenLabs gibi çeşitli hizmetlerden yararlanarak, kullanıcıların metin tabanlı sorgularına yanıt verir.

Tüm bunları Langhcain ile oluşturulan iki farklı AI Agent ile yapar.

![](https://github.com/gryhkn/research-agent/blob/master/ss.png?raw=true)

## Özellikler

- **Metin Tabanlı Sorgulama**: Kullanıcılar herhangi bir konu hakkında soru sorabilir ve AI destekli yanıtlar alabilir.
- **Web İçeriği Özeti**: Web sitelerinden içerik çekme ve bu içeriği özetleme yeteneği.
- **Sesli Yanıt**: ElevenLabs API'si kullanılarak, bulduğu cevapları seslendirme.


## Başlarken

Bu bölüm, projeyi kendi bilgisayarınızda nasıl çalıştıracağınıza dair talimatları içerir.

### Gereksinimler

Projeyi çalıştırmadan önce aşağıdaki araçların yüklü olduğundan emin olun:

- Python 3.7 veya daha yeni bir sürüm
- pip (Python paket yöneticisi)
- virtualenv (isteğe bağlı, önerilir)

### Kurulum

Projeyi kurmak ve çalıştırmak için aşağıdaki adımları izleyin:

1. Repoyu klonlayın:

    ```
    git clone https://github.com/gryhkn/research-agent.git
    cd research-agent
    ```

2. Bir Python sanal ortamı oluşturun (isteğe bağlı):

    ```
    python -m venv venv
    ```

3. Sanal ortamı aktifleştirin(mac):

    ```
    source venv/bin/activate
    ```

4. Gerekli paketleri yükleyin:

    ```
   pip install -r requirements.txt
   ```
5. Uygulamayı çalıştırmak için aşağıdaki komutu kullanın:

    ```
   streamlit run app.py
   ```
   
6. Son olarak [ElevenLabs](https://elevenlabs.io/), [OpenAI](https://openai.com/), [SERP](https://serper.dev/) 
hesapları oluşturup API key'leri alın ve .env dosyası oluşturup burada tanımlayın.


<hr>

### .env kullanmadan

.env dosyası kullanmadan direkt uygulama ekranından API Key'leri girerek de uygulamayı çalıştırabilirsiniz.
Bunun için yapmanız gereken tek şey, yine repoyu indirmek ve

```
streamlit run streamlit_deploy.py
```

kodunu çalıştırmak.


### Elevenlabs seslendirme
Elevenlabs seslendirmesi için ```eleven_multilingual_v2``` ve ```Bella``` kullanıyorum. Ama siz kendi sesinizi veya başka
bir sesi de kullanabilirsiniz. Bunun için Elevenlabs'ta çeşitli ayarlamalar yapmanız gerekiyor.
