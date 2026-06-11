import json
from typing import Any, Dict, List

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from logger import get_logger

log = get_logger("scrap_pad")


# ---------------------------------------------------------------------------
# 1. Interceptor Callback — hooks into LangChain's LLM lifecycle events
# ---------------------------------------------------------------------------

class ToolCallLoggingHandler(BaseCallbackHandler):
    """
    Custom QA callback that intercepts raw LLM I/O before LangChain parses it.

    Useful for verifying that the model is issuing the correct tool-call JSON
    rather than returning a plain text response.
    """

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Fires immediately before the prompt is sent to the remote LLM API."""
        model_id = serialized.get("kwargs", {}).get("model", "unknown-model")
        log.info("LLM request dispatched — model=%s", model_id)
        log.debug("Full prompt payload sent to LLM:\n%s", prompts[0])

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Fires the moment the LLM responds, before LangChain post-processes it."""
        log.info("LLM response received — scanning generation artifacts")

        for i, generation_group in enumerate(response.generations):
            for j, generation in enumerate(generation_group):
                message = generation.message

                if hasattr(message, "tool_calls") and message.tool_calls:
                    log.info(
                        "Tool-call payload detected in generation [group=%d, idx=%d] "
                        "— model decided to route to a tool instead of answering directly",
                        i, j,
                    )
                    for call in message.tool_calls:
                        log.info(
                            "Tool routing decision → function='%s'  args=%s  call_id=%s",
                            call["name"],
                            call["args"],
                            call.get("id"),
                        )
                        # DEBUG level captures the full structured JSON for later analysis
                        log.debug(
                            "Structured tool-call log entry:\n%s",
                            json.dumps(
                                {
                                    "action": "llm_tool_routing",
                                    "target_function": call["name"],
                                    "generated_arguments_json": call["args"],
                                    "internal_call_id": call.get("id"),
                                },
                                indent=2,
                            ),
                        )
                else:
                    log.info(
                        "Standard text response (no tool call) in generation [group=%d, idx=%d]: '%s'",
                        i, j, message.content,
                    )

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Fires when LangChain begins executing a tool."""
        tool_name = serialized.get("name", "unknown-tool")
        log.info("Tool execution started — tool='%s'  input='%s'", tool_name, input_str)

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Fires when a tool returns its result back to the agent."""
        log.info("Tool execution finished — output='%s'", output)


# ---------------------------------------------------------------------------
# 2. EV charging-station mock tool
# ---------------------------------------------------------------------------

@tool
def get_charging_stations(zip_code: str) -> str:
    """Fetches total count of EV charging stations within a specific US Zip Code."""
    log.debug("get_charging_stations invoked — zip_code='%s'", zip_code)
    result = f"Zip {zip_code}: 4 ChargePoint stations."
    log.debug("get_charging_stations returning — result='%s'", result)
    return result


# ---------------------------------------------------------------------------
# 3. Model + tool binding
# ---------------------------------------------------------------------------

log.debug("Initialising ChatGoogleGenerativeAI — model=gemini-2.5-flash, temperature=0.0")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)

log.debug("Binding tool 'get_charging_stations' to the LLM")
llm_with_tools = llm.bind_tools([get_charging_stations])


# ---------------------------------------------------------------------------
# 4. Main execution
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    prompt = "Find charging options in 98101"

    log.info("=" * 60)
    log.info("scrap_pad — execution started")
    log.info("Scenario : EV charging station lookup via LLM tool call")
    log.info("Model    : gemini-2.5-flash")
    log.info("Tool     : get_charging_stations(zip_code)")
    log.info("Prompt   : '%s'", prompt)
    log.info("=" * 60)

    callback_handler = ToolCallLoggingHandler()
    log.debug("ToolCallLoggingHandler instantiated and attached to invocation config")

    log.info("Invoking LLM — expecting it to recognise the zip-code intent and call the tool")
    response = llm_with_tools.invoke(prompt, config={"callbacks": [callback_handler]})

    log.info("Final response content: '%s'", response.content)
    log.info("=" * 60)
    log.info("scrap_pad — execution finished")
    log.info("=" * 60)
