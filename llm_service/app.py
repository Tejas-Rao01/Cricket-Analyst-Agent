from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 1. Configuration
# Load the model and tokenizer at the start of the application
model_id = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
# Ensure the model is loaded once with the specified configurations
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    load_in_8bit=True,
    llm_int8_enable_fp32_cpu_offload=True
)

# 2. FastAPI Application
app = FastAPI()

# Pydantic model to define the request body structure
class PromptRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 50  # Optional parameter with a default value

# 3. API Endpoint
@app.post("/generate")
async def generate_text(request: PromptRequest):
    """
    Generates text based on a user-provided prompt using the Phi-2 model.
    """
    # 3.1. Prepare input
    inputs = tokenizer(request.prompt, return_tensors="pt").to(model.device)

    # 3.2. Generate output
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=request.max_new_tokens,
            pad_token_id=tokenizer.eos_token_id
        )

    # 3.3. Decode and return the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"generated_text": generated_text}

# 4. How to run the server:
#    uvicorn server:app --host 0.0.0.0 --port 8000