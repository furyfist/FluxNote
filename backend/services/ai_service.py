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
        Build the prompt for Gemini to match lectures

        Args:
            syllabus_text: Raw syllabus content
            lectures: List of YouTube videos
        
        Returns:
            Formatted prompt string
        """
        # Format lecture list
        lecture_list = "\n".join([
            f"{i+1}. {video.title} (Position: {video.position})"
            for i, video in enumerate(lectures)
        ])

        prompt = f"""You are an expert course planner. Your task is to match syllabus topics to relevant lectures from a YouTube playlist.

**SYLLABUS:**
{syllabus_text}

**AVAILABLE LECTURES:**
{lecture_list}

**INSTRUCTIONS:**
1. Parse the syllabus and identify distinct topics/modules/weeks
2. For each topic, find the MOST RELEVANT lecture(s) from the list above
3. Use the lecture number EXACTLY as shown in the list (e.g., if you see "5. Database Design", use lecture_number: 5)
4. Arrange lectures in the ORDER they should be watched (follow syllabus sequence)
5. Provide reasoning for each match
6. Assign a confidence score (0.0 to 1.0) for each match

**CRITICAL: Use lecture numbers from 1 to {len(lectures)} ONLY**

**OUTPUT FORMAT (STRICT JSON - NO OTHER TEXT):**
{{
  "matches": [
    {{
      "topic": "exact topic text from syllabus",
      "matched_lectures": [
        {{
          "lecture_number": 1,
          "title": "exact title from lecture list",
          "reasoning": "why this lecture matches this topic",
          "confidence": 0.95,
          "order": 1
        }}
      ]
    }}
  ]
}}

**RULES:**
- Return ONLY valid JSON, no explanatory text before or after
- lecture_number must be between 1 and {len(lectures)}
- Each topic should have 1-3 most relevant lectures
- Order field indicates watch sequence (1, 2, 3...)
- If no good match exists, confidence should be < 0.5

Generate ONLY the JSON:"""

        return prompt

    def match_lectures(
        self, 
        syllabus_text: str,
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
            # ========================================================================
            # TESTING MODE: Load from saved JSON file (comment out for live API calls)
            # ========================================================================
            with open('AIResponse.json', 'r', encoding='utf-8') as f:
                result = json.load(f)
            response_text = json.dumps(result)  # For debug printing
            
            # ========================================================================
            # PRODUCTION MODE: Uncomment below to use actual Gemini API
            # ========================================================================
            # # Call Gemini API with new SDK
            # response = self.client.models.generate_content(
            #     model='gemini-2.0-flash-exp',
            #     contents=prompt,
            #     config=genai.types.GenerateContentConfig(
            #         temperature=0.2,
            #         max_output_tokens=8192,
            #     )
            # )
            # 
            # # Extract text
            # response_text = response.text.strip()
            # 
            # # Clean response (remove markdown code blocks if present)
            # if response_text.startswith("```json"):
            #     response_text = response_text[7:]
            # if response_text.startswith("```"):
            #     response_text = response_text[3:]
            # if response_text.endswith("```"):
            #     response_text = response_text[:-3]
            # response_text = response_text.strip()
            # 
            # # Parse JSON
            # result = json.loads(response_text)
            # ========================================================================

            # DEBUG: Print raw response
            print("=" * 50)
            print("RAW AI RESPONSE (first 500 chars):")
            print(response_text[:500])
            print("=" * 50)

            # DEBUG: Print match statistics
            print(f"📊 Total matches in JSON: {len(result.get('matches', []))}")
            for match in result.get('matches', []):
                print(f"   Topic: {match.get('topic')}")
                print(f"   Lectures found: {len(match.get('matched_lectures', []))}")

            # Convert to Pydantic models
            topic_matches = []

            for match in result.get('matches', []):
                matched_lectures = []

                # CRITICAL FIX: Iterate over match.get(), NOT result.get()
                for lec in match.get('matched_lectures', []):
                    # Find the actual video by lecture number
                    lecture_num = lec.get('lecture_number', 0)
                    
                    # Validate lecture number is in range
                    if 1 <= lecture_num <= len(lectures):
                        video = lectures[lecture_num - 1]  # Convert to 0-indexed

                        matched_lectures.append(MatchedLecture(
                            title=video.title,
                            url=video.url,
                            reasoning=lec.get('reasoning', 'No reasoning provided'),
                            confidence=float(lec.get('confidence', 0.5)),
                            order=int(lec.get('order', 1))
                        ))
                    else:
                        # Debug: Log if lecture number is out of range
                        print(f"⚠️  Lecture number {lecture_num} out of range (1-{len(lectures)})")
                
                # Add topic with its matched lectures
                topic_matches.append(TopicMatch( 
                    topic=match.get('topic', 'Unknown Topic'),
                    matched_lectures=matched_lectures
                ))
            
            return topic_matches
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parse Error: {str(e)}")
            raise ValueError(f"Failed to parse AI response as JSON: {str(e)}")
        
        except Exception as e:
            print(f"❌ Matching Error: {str(e)}")
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
                model='gemini-2.0-flash-exp',
                contents=prompt
            )
            result = json.loads(response.text.strip())
            return result
        except:
            return {"topic_count": 0, "summary": "Unable to analyze"}


# ============================================================================
# TESTING / USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    service = AIMatchingService()
    
    # Test data
    test_syllabus = """
    Week 1: Introduction to Databases
    Week 2: SQL Basics and Queries
    Week 3: Database Normalization
    Week 4: Transactions and ACID Properties
    """
    
    test_lectures = [
        YouTubeVideo(
            title="Database Fundamentals - Complete Guide",
            video_id="abc123",
            url="https://youtube.com/watch?v=abc123",
            position=1
        ),
        YouTubeVideo(
            title="SQL Tutorial for Beginners",
            video_id="def456",
            url="https://youtube.com/watch?v=def456",
            position=2
        ),
        YouTubeVideo(
            title="Normalization Explained (1NF, 2NF, 3NF)",
            video_id="ghi789",
            url="https://youtube.com/watch?v=ghi789",
            position=3
        )
    ]
    
    print("Matching lectures to syllabus...\n")
    matches = service.match_lectures(test_syllabus, test_lectures)
    
    for match in matches:
        print(f"📚 {match.topic}")
        for lec in match.matched_lectures:
            print(f"   → {lec.title}")
            print(f"      Confidence: {lec.confidence:.2f} | Order: {lec.order}")
            print(f"      Reason: {lec.reasoning}")
            print(f"      Link: {lec.url}\n")