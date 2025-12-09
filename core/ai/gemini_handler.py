#!/usr/bin/env python3

"""
Gemini AI service for content summarization.

Handles interactions with Google's Gemini API for text summarization.
"""

import os
from typing import Optional
from google import genai
from google.genai import types
from core.constants import GEMINI_API_KEY


class GeminiService:
    """Service class to handle Gemini API interactions for summarization."""

    def __init__(self):
        api_key = GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")

        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-flash"

    def summarize_text(self, text: str, max_length: Optional[int] = None) -> str:
        """
        Summarize text content using Gemini API.

        Args:
            text: The text content to summarize
            max_length: Optional maximum length for the summary in words

        Returns:
            Summarized text

        Raises:
            Exception: If API call fails
        """
        if not text or not text.strip():
            raise ValueError("Text content cannot be empty")

        # Build prompt
        prompt = "Please provide a concise summary of the following text:\n\n"
        if max_length:
            prompt = f"Please provide a concise summary (max {max_length} words) of the following text:\n\n"

        prompt += text

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,  # Lower temperature for more focused summaries
                    max_output_tokens=500,
                ),
            )

            return response.text.strip()

        except Exception as e:
            raise Exception(f"Failed to summarize text: {str(e)}")


# Singleton instance
_gemini_service = None


def get_gemini_service() -> GeminiService:
    """Get or create GeminiService singleton instance."""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service
