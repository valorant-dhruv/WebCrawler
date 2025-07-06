from pydantic import BaseModel, Field

class WhoIsHiring(BaseModel):
    company_name_and_location: str = Field(..., description="Name of the Company along with posting details who is hiring")
    technology_stack: str = Field(...,description="Tecnology stack in array that the company requires")
    job_description: str = Field(..., description="Description of the job in detailed manner")
    application_details: str = Field(..., description="Details about how to apply") 

class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(
        ..., description="Fee for output token for the OpenAI model."
    )