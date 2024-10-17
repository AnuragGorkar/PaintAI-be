from fastapi import APIRouter
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image

router = APIRouter()

def convert_to_markdown(expression: str, result: str) -> str:
    """
    Convert expression and result to Markdown format for LaTeX display.
    Replaces spaces with LaTeX small space and newlines with LaTeX line breaks.
    """
    # Replace spaces with LaTeX small space
    expression = expression.replace(" ", "\\,")
    result = str(result).replace(" ", "\\,")  # Convert result to string to replace spaces
    
    # Replace newlines with LaTeX line breaks
    expression = expression.replace("\n", "\\\\")
    
    return f"$${expression}$$", f"$${result}$$"

@router.post('')
async def run(data: ImageData):
    image_data = base64.b64decode(data.image.split(",")[1])  # Assumes data:image/png;base64,<data>
    image_bytes = BytesIO(image_data)
    image = Image.open(image_bytes)

    responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
    result_data = []

    for response in responses:
        # Convert expression and result to markdown format
        markdown_expr, markdown_result = convert_to_markdown(response['expr'], response['result'])
        
        # Structure the result data
        result_data.append({
            "expr": markdown_expr,
            "result": markdown_result,
            "assign": response.get('assign', False)  # Assuming assign is part of the original response
        })

    print('response in route: ', result_data)

    return {
        "message": "Image processed",
        "data": result_data,
        "status": "success"
    }
