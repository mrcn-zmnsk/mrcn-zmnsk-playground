from typing import Type
from langchain.tools import BaseTool
from pydantic import Field, BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
import dotenv

class YTTranscriptToolInput(BaseModel):
    video_id: str = Field(..., description="The ID of the YouTube video to get the transcript for, e.g. `1htKBjuUWec`")

class YTTranscriptTool(BaseTool):

    name: str = "YTTranscript_tool"
    description: str = "A tool for getting audio transcript of a YouTube video."
    args_schema: Type[BaseModel] = YTTranscriptToolInput

    api : YouTubeTranscriptApi = YouTubeTranscriptApi()

    def _run(self, video_id: str) -> str:
        transcript = self.api.fetch(video_id)
        result = "\n".join([ f'[{t.start}] {t.text}' for t in transcript])
        return result


