# BMC_API/src/infrastructure/external_services/challenge_to_pdf/challenge_to_pdf_converter.py
import copy
import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate

from BMC_API.src.application.dto.challenge_dto import ChallengeModelOutputPdfDTO
from BMC_API.src.application.dto.task_dto import TaskModelBaseOutputDTO
from BMC_API.src.core.config.settings import settings
from BMC_API.src.infrastructure.external_services.challenge_to_pdf.dependencies import (
    NumberedCanvas,
    add_horizontal_lines,
    register_fonts,
    set_document_styles,
)
from BMC_API.src.infrastructure.external_services.challenge_to_pdf.export_challenge import (
    add_challenge_ending_to_document,
    add_challenge_to_document,
)
from BMC_API.src.infrastructure.external_services.challenge_to_pdf.export_task import (
    add_tasks_to_document,
)


class MyDocTemplate(SimpleDocTemplate):
    """Override the BaseDocTemplate class to do custom handle_XXX actions"""

    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)

    def afterPage(self):
        """Called after each page has been processed"""

        # saveState keeps a snapshot of the canvas state, so you don't
        # mess up any rendering that platypus will do later.
        self.canv.saveState()

        # Reset the origin to (0, 0), remember, we can restore the
        # state of the canvas later, so platypus should be unaffected.
        self.canv._x = 0
        self.canv._y = 0

        # style = getSampleStyleSheet()

        # p = Paragraph("This is drawn after the page!", style["Normal"])

        # Wraps and draws the paragraph onto the canvas
        # You can change the last 2 parameters (canv, x, y)
        # p.wrapOn(self.canv, 2 * inch, 2 * inch)
        # p.drawOn(self.canv, 1 * inch, 3 * inch)

        # Now we restore the canvas back to the way it was.
        self.canv.restoreState()


def parse_db_model(model, PydanticModel, exclude_fields: list[str]):
    model_dict = model.__dict__
    if exclude_fields:
        for f in exclude_fields:
            if f in model_dict.keys():
                model_dict.pop(f)

    # Iterate through the items and modify string values that are not empty
    for key, value in model_dict.items():
        if value and isinstance(value, list) and isinstance(value[0], str):
            value = ", ".join(value)
            model_dict[key] = value

        if value and isinstance(value, str) and value.strip():  # Check if it's a non-empty string
            # Modify the string value

            # This must be first to eliminate broken HTML tag error
            model_dict[key] = model_dict[key].replace("<", "&lt;")
            model_dict[key] = model_dict[key].replace(">", "&gt;")
            # For colorings

            model_dict[key] = model_dict[key].replace("###FONT_TAG_BLUE_START###,", '<span backcolor="#97d2f7">')
            model_dict[key] = model_dict[key].replace("###FONT_TAG_BLUE_START###", '<span backcolor="#97d2f7">')
            model_dict[key] = model_dict[key].replace("###FONT_TAG_RED_START###,", '<span backcolor="#ff8c8c">')
            model_dict[key] = model_dict[key].replace("###FONT_TAG_RED_START###", '<span backcolor="#ff8c8c">')
            model_dict[key] = model_dict[key].replace("###FONT_TAG_END###", "</span>")
            # This must be last
            model_dict[key] = model_dict[key].replace("\n", "<br />")
    model_pydantic = PydanticModel(**model_dict)
    return model_pydantic


def convert_challenge_to_pdf(challenge, tasks):
    # Set up the PDF document
    register_fonts()

    # Arrange submissions folder
    submissions_folder = str(settings.submissions_folder)
    if not os.path.exists(submissions_folder):
        os.mkdir(submissions_folder)

    challenge_name = copy.deepcopy(str(challenge.challenge_name))
    challenge_name = challenge_name.replace("###FONT_TAG_BLUE_START###,", "")
    challenge_name = challenge_name.replace("###FONT_TAG_BLUE_START###", "")
    challenge_name = challenge_name.replace("###FONT_TAG_RED_START###,", "")
    challenge_name = challenge_name.replace("###FONT_TAG_RED_START###", "")
    challenge_name = challenge_name.replace("###FONT_TAG_END###", "")
    challenge_name = " ".join(challenge_name.split()[:8])
    file_name = f"{challenge.id}-{challenge_name.replace(' ', '_')}_{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.pdf"

    # Define a list of characters not allowed in file names across different operating systems
    forbidden_chars = ["<", ">", ":", '"', "/", "\\", "|", "?", "*", ","]
    file_name = "".join(["" if char in forbidden_chars else char for char in file_name])

    pdf_file_path = os.path.join(settings.submissions_folder, file_name)

    left_margin = 30
    right_margin = 25
    top_margin = 35
    bottom_margin = 40

    # Set up the document
    doc = MyDocTemplate(
        pdf_file_path,
        pagesize=A4,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
        title=challenge_name,
        author='Challenge submission system v2',
        subject='',
        creator='',
        producer='',
    
    )
    story = []

    styles = set_document_styles()

    # PARSE MODELS
    exclude_fields = [
        "histories",
        "challenge_conference",
        "challenge_owner",
        "challenge_tasks",
        "_sa_instance_state",
        "challenge_locked",
        "challenge_reviewer_status",
        "challenge_super_reviewer_status",
        "task_challenge",
        "task_challenge_id",
        "task_owner",
        "task_owner_id",
        "task_locked",
    ]
    challenge_pydantic = parse_db_model(challenge, ChallengeModelOutputPdfDTO, exclude_fields=exclude_fields)

    if not isinstance(tasks, list):
        tasks_pydantic = parse_db_model(tasks, TaskModelBaseOutputDTO, exclude_fields=exclude_fields)
    else:
        tasks_pydantic = []
        for idx, task in enumerate(tasks):
            tasks_pydantic.append(parse_db_model(task, TaskModelBaseOutputDTO, exclude_fields=exclude_fields))

    # ADD CHALLENGE TO THE DOCUMENT
    story = add_challenge_to_document(story, challenge_pydantic, styles)

    # ADD TASK(s) TO THE DOCUMENT
    story = add_tasks_to_document(story, tasks_pydantic, challenge_pydantic, styles)

    # ADD CHALLENGE ENDING TO THE DOCUMENT
    story = add_challenge_ending_to_document(story, challenge_pydantic, styles)

    # BUILD THE PDF DOCUMENT

    if len(challenge_name) < 115:
        header_text = challenge_name
    else:
        header_text = challenge_name[:112] + "..."

    doc.build(
        story,
        onFirstPage=add_horizontal_lines,
        onLaterPages=add_horizontal_lines,
        canvasmaker=lambda *args, **kwargs: NumberedCanvas(header_text=header_text, *args, **kwargs),
    )

    return file_name
