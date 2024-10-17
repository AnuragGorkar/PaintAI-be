from fastapi import APIRouter
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image

router = APIRouter()

def convert_to_markdown(expression: str, result: str) -> str:
    expression = expression.replace(" ", "\\,")
    result = str(result).replace(" ", "\\,")
    expression = expression.replace("\n", "\\\\")
    return f"$${expression}$$", f"$${result}$$"

@router.post('')
async def run(data: ImageData):
    image_data = base64.b64decode(data.image.split(",")[1])
    image_bytes = BytesIO(image_data)
    image = Image.open(image_bytes)

    responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
    result_data = []

    for response in responses:
        markdown_expr, markdown_result = convert_to_markdown(response['expr'], response['result'])
        result_data.append({
            "expr": markdown_expr,
            "result": markdown_result,
            "assign": response.get('assign', False)
        })

    return {
        "message": "Image processed",
        "data": result_data,
        "status": "success"
    }
