from reportlab.platypus import ListFlowable, PageBreak, Paragraph


def add_task_to_document(story, task, challenge, idx, styles):
    story.append(PageBreak())
    # TASK NAME
    story.append(
        Paragraph(
            "TASK " + str(idx) + ": " + task.task_name or "N/A",
            styles["Title"],
        )
    )

    # SUMMARY
    story.append(Paragraph("SUMMARY", styles["Heading2"]))

    # Abstract
    story.append(Paragraph("Abstract", styles["Heading3"]))
    story.append(
        Paragraph(
            "Provide a summary of the challenge purpose. This should include a general introduction in the topic from both a biomedical as well as from a technical point of view and clearly state the envisioned technical and/or biomedical impact of the challenge.",
            styles["Definition"],
        )
    )
    story.append(
        Paragraph(
            task.task_abstract or challenge.challenge_abstract or "N/A",
            styles["Normal"],
        )
    )

    # Keywords
    story.append(Paragraph("Keywords", styles["Heading3"]))
    story.append(
        Paragraph(
            "List the primary keywords that characterize the task.",
            styles["Definition"],
        )
    )
    # keywords = ", ".join(task.task_keywords or "N/A")
    story.append(Paragraph(task.task_keywords or "N/A", styles["Normal"]))

    # ORGANIZATION
    story.append(Paragraph("ORGANIZATION", styles["Heading2"]))

    # Organizers
    story.append(Paragraph("Organizers", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) Provide information on the organizing team (names and affiliations).",
            styles["Definition"],
        )
    )
    story.append(Paragraph(task.task_organizing_team or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) Provide information on the primary contact person.",
            styles["Definition"],
        )
    )
    story.append(Paragraph(task.task_contact_person or "N/A", styles["Normal"]))

    # Life cycle type
    story.append(Paragraph("Life cycle type", styles["Heading3"]))

    story.append(
        Paragraph(
            "Define the intended submission cycle of the challenge. Include information on whether/how the challenge will be continued after the challenge has taken place.Not every challenge closes after the submission deadline (one-time event). Sometimes it is possible to submit results after the deadline (open call) or the challenge is repeated with some modifications (repeated event).<br/><br/>Examples:",
            styles["Definition"],
        )
    )
    story.append(
        ListFlowable(
            [
                Paragraph(
                    "One-time event with fixed conference submission deadline",
                    styles["Definition"],
                ),
                Paragraph(
                    "Open call (challenge opens for new submissions after conference deadline)",
                    styles["Definition"],
                ),
                Paragraph(
                    "Repeated event with annual fixed conference submission deadline",
                    styles["Definition"],
                ),
            ],
            bulletType="bullet",
            bulletFontName="OpenSans-Light",
            bulletFontSize=10,
            bulletDedent=6,
        )
    )

    story.append(Paragraph(task.task_lifecycle or "N/A", styles["Normal"]))

    # Challenge venue and platform
    story.append(Paragraph("Challenge venue and platform", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) Report the event (e.g. conference) that is associated with the challenge (if any).",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_conference_name or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) Report the platform (e.g. grand-challenge.org) used to run the challenge.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_platform or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "c) Provide the URL for the challenge website (if any).",
            styles["Definition"],
        )
    )

    story.append(Paragraph(str(task.task_url or "N/A"), styles["Normal"]))

    # Participation policies
    story.append(Paragraph("Participation policies", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) Define the allowed user interaction of the algorithms assessed (e.g. only (semi-) automatic methods allowed).",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_interaction_level_policy or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) Define the policy on the usage of training data. The data used to train algorithms may, for example, be restricted to the data provided by the challenge or to publicly available data including (open) pre-trained nets.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_training_data_policy or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "c) Define the participation policy for members of the organizers' institutes. For example, members of the organizers' institutes may participate in the challenge but are not eligible for awards.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_organizer_participation_policy or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "d) Define the award policy. In particular, provide details with respect to challenge prizes.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_award_policy or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "e) Define the policy for result announcement.<br/><br/>Examples:",
            styles["Definition"],
        )
    )

    story.append(
        ListFlowable(
            [
                Paragraph(
                    "Top 3 performing methods will be announced publicly.",
                    styles["Definition"],
                ),
                Paragraph(
                    "Participating teams can choose whether the performance results will be made public.",
                    styles["Definition"],
                ),
            ],
            bulletType="bullet",
            bulletFontName="OpenSans-Light",
            bulletFontSize=10,
            bulletDedent=6,
        )
    )

    story.append(Paragraph(task.task_results_announcement or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "f) Define the publication policy. In particular, provide details on ...",
            styles["Definition"],
        )
    )

    story.append(
        ListFlowable(
            [
                Paragraph(
                    "... who of the participating teams/the participating teams’ members qualifies as author",
                    styles["Definition"],
                ),
                Paragraph(
                    "... whether the participating teams may publish their own results separately, and (if so)",
                    styles["Definition"],
                ),
                Paragraph(
                    "... whether an embargo time is defined (so that challenge organizers can publish a challenge paper first).",
                    styles["Definition"],
                ),
            ],
            bulletType="bullet",
            bulletFontName="OpenSans-Light",
            bulletFontSize=10,
            bulletDedent=6,
        )
    )

    story.append(Paragraph(task.task_pulication_policy or "N/A", styles["Normal"]))

    # Submission method
    story.append(Paragraph("Submission method", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) Describe the method used for result submission. Preferably, provide a link to the submission instructions.<br/><br/>Examples:",
            styles["Definition"],
        )
    )

    story.append(
        ListFlowable(
            [
                Paragraph(
                    "Docker container on the Synapse platform. Link to submission instructions: &lt;URL&gt;",
                    styles["Definition"],
                ),
                Paragraph(
                    "Algorithm output was sent to organizers via e-mail. Submission instructions were sent by e-mail.",
                    styles["Definition"],
                ),
            ],
            bulletType="bullet",
            bulletFontName="OpenSans-Light",
            bulletFontSize=10,
            bulletDedent=6,
        )
    )

    story.append(Paragraph(task.task_result_submission_method or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) Provide information on the possibility for participating teams to evaluate their algorithms before submitting final results. For example, many challenges allow submission of multiple results, and only the last run is officially counted to compute challenge results.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_pre_evaluation or "N/A", styles["Normal"]))

    # Challenge schedule
    story.append(Paragraph("Challenge schedule", styles["Heading3"]))

    story.append(
        Paragraph(
            "Provide a timetable for the challenge. Preferably, this should include",
            styles["Definition"],
        )
    )

    story.append(
        ListFlowable(
            [
                Paragraph(
                    "the release date(s) of the training cases (if any)",
                    styles["Definition"],
                ),
                Paragraph(
                    "the registration date/period",
                    styles["Definition"],
                ),
                Paragraph(
                    "the release date(s) of the test cases and validation cases (if any)",
                    styles["Definition"],
                ),
                Paragraph(
                    "the submission date(s)",
                    styles["Definition"],
                ),
                Paragraph(
                    "associated workshop days (if any)",
                    styles["Definition"],
                ),
                Paragraph(
                    "the release date(s) of the results",
                    styles["Definition"],
                ),
            ],
            bulletType="bullet",
            bulletFontName="OpenSans-Light",
            bulletFontSize=10,
            bulletDedent=6,
        )
    )

    story.append(Paragraph(task.task_schedule or "N/A", styles["Normal"]))

    # Ethics approval
    story.append(Paragraph("Ethics approval", styles["Heading3"]))

    story.append(
        Paragraph(
            "Indicate whether ethics approval is necessary for the data. If yes, provide details on the ethics approval, preferably institutional review board, location, date and number of the ethics approval (if applicable). Add the URL or a reference to the document of the ethics approval (if available).",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_ethics_approval or "N/A", styles["Normal"]))

    # Data usage agreement
    story.append(Paragraph("Data usage agreement", styles["Heading3"]))

    story.append(
        Paragraph(
            "Clarify how the data can be used and distributed by the teams that participate in the challenge and by others during and after the challenge. This should include the explicit listing of the license applied.<br/><br/>Examples:",
            styles["Definition"],
        )
    )

    story.append(
        ListFlowable(
            [
                Paragraph(
                    "CC BY (Attribution)",
                    styles["Definition"],
                ),
                Paragraph(
                    "CC BY-SA (Attribution-ShareAlike)",
                    styles["Definition"],
                ),
                Paragraph(
                    "CC BY-ND (Attribution-NoDerivs)",
                    styles["Definition"],
                ),
                Paragraph(
                    "CC BY-NC (Attribution-NonCommercial)",
                    styles["Definition"],
                ),
                Paragraph(
                    "CC BY-NC-SA (Attribution-NonCommercial-ShareAlike)",
                    styles["Definition"],
                ),
                Paragraph(
                    "CC BY-NC-ND (Attribution-NonCommercial-NoDerivs)",
                    styles["Definition"],
                ),
            ],
            bulletType="bullet",
            bulletFontName="OpenSans-Light",
            bulletFontSize=10,
            bulletDedent=6,
        )
    )

    story.append(Paragraph(task.task_licence or "N/A", styles["Normal"]))

    # Code availability
    story.append(Paragraph("Code availability", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) Provide information on the accessibility of the organizers' evaluation software (e.g. code to produce rankings). Preferably, provide a link to the code and add information on the supported platforms.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_code_availability_organizers or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) In an analogous manner, provide information on the accessibility of the participating teams' code.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_code_availability_participants or "N/A", styles["Normal"]))

    # Conflicts of interest
    story.append(Paragraph("Conflicts of interest", styles["Heading3"]))

    story.append(
        Paragraph(
            "Provide information related to conflicts of interest. In particular provide information related to sponsoring/funding of the challenge. Also, state explicitly who had/will have access to the test case labels and when.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_conflict_of_interest or "N/A", styles["Normal"]))

    # MISSION OF THE CHALLENGE
    story.append(Paragraph("MISSION OF THE CHALLENGE", styles["Heading2"]))

    # Field(s) of application
    story.append(Paragraph("Field(s) of application", styles["Heading3"]))

    story.append(
        Paragraph(
            "State the main field(s) of application that the participating algorithms target.<br/><br/>Examples:",
            styles["Definition"],
        )
    )

    story.append(
        ListFlowable(
            [
                Paragraph(
                    "Diagnosis",
                    styles["Definition"],
                ),
                Paragraph(
                    "Education",
                    styles["Definition"],
                ),
                Paragraph(
                    "Intervention assistance",
                    styles["Definition"],
                ),
                Paragraph(
                    "Intervention follow-up",
                    styles["Definition"],
                ),
                Paragraph(
                    "Intervention planning",
                    styles["Definition"],
                ),
                Paragraph(
                    "Prognosis",
                    styles["Definition"],
                ),
                Paragraph(
                    "Research",
                    styles["Definition"],
                ),
                Paragraph(
                    "Screening",
                    styles["Definition"],
                ),
                Paragraph(
                    "Training",
                    styles["Definition"],
                ),
                Paragraph(
                    "Cross-phase",
                    styles["Definition"],
                ),
                Paragraph(
                    "",
                    styles["Definition"],
                ),
            ],
            bulletType="bullet",
            bulletFontName="OpenSans-Light",
            bulletFontSize=10,
            bulletDedent=6,
        )
    )

    story.append(Paragraph(task.task_field_of_application or "N/A", styles["Normal"]))

    # Task category(ies)
    story.append(Paragraph("Task category(ies)", styles["Heading3"]))

    story.append(
        Paragraph(
            "State the task category(ies)<br/><br/>Examples:",
            styles["Definition"],
        )
    )

    story.append(
        ListFlowable(
            [
                Paragraph(
                    "Classification",
                    styles["Definition"],
                ),
                Paragraph(
                    "Detection",
                    styles["Definition"],
                ),
                Paragraph(
                    "Localization",
                    styles["Definition"],
                ),
                Paragraph(
                    "Modeling",
                    styles["Definition"],
                ),
                Paragraph(
                    "Prediction",
                    styles["Definition"],
                ),
                Paragraph(
                    "Reconstruction",
                    styles["Definition"],
                ),
                Paragraph(
                    "Registration",
                    styles["Definition"],
                ),
                Paragraph(
                    "Retrieval",
                    styles["Definition"],
                ),
                Paragraph(
                    "Segmentation",
                    styles["Definition"],
                ),
                Paragraph(
                    "Tracking",
                    styles["Definition"],
                ),
            ],
            bulletType="bullet",
            bulletFontName="OpenSans-Light",
            bulletFontSize=10,
            bulletDedent=6,
        )
    )

    story.append(Paragraph(task.task_task_category or "N/A", styles["Normal"]))

    # Cohorts
    story.append(Paragraph("Cohorts", styles["Heading3"]))

    story.append(
        Paragraph(
            "We distinguish between the target cohort and the challenge cohort. For example, a challenge could be designed around the task of medical instrument tracking in robotic kidney surgery. While the challenge could be based on ex vivo data obtained from a laparoscopic training environment with porcine organs (challenge cohort), the final biomedical application (i.e. robotic kidney surgery) would be targeted on real patients with certain characteristics defined by inclusion criteria such as restrictions regarding sex or age (target cohort).",
            styles["Definition"],
        )
    )

    story.append(
        Paragraph(
            "a) Describe the target cohort, i.e. the subjects/objects from whom/which the data would be acquired in the final biomedical application.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_target_cohort or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) Describe the challenge cohort, i.e. the subject(s)/object(s) from whom/which the challenge data was acquired.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_challenge_cohort or "N/A", styles["Normal"]))

    # Imaging modality(ies)
    story.append(Paragraph("Imaging modality(ies)", styles["Heading3"]))

    story.append(
        Paragraph(
            "Specify the imaging technique(s) applied in the challenge.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_imaging_modalities or "N/A", styles["Normal"]))

    # Context information
    story.append(Paragraph("Context information", styles["Heading3"]))

    story.append(
        Paragraph(
            "Provide additional information given along with the images. The information may correspond ...",
            styles["Definition"],
        )
    )

    story.append(
        Paragraph(
            "a) ... directly to the image data (e.g. tumor volume).",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_contex_information_data or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) ... to the patient in general (e.g. sex, medical history).",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_contex_information_patient or "N/A", styles["Normal"]))

    # Target entity(ies)
    story.append(Paragraph("Target entity(ies)", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) Describe the data origin, i.e. the region(s)/part(s) of subject(s)/object(s) from whom/which the image data would be acquired in the final biomedical application (e.g. brain shown in computed tomography (CT) data, abdomen shown in laparoscopic video data, operating room shown in video data, thorax shown in fluoroscopy video). If necessary, differentiate between target and challenge cohort.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_data_origin or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) Describe the algorithm target, i.e. the structure(s)/subject(s)/object(s)/component(s) that the participating algorithms have been designed to focus on (e.g. tumor in the brain, tip of a medical instrument, nurse in an operating theater, catheter in a fluoroscopy scan). If necessary, differentiate between target and challenge cohort.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_algorithm_target or "N/A", styles["Normal"]))

    # Assessment aim(s)
    story.append(Paragraph("Assessment aim(s)", styles["Heading3"]))

    story.append(
        Paragraph(
            "Identify the property(ies) of the algorithms to be optimized to perform well in the challenge. If multiple properties are assessed, prioritize them (if appropriate). The properties should then be reflected in the metrics applied (see below, parameter metric(s)), and the priorities should be reflected in the ranking when combining multiple metrics that assess different properties.",
            styles["Definition"],
        )
    )
    story.append(
        ListFlowable(
            [
                Paragraph(
                    "Example 1: Find highly accurate liver segmentation algorithm for CT images.",
                    styles["Definition"],
                ),
                Paragraph(
                    "Example 2: Find lung tumor detection algorithm with high sensitivity and specificity for mammography images.",
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
            "Corresponding metrics are listed below (parameter metric(s)).",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_assesment_aim or "N/A", styles["Normal"]))

    # DATA SETS
    story.append(Paragraph("DATA SETS", styles["Heading2"]))

    # Data source(s)
    story.append(Paragraph("Data source(s)", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) Specify the device(s) used to acquire the challenge data. This includes details on the device(s) used to acquire the imaging data (e.g. manufacturer) as well as information on additional devices used for performance assessment (e.g. tracking system used in a surgical setting).",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_acquisition_devices or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) Describe relevant details on the imaging process/data acquisition for each acquisition device (e.g. image acquisition protocol(s)).",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_acquisition_protocol or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "c) Specify the center(s)/institute(s) in which the data was acquired and/or the data providing platform/source (e.g. previous challenge). If this information is not provided (e.g. for anonymization reasons), specify why.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_center or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "d) Describe relevant characteristics (e.g. level of expertise) of the subjects (e.g. surgeon)/objects (e.g. robot) involved in the data acquisition process (if any).",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_characteristic_data or "N/A", styles["Normal"]))

    # Training and test case characteristics
    story.append(Paragraph("Training and test case characteristics", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) State what is meant by one case in this challenge. A case encompasses all data that is processed to produce one result that is compared to the corresponding reference result (i.e. the desired algorithm output).<br/><br/>Examples:",
            styles["Definition"],
        )
    )

    story.append(
        ListFlowable(
            [
                Paragraph(
                    "Training and test cases both represent a CT image of a human brain. Training cases have a weak annotation (tumor present or not and tumor volume (if any)) while the test cases are annotated with the tumor contour (if any).",
                    styles["Definition"],
                ),
                Paragraph(
                    "A case refers to all information that is available for one particular patient in a specific study. This information always includes the image information as specified in data source(s) (see above) and may include context information (see above). Both training and test cases are annotated with survival (binary) 5 years after (first) image was taken.",
                    styles["Definition"],
                ),
            ],
            bulletType="bullet",
            bulletFontName="OpenSans-Light",
            bulletFontSize=10,
            bulletDedent=6,
        )
    )

    story.append(Paragraph(task.task_case_definition or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) State the total number of training, validation and test cases.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_number_of_cases or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "c) Explain why a total number of cases and the specific proportion of training, validation and test cases was chosen.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_explanation_number_proportion_data or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "d) Mention further important characteristics of the training, validation and test cases (e.g. class distribution in classification tasks chosen according to real-world distribution vs. equal class distribution) and justify the choice.",
            styles["Definition"],
        )
    )
    story.append(Paragraph(task.task_justification_of_data_characteristics or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "e) Challenge organizers are encouraged to (partly) use unseen, unpublished data for their challenges. Describe if new data will be used for the challenge and state the number of cases along with the proportion of new data.",
            styles["Definition"],
        )
    )
    story.append(Paragraph(task.task_new_data or "N/A", styles["Normal"]))

    # Annotation characteristics
    story.append(Paragraph("Annotation characteristics", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) Describe the method for determining the reference annotation, i.e. the desired algorithm output. Provide the information separately for the training, validation and test cases if necessary. Possible methods include manual image annotation, in silico ground truth generation and annotation by automatic methods.",
            styles["Definition"],
        )
    )

    story.append(
        Paragraph(
            "If human annotation was involved, state the number of annotators.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_metod_reference or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) Provide the instructions given to the annotators (if any) prior to the annotation. This may include description of a training phase with the software. Provide the information separately for the training, validation and test cases if necessary. Preferably, provide a link to the annotation protocol.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_annoation_instructions or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "c) Provide details on the subject(s)/algorithm(s) that annotated the cases (e.g. information on level of expertise such as number of years of professional experience, medically-trained or not). Provide the information separately for the training, validation and test cases if necessary.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_annotators or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "d) Describe the method(s) used to merge multiple annotations for one case (if any). Provide the information separately for the training, validation and test cases if necessary.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(str(task.task_annotation_aggregation or "N/A"), styles["Normal"]))

    # Data pre-processing method(s)
    story.append(Paragraph("Data pre-processing method(s)", styles["Heading3"]))

    story.append(
        Paragraph(
            "Describe the method(s) used for pre-processing the raw training data before it is provided to the participating teams. Provide the information separately for the training, validation and test cases if necessary.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_pre_processing_methods or "N/A", styles["Normal"]))

    # Sources of error
    story.append(Paragraph("Sources of error", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) Describe the most relevant possible error sources related to the image annotation. If possible, estimate the magnitude (range) of these errors, using inter-and intra-annotator variability, for example. Provide the information separately for the training, validation and test cases, if necessary.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_sources_of_error_images or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) In an analogous manner, describe and quantify other relevant sources of error.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_sources_of_error_other or "N/A", styles["Normal"]))

    # ASSESSMENT METHODS
    story.append(Paragraph("ASSESSMENT METHODS", styles["Heading2"]))

    # Metric(s)
    story.append(Paragraph("Metric(s)", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) Define the metric(s) to assess a property of an algorithm. These metrics should reflect the desired algorithm properties described in assessment aim(s) (see above). State which metric(s) were used to compute the ranking(s) (if any).",
            styles["Definition"],
        )
    )

    story.append(
        ListFlowable(
            [
                Paragraph(
                    "Example 1: Dice Similarity Coefficient (DSC)",
                    styles["Definition"],
                ),
                Paragraph(
                    "Example 2: Area under curve (AUC)",
                    styles["Definition"],
                ),
            ],
            bulletType="bullet",
            bulletFontName="OpenSans-Light",
            bulletFontSize=10,
            bulletDedent=6,
        )
    )

    story.append(Paragraph(task.task_evaluation_metrics or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) Justify why the metric(s) was/were chosen, preferably with reference to the biomedical application.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_justification_of_metrics or "N/A", styles["Normal"]))

    # Ranking method(s)
    story.append(Paragraph("Ranking method(s)", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) Describe the method used to compute a performance rank for all submitted algorithms based on the generated metric results on the test cases. Typically the text will describe how results obtained per case and metric are aggregated to arrive at a final score/ranking.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_rank_computation_method or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) Describe the method(s) used to manage submissions with missing results on test cases.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_missing_data or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "c) Justify why the described ranking scheme(s) was/were used.",
            styles["Definition"],
        )
    )

    story.append(
        Paragraph(
            task.task_justification_of_rank_computation_method or "N/A",
            styles["Normal"],
        )
    )

    # Statistical analyses
    story.append(Paragraph("Statistical analyses", styles["Heading3"]))

    story.append(
        Paragraph(
            "a) Provide details for the statistical methods used in the scope of the challenge analysis. This may include",
            styles["Definition"],
        )
    )
    story.append(
        ListFlowable(
            [
                Paragraph(
                    "description of the missing data handling,",
                    styles["Definition"],
                ),
                Paragraph(
                    "details about the assessment of variability of rankings,",
                    styles["Definition"],
                ),
                Paragraph(
                    "description of any method used to assess whether the data met the assumptions, required for the particular statistical approach, or",
                    styles["Definition"],
                ),
                Paragraph(
                    "indication of any software product that was used for all data analysis methods.",
                    styles["Definition"],
                ),
            ],
            bulletType="bullet",
            bulletFontName="OpenSans-Light",
            bulletFontSize=10,
            bulletDedent=6,
        )
    )

    story.append(Paragraph(task.task_statistical_analyses or "N/A", styles["Normal"]))

    story.append(
        Paragraph(
            "b) Justify why the described statistical method(s) was/were used.",
            styles["Definition"],
        )
    )

    story.append(Paragraph(task.task_justification_of_statistical_analyses or "N/A", styles["Normal"]))

    # Further analyses
    story.append(Paragraph("Further analyses", styles["Heading3"]))

    story.append(
        Paragraph(
            "Present further analyses to be performed (if applicable), e.g. related to",
            styles["Definition"],
        )
    )

    story.append(
        ListFlowable(
            [
                Paragraph(
                    "combining algorithms via ensembling,",
                    styles["Definition"],
                ),
                Paragraph(
                    "inter-algorithm variability,",
                    styles["Definition"],
                ),
                Paragraph(
                    "common problems/biases of the submitted methods, or",
                    styles["Definition"],
                ),
                Paragraph(
                    "ranking variability.",
                    styles["Definition"],
                ),
            ],
            bulletType="bullet",
            bulletFontName="OpenSans-Light",
            bulletFontSize=10,
            bulletDedent=6,
        )
    )

    story.append(Paragraph(str(task.task_further_analyses or "N/A"), styles["Normal"]))

    return story


def add_tasks_to_document(story, tasks, challenge, styles):
    if not isinstance(tasks, list):
        story = add_task_to_document(story, tasks, challenge, 1, styles)
    else:
        for idx, task in enumerate(tasks):
            story = add_task_to_document(story, task, challenge, idx + 1, styles)
    return story
