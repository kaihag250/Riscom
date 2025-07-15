from typing import Optional
from pydantic import BaseModel, Field

class Risk(BaseModel):
    risk_com: int = Field(
        description="Binary variable (1 if the text contains risk communication, 0 otherwise)."
    )
    one_case: int = Field(
        description="Binary variable (1 if the text contains only one case of risk and no alternative cases, 0 otherwise)."
    )
    absolute_risk_base: Optional[float] = Field(
        default=None,
        description="The absolute risk (%) before any intervention or treatment."
    )
    absolute_risk_new: Optional[float] = Field(
        default=None,
        description="The absolute risk (%) after intervention or treatment."
    )
    # Absolute number
    absolute_number_base: Optional[int] = Field(
        default=None,
        description="The absolute number of cases in the base case."
    )
    absolute_number_new: Optional[int] = Field(
        default=None,
        description="The absolute number of cases in the new case."
    )
    # Absolute risk difference
    absolute_risk_difference: Optional[float] = Field(
        default=None,
        description="The difference in absolute risk (%) between base and new."
    )
    # Relative risk
    relative_risk: Optional[float] = Field(
        default=None,
        description="The relative risk (%) comparing new and baseline absolute risk."
    )
    # Absolute number difference
    absolute_number_difference: Optional[int] = Field(
        default=None,
        description="The difference in absolute number of cases between base and new."
    )
    # Verbal risk descriptors
    verbal_risk_descriptor_base: Optional[str] = Field(
        default=None,
        description="The verbal risk descriptor in the base case."
    )
    verbal_risk_descriptor_new: Optional[str] = Field(
        default=None,
        description="The verbal risk descriptor in the new case."
    )
    verbal_risk_descriptor_change: Optional[str] = Field(
        default=None,
        description="The change in verbal risk descriptor from base to new case."
    )
    # Reference class size
    reference_class_size_base: Optional[int] = Field(
        default=None,
        description="The reference class size (base case)."
    )
    reference_class_size_new: Optional[int] = Field(
        default=None,
        description="The reference class size (new case)."
    )
    # Reference class description
    reference_class_description_base: Optional[str] = Field(
        default=None,
        description="Description of the reference class (base case)."
    )
    reference_class_description_new: Optional[str] = Field(
        default=None,
        description="Description of the reference class (new case)."
    )
    # Source
    source_base: Optional[str] = Field(
        default=None,
        description="Source information (base case)."
    )
    source_new: Optional[str] = Field(
        default=None,
        description="Source information (new case)."
    )
    # Topic and unit
    topic_and_unit: Optional[str] = Field(
        default=None,
        description="Topic and unit of the risk communication."
    )



    # Source Checker 

