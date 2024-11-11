"""usage docs: learn/calls.md#provider-specific-parameters"""

from __future__ import annotations

from typing import TYPE_CHECKING

from openai.types.chat import (
    ChatCompletionStreamOptionsParam,
    ChatCompletionToolChoiceOptionParam,
)
from openai.types.chat.completion_create_params import ResponseFormat
from typing_extensions import NotRequired

from ..base import BaseCallParams
from ..base.call_params import CommonCallParams, convert_params

if TYPE_CHECKING:
    from openai.types.chat.chat_completion_audio_param import (  # pyright: ignore [reportMissingImports]
        ChatCompletionAudioParam,
        ChatCompletionModality,  # pyright: ignore [reportAttributeAccessIssue]
    )
else:
    try:
        from openai.types.chat.chat_completion_audio_param import (  # pyright: ignore [reportMissingImports]
            ChatCompletionAudioParam,
            ChatCompletionModality,
        )
    except ImportError:

        class ChatCompletionAudioParam: ...

        class ChatCompletionModality: ...


class OpenAICallParams(BaseCallParams):
    """The parameters to use when calling the OpenAI API.

    [OpenAI API Reference](https://platform.openai.com/docs/api-reference/chat/create)

    Attributes:
        audio: ...
        frequency_penalty: ...
        logit_bias: ...
        logprobs: ...
        max_tokens: ...
        modalities: ...
        n: ...
        parallel_tool_calls: ...
        presence_penalty: ...
        response_format: ...
        seed: ...
        stop: ...
        stream_options: ...
        temperature: ...
        tool_choice: ...
        top_logprobs: ...
        top_p: ...
        user: ...
    """

    audio: NotRequired[ChatCompletionAudioParam | None]
    extra_headers: NotRequired[dict[str, str] | None]
    frequency_penalty: NotRequired[float | None]
    logit_bias: NotRequired[dict[str, int] | None]
    logprobs: NotRequired[bool | None]
    max_tokens: NotRequired[int | None]
    modalities: NotRequired[list[ChatCompletionModality] | None]
    n: NotRequired[int | None]
    parallel_tool_calls: NotRequired[bool]
    presence_penalty: NotRequired[float | None]
    response_format: NotRequired[ResponseFormat]
    seed: NotRequired[int | None]
    stop: NotRequired[str | list[str] | None]
    stream_options: NotRequired[ChatCompletionStreamOptionsParam | None]
    temperature: NotRequired[float | None]
    tool_choice: NotRequired[ChatCompletionToolChoiceOptionParam]
    top_logprobs: NotRequired[int | None]
    top_p: NotRequired[float | None]
    user: NotRequired[str]


def get_openai_call_params_from_common(params: CommonCallParams) -> OpenAICallParams:
    """Converts common call parameters to OpenAI-specific call parameters."""
    mapping = {
        "temperature": "temperature",
        "max_tokens": "max_tokens",
        "top_p": "top_p",
        "frequency_penalty": "frequency_penalty",
        "presence_penalty": "presence_penalty",
        "seed": "seed",
        "stop": "stop",
    }
    return convert_params(params, mapping, OpenAICallParams)
