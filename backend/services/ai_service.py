from google import genai
import os
import json
from typing import List, Dict, Any
from models.schemas import YouTubeVideo, TopicMatch, MatchedLecture

class AIMatchingService:
    """
    Handles intelligent lecture matching using Google Gemini
    """

    def __init__(self, api_key: str = None):
        """
        Initialize Gemini API client

        Args: 
            api_key: Google Gemini API key (loads from the env)
        """
        
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API Key is not Found")

        # Initialize Gemini client 
        self.client = genai.Client(api_key=self.api_key)

    def _build_prompt(self, syllabus_text: str, lectures: List[YouTubeVideo]) -> str:
        """
        Buid the prompt for Gemini to match lectures

        Args:
            syllabus_text: Raw syllabus content
            lectures: List of YouTube videos
        
        Returns:
            Formatted prompt string
        """
        # Format lecture list
        lecture_list = "\n".join([
            f"{i+1}, {video.title} (Position: {video.position})"
            for i, video in enumerate(lectures)
        ])

        prompt = f"""You are an expert course planner. Your task is to match syllabus topics to relevant lectures from a YouTube playlist.

        **SYLLABUS:**
        {syllabus_text}

        **AVAILABLE LECTURES:**
        {lecture_list}

        **INSTRUCTIONS:**
        1. Parse the syllabus and identify distinct topics/modules/weeks
        2. For each topic, find the MOST RELEVANT lecture(s) from the list
        3. Arrange lectures in the ORDER they should be watched (follow syllabus sequence)
        4. Provide reasoning for each match
        5. Assign a confidence score (0.0 to 1.0) for each match

        **OUTPUT FORMAT (STRICT JSON):**
        {{
        "matches": [
            {{
            "topic": "exact topic text from syllabus",
            "matched_lectures": [
                {{
                "lecture_number": 1,
                "title": "lecture title",
                "reasoning": "why this lecture matches this topic",
                "confidence": 0.95,
                "order": 1
                }}
            ]
            }}
        ]
        }}

        **RULES:**
        - Return ONLY valid JSON, no extra text
        - Each topic should have at least 1 lecture (if relevant match exists)
        - Order field should indicate watch sequence (1, 2, 3...)
        - Confidence should reflect how well the lecture matches the topic
        - If no good match exists, set confidence < 0.3 and explain in reasoning

        Generate the JSON now:"""

        return prompt

    def matched_lectures(
        self, 
        syllabus_text:str,
        lectures: List[YouTubeVideo]
    ) -> List[TopicMatch]:
        """
        Match syllabus topics to lectures using Gemini AI

        Args:
            syllabus_text: Full syllabus content
            lectures: List of YouTube videos from playlist

        Returns:
            List of TopicMatch objects with matched lectures

        Raises:
            ValueError: If API fails or returns invalid JSON
        """
        if not syllabus_text.strip():
            raise ValueError("Syllabus text cannot be empty")
        
        if not lectures:
            raise ValueError("No lectures Provided")

        # Build Prompt
        prompt = self._build_prompt(syllabus_text, lectures)

        try:
            # Call Gemini Api with new SDK
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=4096,
                )
            )

            # Extract text
            response_text = response.text.strip()

            # Clean response (remove markdown code blocks if present)
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            # Parse JSON
            result = json.loads(response_text)

            # Convert to Pydantic models
            topic_matches = []

            for match in result.get('matches', []):
                matched_lectures = []

                for lec in result.get('matched_lectures', []):
                    # Find the actual video by lecture number
                    lecture_num = lec.get('lecture_number', 0)
                    if 1 <= lecture_num <= len(lectures):
                        video = lectures[lecture_num - 1]

                        matched_lectures.append(MatchedLecture(
                            title=video.title,
                            url=video.url,
                            reasoning=lec.get('reasoning', 'No reasoning provided'),
                            confidence=lec.get('confidence', 0.5),
                            order=lec.get('order', 1)
                        ))
                topic_matches.append(TopicMatch( 
                    topic = match.get('topic', 'Unknown Topic'),
                    matched_lectures=matched_lectures
                ))
            return topic_matches
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {str(e)}")
        
        except Exception as e:
            raise ValueError(f"AI matching failed: {str(e)}")

        
        def get_quick_summary(self, syllabus_text: str) -> Dict[str, Any]:
            """
            Get a quick analysis of the syllabus

            Args:
                syllabus_text: Syllabus content

            Returns:
                Dictionary with topic count and brief summary
            """
            prompt = f"""Analyze this syllabus and provide:
                1. Number of distinct topics/modules
                2. Brief summary of course content

                Syllabus:
                {syllabus_text}

                Return as JSON:
                {{
                "topic_count": <number>,
                "summary": "<brief description>"
            }}"""

            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                result = json.loads(response.text.strip())
                return result
            except:
                return {"topic_count": 0, "summary": "Unable to analyze"}

