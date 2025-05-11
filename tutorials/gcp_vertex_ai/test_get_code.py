from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        vertexai=True,
        project="agentoc",
        location="us-central1",
    )
    model = "gemini-2.0-flash-001"
    contents = [
        types.Content(
            role="user", parts=[types.Part.from_text(text="""What is MCP inspector?"""),]
        ),
    ]
    tools = [
        types.Tool(
            retrieval=types.Retrieval(
                vertex_ai_search=types.VertexAISearch(
                    datastore="projects/agentoc/locations/global/collections/default_collection/dataStores/agentoc-data-sources_1746981317464"
                )
            )
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"
            ),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        tools=tools,
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            not chunk.candidates
            or not chunk.candidates[0].content
            or not chunk.candidates[0].content.parts
        ):
            continue
        print(chunk.text, end="")


generate()
