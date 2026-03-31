from typing import Any, Optional
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


# ---------------------------------------------------------------------------
# M2 – Template upload / mapping / profile-from-template
# ---------------------------------------------------------------------------

class TemplateUploadResponse(BaseModel):
    template_id: str
    original_filename: str
    stored_path: str
    metadata_path: str
    paragraph_count: int
    table_count: int


class BlockCandidate(BaseModel):
    block_index: int = Field(description="Index of the paragraph/block in the document")
    text_snippet: str = Field(description="First ~120 characters of the block text")
    style_hint: str = Field(description="Brief style summary, e.g. 'bold 14pt Times New Roman'")
    confidence: float = Field(ge=0.0, le=1.0, description="Heuristic confidence 0–1")
    field_name: str = Field(
        description="Suggested field: experiment_number | aim | source_code | output | ignore"
    )


class SuggestMappingResponse(BaseModel):
    template_id: str
    suggestions: list[BlockCandidate]


class MappingSelection(BaseModel):
    block_index: int = Field(description="Block index chosen by the user for this field")
    field_name: str = Field(
        description="Field name: experiment_number | aim | source_code | output"
    )


class StyleOverride(BaseModel):
    font_family: Optional[str] = None
    font_size: Optional[int] = Field(default=None, ge=6, le=72)
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    underline: Optional[bool] = None


class ProfileFromTemplateRequest(BaseModel):
    template_id: str = Field(description="ID of the previously uploaded template")
    profile_id: str = Field(description="New profile identifier, e.g. 'my-lab-profile'")
    profile_name: str = Field(description="Human-readable name for the profile")
    confirmed_mappings: list[MappingSelection] = Field(
        description="User-confirmed list of field → block_index assignments"
    )
    style_overrides: Optional[dict[str, StyleOverride]] = Field(
        default=None,
        description=(
            "Optional per-field style overrides keyed by field name "
            "(aim, source_code, output)"
        ),
    )

