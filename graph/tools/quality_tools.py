from pathlib import Path
import cv2 # OpenCV for image processing (lapalacian operator)
import textstat # for readability scores
from llm_config import get_llm
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

def analyze_images(image_paths: list) -> str:
    """
    Analyze the sharpness of all images in a folder and return a report.
    """
    treshold = 100 # if resized to 256x256 -> use 1000
    values = []
    results = ""
    count_sharp = 0
    count_blurry = 0

    # Analyze all PNG images in the folder
    for path in image_paths:
        img = Path(path)

        sharpness = measure_img_sharpness(img)
        values.append({"image": img.name, "sharpness": sharpness})

        if sharpness > treshold:
            results += f"{img.name} is sharp\n"
            count_sharp += 1
        else:
            results += f"{img.name} is blurry\n"
            count_blurry += 1
    
    results += f"\nSummary: {count_sharp} sharp images and {count_blurry} blurry images.\n"
    return results

def measure_img_sharpness(image_path: Path) -> float:
    """
    Measure the sharpness of the images using the variance of the Laplacian.
    Higher values indicate a sharper image.
    """
    # 1. load image
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not load image: {image_path}")
    #img = cv2.resize(img, (256, 256))  # unify size
    
    # 2. convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. apply Laplace operator
    laplacian = cv2.Laplacian(gray_img, cv2.CV_64F)

    # 4. calculate variance of Laplace values → sharpness value
    sharpness = laplacian.var()

    return sharpness


def compute_readability_scores(md_path: Path) -> dict:
    """
    Computes various readability scores for a given text.
    """
    results = {}

    # 1. read markdown text
    with open(md_path, "r") as file:
        md_text = file.read()

    # 2. calculate different readability scores
    results["flesch_reading_ease"] = textstat.flesch_reading_ease(md_text)
    results["flesch_kincaid_grade"] = textstat.flesch_kincaid_grade(md_text)
    results["gunning_fog"] = textstat.gunning_fog(md_text)
    results["smog_index"] = textstat.smog_index(md_text)
    results["automated_readability_index"] = textstat.automated_readability_index(md_text)
    results["coleman_liau_index"] = textstat.coleman_liau_index(md_text)
    results["linsear_write_formula"] = textstat.linsear_write_formula(md_text)
    results["dale_chall_readability_score"] = textstat.dale_chall_readability_score(md_text)
    results["mcalpine_eflaw"] = textstat.mcalpine_eflaw(md_text)

    return results

class QualityReport(BaseModel):
    """Report of Quality Agent"""
    report: str = Field(description="Concise quality report of max 200 words")
    score: int = Field(ge=0, le=10, description="Quality score 0-10")


def generate_quality_report(image_quality: str, readability_scores: dict) -> dict:
    
    # Build a prompt with context
    system_prompt = """
        You are an rigorous scientific reviewer for a scientific journal.

        Your task is to assess the quality of a scientific manuscript based on the inputs: readability scores and image quality summary.
        Use the input data to assess: how appropriate the manuscript’s readability is for an academic paper, how good the overall sharpness of the images is and how these factors reflect the manuscript’s overall quality.
        You must provide:
        1) A concise quality report (maximum 200 words)  
        2) A quality score from 0 to 10, where:
            - 0 = poor image quality; readability scores are low and therefore not appropriate for a scientific paper  
            - 10 = excellent image quality; readability scores are high and therefore appropriate for a scientific paper

        Do not make assumptions beyond the supplied data.
        Return information strictly according to the fields defined in the output schema.
        Do not produce explanations outside the schema fields.
        Always answer in English!
        """
    user_prompt = """
        Here are the analysis results:

        Text readability scores:
        {readability_scores}

        Image quality:
        {image_quality}

        Based on these inputs, generate your quality assessment.
        """

    # Invoke LLM
    structured_llm = get_llm().with_structured_output(QualityReport, include_raw=True)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", user_prompt)
    ])
    chain = prompt | structured_llm
    response = chain.invoke({
        "readability_scores": readability_scores,
        "image_quality": image_quality
    })
    # process raw data
    result = response["parsed"].model_dump()
    input_tokens = response["raw"].usage_metadata["input_tokens"]
    output_tokens = response["raw"].usage_metadata["output_tokens"]
    return result, input_tokens, output_tokens