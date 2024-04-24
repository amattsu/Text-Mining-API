from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dotenv import load_dotenv
import os
import openai


@api_view(['POST'])
def text_mining(request):
    text = request.data.get('text', '')
    openai.api_key = os.getenv('OPENAI_API_KEY')

    response_info = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=f"Identify and extract important names, dates, places from the following text: {text}",
        max_tokens=150
    )

    response_sentiment = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=f"Determine the sentiment of the following text: {text}",
        max_tokens=60
    )

    response_summary = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=f"Summarize the following text: {text}",
        max_tokens=100
    )

    return Response({
        'extracted_info': response_info.choices[0].text.strip(),
        'sentiment': response_sentiment.choices[0].text.strip(),
        'summary': response_summary.choices[0].text.strip()
    })
