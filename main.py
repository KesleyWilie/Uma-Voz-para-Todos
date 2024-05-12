import os
from google.cloud import vision
from google.cloud import texttospeech
from PIL import Image

# Defina a variável de ambiente com sua API Key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "caminho/para/sua/chave.json"

# Crie os clientes Vision e Text-to-Speech com a API Key
client_vision = vision.ImageAnnotatorClient()
client_tts = texttospeech.TextToSpeechClient()

def extrair_texto(caminho_imagem):
    """Extrai o texto de uma imagem usando a Cloud Vision API."""
    try:
        with open(caminho_imagem, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client_vision.text_detection(image=image)
        texts = response.text_annotations
        if texts:
            return texts[0].description
        else:
            return ""
    except Exception as e:
        print(f"Erro ao extrair texto da imagem: {e}")
        return ""

def texto_para_voz(texto, idioma="pt-BR", nome_arquivo="audio.mp3"):
    """Converte o texto em áudio usando a Cloud Text-to-Speech API."""
    try:
        voice = texttospeech.VoiceSelectionParams(
            language_code=idioma, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        synthesis_input = texttospeech.SynthesisInput(text=texto)
        response = client_tts.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        with open(nome_arquivo, "wb") as out:
            out.write(response.audio_content)
        print(f'Áudio salvo como "{nome_arquivo}"')
    except Exception as e:
        print(f"Erro ao converter texto em áudio: {e}")

# Solicite o caminho da imagem
caminho_imagem = input("Digite o caminho da imagem: ")

# Verifique se o caminho da imagem é válido
if not os.path.isfile(caminho_imagem):
    print("Caminho da imagem inválido.")
    exit()

# Extraia o texto da imagem
texto = extrair_texto(caminho_imagem)

# Verifique se o texto foi extraído
if texto:
    print("Texto extraído da imagem:")
    print(texto)

    # Converta o texto em áudio
    texto_para_voz(texto)
else:
    print("Nenhum texto encontrado na imagem.")
