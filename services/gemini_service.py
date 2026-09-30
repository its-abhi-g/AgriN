import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from models.analysis import AgriculturalAnalysis
from prompts.agriculture import create_analysis_prompt


load_dotenv(override=True)


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=15000
        ),
    )


def analyze_farm_problem(
    query: str,
    language: str = "Auto Detect",
    state: str = "",
    district: str = "",
    crop: str = "",
    crop_stage: str = "",
    irrigation: str = "",
) -> AgriculturalAnalysis:

    client = get_client()

    model_name = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.1-flash-lite"
    )

    prompt = create_analysis_prompt(
        query=query,
        language=language,
        state=state,
        district=district,
        crop=crop,
        crop_stage=crop_stage,
        irrigation=irrigation,
    )

    last_error = None

    # Retry temporary Gemini service failures
    for attempt in range(1):

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    response_mime_type="application/json",
                    response_schema=AgriculturalAnalysis,
                ),
            )

            if response.parsed:
                return response.parsed

            if response.text:
                return AgriculturalAnalysis.model_validate_json(
                    response.text
                )

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        except Exception as error:
            last_error = error

            error_text = str(error)

            # Retry only temporary service problems
            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
                or "high demand" in error_text.lower()
            ):
                if attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue

            # Do not retry invalid key, invalid model, etc.
            raise

    raise RuntimeError(
        "Gemini is temporarily unavailable after multiple retries."
    ) from last_error
