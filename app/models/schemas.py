from typing import Optional
from pydantic import BaseModel, Field


class TextStyle(BaseModel):
    font_family: str = Field(default="Times New Roman", description="Font family name")
    font_size: int = Field(default=12, ge=6, le=72, description="Font size in points")
    bold: bool = Field(default=False)
    italic: bool = Field(default=False)
    underline: bool = Field(default=False)


class SectionConfig(BaseModel):
    label: str = Field(description="Label text shown in the document for this section")
    label_style: TextStyle = Field(default_factory=TextStyle)
    body_style: TextStyle = Field(default_factory=TextStyle)


class PageLayout(BaseModel):
    margin_top_cm: float = Field(default=2.54, description="Top margin in centimetres")
    margin_bottom_cm: float = Field(default=2.54)
    margin_left_cm: float = Field(default=2.54)
    margin_right_cm: float = Field(default=2.54)


class TemplateProfileCreate(BaseModel):
    id: str = Field(description="Unique profile identifier, e.g. 'java-default'")
    name: str = Field(description="Human-readable profile name")
    heading_style: TextStyle = Field(
        default_factory=lambda: TextStyle(font_size=16, bold=True)
    )
    experiment_number_label: str = Field(default="Program")
    aim_section: SectionConfig = Field(
        default_factory=lambda: SectionConfig(
            label="Aim:- ",
            label_style=TextStyle(font_size=14, bold=True, underline=True),
            body_style=TextStyle(font_size=12),
        )
    )
    source_code_section: SectionConfig = Field(
        default_factory=lambda: SectionConfig(
            label="SOURCE CODE:-",
            label_style=TextStyle(font_size=14, bold=True, underline=True),
            body_style=TextStyle(font_family="Courier New", font_size=11),
        )
    )
    output_section: SectionConfig = Field(
        default_factory=lambda: SectionConfig(
            label="OUTPUT:-",
            label_style=TextStyle(font_size=14, bold=True, underline=True),
            body_style=TextStyle(font_size=12, italic=True),
        )
    )
    output_placeholder: str = Field(default="[ PASTE SCREENSHOT HERE ]")
    page_layout: PageLayout = Field(default_factory=PageLayout)


class TemplateProfile(TemplateProfileCreate):
    pass


class GenerateRequest(BaseModel):
    profile_id: str = Field(description="ID of the template profile to use")
    experiment_number: Optional[str] = Field(
        default=None, description="Experiment or program number/title"
    )
    aim: str = Field(description="Aim / objective of the experiment")
    source_code: str = Field(description="Source code text")
    output_text: Optional[str] = Field(
        default=None,
        description="Optional output text; leave blank to use the profile placeholder",
    )


class GenerateResponse(BaseModel):
    filename: str
    file_path: str
    download_url: str
    profile_id: str
    experiment_number: Optional[str]
    aim: str
