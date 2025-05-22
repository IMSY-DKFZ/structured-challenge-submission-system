from reportlab.platypus import ListFlowable, Paragraph


def add_challenge_to_document(story, challenge, styles):
    # CHALLENGE NAME
    story.append(
        Paragraph(
            challenge.challenge_name + ": Structured description of the challenge design",
            styles["Heading1"],
        )
    )
    story.append(Paragraph("<br/>", styles["Heading1"]))

    if challenge.subheading:
        story.append(
            Paragraph(
                challenge.subheading,
                styles["Definition"],
            )
        )

    # CHALLENGE ORGANIZATION
    story.append(Paragraph("CHALLENGE ORGANIZATION", styles["Heading2"]))

    # Title
    story.append(Paragraph("Title", styles["Heading3"]))
    story.append(
        Paragraph(
            "Use the title to convey the essential information on the challenge mission.",
            styles["Definition"],
        )
    )
    story.append(Paragraph(challenge.challenge_name, styles["Normal"]))

    # Challenge acronym
    story.append(Paragraph("Challenge acronym", styles["Heading3"]))
    story.append(
        Paragraph(
            "Preferable, provide a short acronym of the challenge (if any).",
            styles["Definition"],
        )
    )
    story.append(Paragraph(str(challenge.challenge_acronym or "N/A"), styles["Normal"]))

    # Challenge abstract
    story.append(Paragraph("Challenge abstract", styles["Heading3"]))
    story.append(
        Paragraph(
            "Provide a summary of the challenge purpose. This should include a general introduction in the topic from both a biomedical as well as from a technical point of view and clearly state the envisioned technical and/or biomedical impact of the challenge.",
            styles["Definition"],
        )
    )
    story.append(Paragraph(challenge.challenge_abstract or "N/A", styles["Normal"]))

    # Challenge keywords
    story.append(Paragraph("Challenge keywords", styles["Heading3"]))
    story.append(
        Paragraph(
            "List the primary keywords that characterize the challenge.",
            styles["Definition"],
        )
    )
    # keywords = ", ".join(challenge.challenge_keywords or "N/A")
    story.append(Paragraph(challenge.challenge_keywords or "N/A", styles["Normal"]))

    # Challenge year
    story.append(Paragraph("Year", styles["Heading3"]))
    story.append(
        Paragraph(
            str(challenge.challenge_year or "..."),
            styles["Normal"],
        )
    )

    # Challenge novelty
    story.append(Paragraph("Novelty of the challenge", styles["Heading3"]))
    story.append(
        Paragraph(
            "Briefly describe the novelty of the challenge.",
            styles["Definition"],
        )
    )
    story.append(Paragraph(challenge.challenge_novelty or "N/A", styles["Normal"]))

    # Challenge novelty
    story.append(Paragraph("Task description and application scenarios", styles["Heading3"]))
    story.append(
        Paragraph(
            "Briefly describe the application scenarios for the tasks in the challenge.",
            styles["Definition"],
        )
    )
    story.append(Paragraph(challenge.challenge_application_scenarios or "N/A", styles["Normal"]))

    # Special fields for lighthouse challenges
    if challenge.challenge_is_lighthouse_challenge and challenge.challenge_lighthouse_general_terms_agreed:
        story.append(Paragraph("Lighthouse challenge agreement", styles["Heading3"]))

        story.append(
            Paragraph(
                "The organizers agree to all of the following points:",
                styles["Definition"],
            )
        )

        story.append(
            ListFlowable(
                [
                    Paragraph(
                        "The full labeling protocol will be sent to the challenge chairs in addition to the full proposal document.",
                        styles["Definition"],
                    ),
                    Paragraph(
                        "A set of a few representative data samples including annotations will be sent to the challenge chairs in addition to the full proposal document.",
                        styles["Definition"],
                    ),
                    Paragraph(
                        "The challenge will be open for at least 4 months.",
                        styles["Definition"],
                    ),
                    Paragraph(
                        "For the dataset review, the challenge chairs will get access to the data at least 3 months before challenge opening.",
                        styles["Definition"],
                    ),
                ],
                bulletType="bullet",
                bulletFontName="OpenSans-Light",
                bulletFontSize=10,
                bulletDedent=6,
            )
        )
        story.append(
            Paragraph(
                "Challenge organizers have read and agree to all of the above terms and conditions.",
                styles["Normal"],
            )
        )

        story.append(Paragraph("Lighthouse challenge information", styles["Heading3"]))
        story.append(
            Paragraph(
                "In two sentences or less, what sets your challenge apart from ordinary MICCAI challenges. In other words: What makes your challenge a lighthouse challenge?",
                styles["Definition"],
            )
        )
        story.append(
            Paragraph(
                str(challenge.challenge_lighthouse_what_is_different or "N/A"),
                styles["Normal"],
            )
        )

        story.append(Paragraph("Previous challenge(s)", styles["Heading3"]))
        story.append(
            Paragraph(
                "What is the closest challenge to your proposed lighthouse challenge? Are there previous versions of it? Specifically, if you applied for a 2024 challenge, what is the delta between the two iterations? (e.g., number of centers for new data, number of newly added data – This is not to be confused with details about the total data set)",
                styles["Definition"],
            )
        )
        story.append(
            Paragraph(
                str(challenge.challenge_lighthouse_closest_challenge or "N/A"),
                styles["Normal"],
            )
        )

        story.append(Paragraph("Test set status", styles["Heading3"]))
        story.append(
            Paragraph(
                "Was the test set (or parts of it) already used in previous challenges and/or previously made publicly available?",
                styles["Definition"],
            )
        )
        story.append(
            Paragraph(
                str(challenge.challenge_lighthouse_test_set_already_used or "N/A"),
                styles["Normal"],
            )
        )

        story.append(
            Paragraph(
                "What major scientific advances or insights are expected from the challenge?",
                styles["Heading3"],
            )
        )
        story.append(
            Paragraph(
                "Please describe the major scientific advances ore insights you expect to be gained from the challenge. Please include references to the state of the art in your description and list open research questions to which the challenge seeks answers or solutions.",
                styles["Definition"],
            )
        )
        story.append(
            Paragraph(
                str(challenge.challenge_lighthouse_major_scientific_advances or "N/A"),
                styles["Normal"],
            )
        )

        story.append(Paragraph("Clinical body affiliation", styles["Heading3"]))
        story.append(
            Paragraph(
                "Please describe your proposed challenge’s affiliation with a clinical body, if any. How do you plan to engage the clinical community that your challenge is set to impact?",
                styles["Definition"],
            )
        )
        story.append(
            Paragraph(
                str(challenge.challenge_lighthouse_clinical_affiliation or "N/A"),
                styles["Normal"],
            )
        )

        story.append(Paragraph("Deadline for data acquisition and annotation", styles["Heading3"]))
        story.append(
            Paragraph(
                "What’s the deadline for data acquisition and annotation?",
                styles["Definition"],
            )
        )
        story.append(
            Paragraph(
                str(challenge.challenge_lighthouse_deadline_for_data or "N/A"),
                styles["Normal"],
            )
        )

        story.append(Paragraph("How much prize money has been secured?", styles["Heading3"]))
        story.append(
            Paragraph(
                "Please state how much prize money has already been secured for the challenge.",
                styles["Definition"],
            )
        )
        story.append(
            Paragraph(
                str(challenge.challenge_lighthouse_prize_money or "N/A"),
                styles["Normal"],
            )
        )

        story.append(Paragraph("Computing requirements per participant", styles["Heading3"]))
        story.append(
            Paragraph(
                "Roughly estimate how much computing power would be required per challenge participant?",
                styles["Definition"],
            )
        )
        story.append(
            Paragraph(
                str(challenge.challenge_lighthouse_compute_per_participant or "N/A"),
                styles["Normal"],
            )
        )

    # FURTHER INFOS
    story.append(Paragraph("FURTHER INFORMATION FOR CONFERENCE ORGANIZERS", styles["Heading2"]))

    # Workshop
    story.append(Paragraph("Workshop", styles["Heading3"]))
    story.append(
        Paragraph(
            "If the challenge is part of a workshop, please indicate the workshop.",
            styles["Definition"],
        )
    )
    story.append(Paragraph(str(challenge.challenge_workshop or "N/A"), styles["Normal"]))

    # Duration
    story.append(Paragraph("Duration", styles["Heading3"]))
    story.append(
        Paragraph(
            "How long does the challenge take?",
            styles["Definition"],
        )
    )
    story.append(Paragraph(str(challenge.challenge_duration or "N/A"), styles["Normal"]))

    # Longer duration explanation
    story.append(
        Paragraph(
            "In case you selected half or full day, please explain why you need a long slot for your challenge.",
            styles["Definition"],
        )
    )
    story.append(Paragraph(str(challenge.challenge_duration_explanation or "N/A"), styles["Normal"]))

    # Expected number of participants
    story.append(Paragraph("Expected number of participants", styles["Heading3"]))
    story.append(
        Paragraph(
            "Please explain the basis of your estimate (e.g. numbers from previous challenges) and/or provide a list of potential participants and indicate if they have already confirmed their willingness to contribute.",
            styles["Definition"],
        )
    )
    story.append(
        Paragraph(
            str(challenge.challenge_expected_number_of_participants or "N/A"),
            styles["Normal"],
        )
    )

    # Publication and future plans
    story.append(Paragraph("Publication and future plans", styles["Heading3"]))
    story.append(
        Paragraph(
            "Please indicate if you plan to coordinate a publication of the challenge results.",
            styles["Definition"],
        )
    )
    story.append(Paragraph(str(challenge.challenge_publication_and_future or "N/A"), styles["Normal"]))

    # Space and hardware requirements
    story.append(Paragraph("Space and hardware requirements", styles["Heading3"]))
    story.append(
        Paragraph(
            "Organizers of on-site challenges must provide a fair computing environment for all participants. For instance, algorithms should run on the same computing platform provided to all.",
            styles["Definition"],
        )
    )
    story.append(
        Paragraph(
            str(challenge.challenge_space_and_hardware_requirements or "N/A"),
            styles["Normal"],
        )
    )

    return story


def add_challenge_ending_to_document(story, challenge, styles):
    # ADDITIONAL POINTS
    story.append(Paragraph("ADDITIONAL POINTS", styles["Heading2"]))

    # References
    story.append(Paragraph("References", styles["Heading3"]))
    story.append(
        Paragraph(
            "Please include any reference important for the challenge design, for example publications on the data, the annotation process or the chosen metrics as well as DOIs referring to data or code.",
            styles["Definition"],
        )
    )
    story.append(Paragraph(challenge.challenge_references or "N/A", styles["Normal"]))

    # Further comments
    story.append(Paragraph("Further comments", styles["Heading3"]))
    story.append(
        Paragraph(
            "Further comments from the organizers.",
            styles["Definition"],
        )
    )
    story.append(Paragraph(challenge.challenge_further_comments or "N/A", styles["Normal"]))

    return story
