import os
from openai import OpenAI
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise Exception("API key not found. Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key)

@api_view(['POST'])
def text_mining(request):
    text = request.data.get('text', '')

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Extract key names, dates, places, determine sentiment, and summarize the text."},
                {"role": "user", "content": text}
            ],
            model="gpt-3.5-turbo",
            max_tokens=500
        )

        if chat_completion['choices']:
            response_text = chat_completion['choices'][0]['message']['content']
        else:
            response_text = "No response generated."

        # Determining the answer into parts for a single result
        results = response_text.strip().split('\n')
        if len(results) >= 3:
            extracted_info, sentiment, summary = results[0], results[1], results[2]
        else:
            extracted_info = sentiment = summary = "Insufficient data to extract all responses."

        return Response({
            'extracted_info': extracted_info,
            'sentiment': sentiment,
            'summary': summary
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
