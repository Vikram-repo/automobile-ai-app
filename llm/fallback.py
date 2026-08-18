import logging
import time

from langchain_core.runnables import Runnable


logger = logging.getLogger(__name__)


class LLMFallback(Runnable):

    def __init__(self, primary, fallback, max_retries=1):
        self.primary = primary
        self.fallback = fallback
        self.max_retries = max_retries

    def invoke(self, input, config=None, **kwargs):

        # PRIMARY + RETRY
        for attempt in range(self.max_retries + 1):

            start = time.perf_counter()

            try:
                logger.info(
                    "LLM_PRIMARY_START attempt=%s",
                    attempt + 1,
                )

                response = self.primary.invoke(
                    input,
                    config=config,
                    **kwargs,
                )

                elapsed = time.perf_counter() - start

                logger.info(
                    "LLM_PRIMARY_SUCCESS provider=ollama attempt=%s elapsed=%.2fs",
                    attempt + 1,
                    elapsed,
                )

                return response

            except Exception as primary_error:

                elapsed = time.perf_counter() - start

                logger.warning(
                    "LLM_PRIMARY_FAILED provider=ollama attempt=%s elapsed=%.2fs error=%s",
                    attempt + 1,
                    elapsed,
                    primary_error,
                )

                # Retry if attempts remain
                if attempt < self.max_retries:
                    logger.info(
                        "LLM_PRIMARY_RETRY next_attempt=%s",
                        attempt + 2,
                    )
                    continue

        # FALLBACK
        fallback_start = time.perf_counter()

        try:
            logger.info(
                "LLM_FALLBACK_START provider=azure_foundry model=gpt-4.1"
            )

            response = self.fallback.invoke(
                input,
                config=config,
                **kwargs,
            )

            fallback_elapsed = time.perf_counter() - fallback_start

            logger.info(
                "LLM_FALLBACK_SUCCESS provider=azure_foundry model=gpt-4.1 elapsed=%.2fs",
                fallback_elapsed,
            )

            return response

        except Exception as fallback_error:

            logger.error(
                "LLM_FALLBACK_FAILED provider=azure_foundry error=%s",
                fallback_error,
            )

            raise RuntimeError(
                "Both primary and fallback LLMs failed."
            ) from fallback_error
