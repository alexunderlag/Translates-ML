from quart import Quart, request, jsonify, render_template
from transformers import MarianMTModel, MarianTokenizer

app = Quart(__name__)

# Загрузка моделей и токенизаторов
tokenizers = {
    "ru-en": MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en"),
    "en-ru": MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
}
models = {
    "ru-en": MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-ru-en"),
    "en-ru": MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
}

@app.route("/translate", methods=["POST"])
async def translate_text():
    content = await request.json
    text = content['text']
    lang = content['lang']

    tokenizer = tokenizers[lang]
    model = models[lang]

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    translated = model.generate(**inputs)
    translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]

    return jsonify({"translation": translated_text})

@app.route("/", methods=["GET", "POST"])
async def index():
    translation = None  # Если нет запроса на перевод, оставляем пустым
    if request.method == "POST":
        try:
            data = await request.form
            text = data.get("text")
            lang = data.get("lang")

            # Процесс перевода, аналогичный функции translate_text
            tokenizer = tokenizers[lang]
            model = models[lang]
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            translated = model.generate(**inputs)
            translation = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]

        except Exception as e:
            translation = str(e)  # Отображаем ошибку в качестве "перевода"

    return await render_template("index.html", translation=translation)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)