from openai import OpenAI
import requests
import os
openai_api_key = os.getenv("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")
openai_client = OpenAI(api_key=openai_api_key)


def speech_to_text(audio_binary):

    # Set up Watson Speech-to-Text HTTP Api url
    base_url = 'https://sn-watson-stt.labs.skills.network'
    api_url = base_url+'/speech-to-text/api/v1/recognize'

    # Set up parameters for our HTTP reqeust
    params = {
        'model': 'en-US_Multimedia',
    }

    # Set up the body of our HTTP request
    body = audio_binary

    # Send a HTTP Post request
    response = requests.post(api_url, params=params, data=audio_binary).json()

    # Parse the response to get our transcribed text
    text = 'null'
    while bool(response.get('results')):
        print('speech to text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognised text: ', text)
        return text


def text_to_speech(text, voice=""):
    # Watson 음성 합성 HTTP API URL 설정
    base_url = '..https://sn-watson-tts.labs.skills.network'
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'
    # 사용자가 선호하는 음성을 선택한 경우 api_url에 음성 매개변수 추가
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice
    # HTTP 요청을 위한 헤더 설정
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }
    # HTTP 요청의 본문 설정
    json_data = {
        'text': text,
    }
    # Watson 음성 합성 서비스에 HTTP Post 요청 전송
    response = requests.post(api_url, headers=headers, json=json_data)
    print('음성 합성 응답:', response)
    return response.content


def openai_process_message(user_message):
    # OpenAI API를 위한 프롬프트 설정
    prompt = "개인 비서처럼 행동하세요. 질문에 답변하고, 문장을 번역하고, 뉴스를 요약하고, 추천을 할 수 있습니다."
    # OpenAI API를 호출하여 프롬프트 처리
    openai_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=4000
    )
    print("openai 응답:", openai_response)
    # 응답을 파싱하여 프롬프트에 대한 응답 메시지 가져오기
    response_text = openai_response.choices[0].message.content
    return response_text
