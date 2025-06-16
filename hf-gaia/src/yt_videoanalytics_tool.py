from typing import Type
from langchain.tools import BaseTool
from pydantic import Field, BaseModel
import yt_dlp
import cv2
import base64

class YTKeyFrameExtractToolInput(BaseModel):
    video_id: str = Field(..., description="The ID of the YouTube video to get the analysis for, e.g. `1htKBjuUWec`")
    query:str = Field(..., description="The query to analyze the video with, e.g. `What is the main topic of this video?`")

class YTKeyFrameExtractTool(BaseTool):

    name: str = "YTKeyFrameExtract_tool"
    description: str = "A tool for extracting key frames from a YouTube video. Returns text with a list of base64 encoded frames."
    args_schema: Type[BaseModel] = YTKeyFrameExtractToolInput


    def _run(self, video_id: str, query:str) -> str:        
        url = f'https://www.youtube.com/watch?v={video_id}'

        result = f'Base64 key frames extracted from the video: {url} \n\n'

        ydl_opts = {
            'outtmpl': f'./data/{video_id}.%(ext)s'
        }

        # download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:            
            ydl.download([url])
        
        # extract key frames        
        vc = cv2.VideoCapture(f'./data/{video_id}.mp4')
        fps = vc.get(cv2.CAP_PROP_FPS)

        try:
            i = 0
            while (True):
                ret, frame = vc.read()
                if not ret:
                    break

                i += 1
                if i % (fps * 5) == 0: # key frame every 5 seconds
                    _, buffer = cv2.imencode('.png', frame)
                    result += f'''Key frame: {i}
{base64.b64encode(buffer).decode('utf-8')}\n\n'''

        finally:
            vc.release()

        return result


#tool = YTKeyFrameExtractTool()
#result = tool._run('L1vXCYZAYYM', 'What is the main topic of this video?')
#print(result)

