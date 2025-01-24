"""Tests the `google.call_response_chunk` module."""

from google.genai.types import (
    Candidate,
    Content,
    GenerateContentResponse,
    Part,
)
from google.genai.types import (
    FinishReason as GoogleFinishReason,
)

from mirascope.core.google.call_response_chunk import GoogleCallResponseChunk


def test_google_call_response_chunk() -> None:
    """Tests the `GoogleCallResponseChunk` class."""
    chunk = GenerateContentResponse(
        candidates=[
            Candidate(
                finish_reason=GoogleFinishReason.STOP,
                content=Content(
                    parts=[Part(text="The author is Patrick Rothfuss")],
                    role="model",
                ),
            )
        ]
    )

    call_response_chunk = GoogleCallResponseChunk(chunk=chunk)
    assert call_response_chunk.content == "The author is Patrick Rothfuss"
    assert call_response_chunk.finish_reasons == [GoogleFinishReason.STOP]
    assert call_response_chunk.model is None
    assert call_response_chunk.id is None
    assert call_response_chunk.usage is None
    assert call_response_chunk.input_tokens is None
    assert call_response_chunk.output_tokens is None
