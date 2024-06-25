"""This module contains the `AnthropicCallResponse` class."""

from anthropic.types import Message, MessageParam, ToolResultBlockParam, Usage
from pydantic import computed_field

from ..base import BaseCallResponse
from .call_params import AnthropicCallParams
from .function_return import AnthropicCallFunctionReturn
from .tool import AnthropicTool


class AnthropicCallResponse(
    BaseCallResponse[
        Message,
        AnthropicTool,
        AnthropicCallFunctionReturn,
        MessageParam,
        AnthropicCallParams,
        MessageParam,
    ]
):
    '''A convenience wrapper around the Anthropic `Message` response.

    When calling the Anthropic API using a function decorated with `anthropic_call`, the
    response will be an `AnthropicCallResponse` instance with properties that allow for
    more convenience access to commonly used attributes.

    Example:

    ```python
    from mirascope.core.anthropic import anthropic_call

    @anthropic_call(model="claude-3-5-sonnet-20240620")
    def recommend_book(genre: str):
        """Recommend a {genre} book."""

    response = recommend_book("fantasy")  # response is an `AnthropicCallResponse` instance
    print(response.content)
    #> Sure! I would recommend...
    ```
    '''

    @computed_field
    @property
    def message_param(self) -> MessageParam:
        """Returns the assistants's response as a message parameter."""
        return self.response.model_dump(include={"content", "role"})

    @property
    def content(self) -> str:
        """Returns the string text of the 0th text block."""
        block = self.response.content[0]
        return block.text if block.type == "text" else ""

    @property
    def model(self) -> str:
        """Returns the name of the response model."""
        return self.response.model

    @property
    def id(self) -> str:
        """Returns the id of the response."""
        return self.response.id

    @property
    def finish_reasons(self) -> list[str]:
        """Returns the finish reasons of the response."""
        return [str(self.response.stop_reason)]

    @computed_field
    @property
    def tools(self) -> list[AnthropicTool] | None:
        """Returns any available tool calls as their `AnthropicTool` definition.

        Raises:
            ValidationError: if a tool call doesn't match the tool's schema.
        """
        if not self.tool_types:
            return None

        extracted_tools = []
        for tool_call in self.response.content:
            if tool_call.type != "tool_use":
                continue
            for tool_type in self.tool_types:
                if tool_call.name == tool_type._name():
                    tool = tool_type.from_tool_call(tool_call)
                    extracted_tools.append(tool)
                    break

        return extracted_tools

    @computed_field
    @property
    def tool(self) -> AnthropicTool | None:
        """Returns the 0th tool for the 0th choice message.

        Raises:
            ValidationError: if the tool call doesn't match the tool's schema.
        """
        if tools := self.tools:
            return tools[0]
        return None

    @classmethod
    def tool_message_params(
        cls, tools_and_outputs: list[tuple[AnthropicTool, str]]
    ) -> list[MessageParam]:
        """Returns the tool message parameters for tool call results."""
        return [
            {
                "role": "user",
                "content": [
                    ToolResultBlockParam(
                        tool_use_id=tool.tool_call.id,
                        type="tool_result",
                        content=[{"text": output, "type": "text"}],
                    )
                    for tool, output in tools_and_outputs
                ],
            }
        ]

    @property
    def usage(self) -> Usage:
        """Returns the usage of the message."""
        return self.response.usage

    @property
    def input_tokens(self) -> int:
        """Returns the number of input tokens."""
        return self.usage.input_tokens

    @property
    def output_tokens(self) -> int:
        """Returns the number of output tokens."""
        return self.usage.output_tokens

    def __str__(self) -> str:
        """Returns the string content of the response."""
        return self.content
