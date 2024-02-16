from pydantic import BaseModel, Field, AnyUrl
from typing import List

class DatasetConfig(BaseModel):
    url: AnyUrl = Field('', description="The URL for the dataset")
    variables: List[str] = Field([], description="List of variables in the dataset")
    decoded_time: bool = Field(True, description="Flag indicating if time is decoded")
    time_range: List[str] = Field([], description="Time range for the dataset")
    is_resampled: bool = Field(False, description="Flag indicating if the dataset is resampled")
    resampling_frequency: str = Field('raw', description="Frequency of resampling")
    output_format: str = Field('nc', description="Output format for the dataset")
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "url": "https://thredds.met.no/thredds/dodsC/alertness/YOPP_supersite/obs/utqiagvik/utqiagvik_obs_timeSeriesProfileSonde_20180201_20180331.nc",
                "variables": ["ta", "hur", "wdir_refmt"],
                "decoded_time": True,
                "time_range": [" ", " "],
                "is_resampled": False,
                "resampling_frequency": "raw",
                "output_format": "nc"
            }
        }
