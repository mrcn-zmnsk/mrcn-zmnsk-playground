from typing import Type
from langchain.tools import BaseTool
from pydantic import Field, BaseModel
import openai
import dotenv

dotenv.load_dotenv()

class AudioTranscribeToolInput(BaseModel):
    file_path: str = Field(..., description="The path to the audio file to transcribe")

class AudioTranscribeTool(BaseTool):

    name: str = "AudioTranscribe_tool"
    description: str = "A tool for transcribing audio files to text."
    args_schema: Type[BaseModel] = AudioTranscribeToolInput
    
    def _run(self, file_path: str) -> str:   
        transcribed_text = openai.audio.transcriptions.create(
            file=open(f'./data/{file_path}', "rb"),
            model="whisper-1",
        )
        
        return transcribed_text.text
        


