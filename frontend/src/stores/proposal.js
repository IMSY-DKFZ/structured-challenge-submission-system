import { defineStore } from 'pinia'
import { apiDelete, apiGet, apiPut, apiPost } from '@/api/api'

function stringToList(input) {
  return input.split(',').map((item) => item.trim())
}

export const useProposalStore = defineStore('proposal', {
  state: () => {
    return {
      conferences: [],
      created: '',
      proposal: [],
      proposalConference: {},
      proposalId: '',
      tasks: [],
      activeProposalOnline: false,
    }
  },

  // methods: {
  //   convertStringToList(value) {
  //     // Split the string by commas and trim spaces
  //     return value.split(',').map(item => item.trim());
  //   },
  // },
  // computed: {
  //   // ... (other computed properties)

  //   // Update this computed property to use the conversion method
  //   computedChallengeKeywords() {
  //     return this.convertStringToList(this.tab.questions.find(q => q.key === 'challengeKeywords').value);
  //   },
  // },

  getters: {
    getActiveProposalOnline: (state) => state.activeProposalOnline,
    getTasks: (state) => state.tasks,
    proposalActive: (state) => state.created !== '',
    getProposalCreated: (state) => state.created,
    getProposalConference: (state) => state.proposalConference,
    getProposalId: (state) => state.proposalId,
    async getConferences(state) {
      const resp = await apiGet('/conference/all_limited?limit=0&offset=0')
      if (resp) {
        this.conferences = resp['content']
        return resp['content']
      }
    },

    isInputStillRequired: (state) => {
      const list = []
      state.proposal.forEach((form) => {
        form.questions.forEach((item) => {
          if (item.validation.required) {
            if (typeof item.value === 'string' || item.value instanceof String) {
              if (item.value === '') {
                list.push(item.title)
              }
            } else {
              if (item.value.map((x) => x.value).includes('')) {
                // if (item.value.map((x) => (x == null ? true : false))) {
                list.push(item.title)
              }
            }
          }
        })
      })
      return list.length > 0
    },
  },
  actions: {
    setConferences(list) {
      this.conferences = list
    },

    getProposalTemplate(challengeIsLighthouseChallenge) {
      const generalQuestions = [
        {
          key: 'challenge_name',
          title: 'Challenge name',
          text: 'Use the title to convey the essential information on the challenge mission.',
          value: '',
          type: 'text',
          validation: { required: true, minlength: 2 },
          errorState: false,
        },
        {
          key: 'challenge_acronym',
          title: 'Acronym',
          text: 'Preferable, provide a short acronym of the challenge (if any).',
          value: '',
          type: 'text',
          validation: { required: false },
          errorState: false,
        },
        {
          key: 'challenge_abstract',
          title: 'Abstract',
          text: 'Provide a summary of the challenge purpose. This should include a general introduction in the topic from both a biomedical as well as from a technical point of view and clearly state the envisioned technical and/or biomedical impact of the challenge.',
          value: '',
          type: 'textarea',
          validation: { required: true, minlength: 10 },
          errorState: false,
        },
        {
          key: 'challenge_keywords',
          title: 'Keywords',
          text: 'List the primary keywords that characterize the challenge. (Separate your inputs with comma like Keyword 1, Keyword 2)',
          value: [],
          type: 'text',
          validation: { required: true },
          errorState: false,
          convertToList: true,
        },
        {
          key: 'challenge_year',
          title: 'Year',
          text: 'Please indicate the year of the challenge. If you are applying for next yearʼs conference, please write the year of that conference..',
          value: '',
          type: 'text',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'challenge_novelty',
          title: 'Novelty of the challenge',
          text: 'Briefly describe the novelty of the challenge.',
          value: '',
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'challenge_application_scenarios',
          title: 'Task description and application scenarios',
          text: 'Briefly describe the application scenarios for the tasks in the challenge.',
          value: '',
          type: 'textarea',
          validation: { required: false },
          errorState: false,
        },

      ]

      if (challengeIsLighthouseChallenge === true) {
        generalQuestions.push({ //////////////////////////////////////////////
          key: 'challenge_lighthouse_general_terms_agreed',
          title: 'Lighthouse challenge agreement',
          text:
            '<p>The organizers agree to all of the following points:</p>' +
            '<ul>\n' +
            '<li>The full labeling protocol will be sent to the challenge chairs in addition to the full proposal document.</li>\n' +
            '<li>A set of a few representative data samples including annotations will be sent to the challenge chairs in addition to the full proposal document.</li>\n' +
            '<li>The challenge will be open for at least 4 months.</li>\n' +
            '<li>For the dataset review, the challenge chairs will get access to the data at least 3 months before challenge opening.</li>\n' +
            '</ul>',
          value: false,
          type: 'checkbox',
          label: 'Challenge organizers have read and agree to all of the above terms and conditions.',
          validation: { required: true },
          errorState: false,
        },
          {
            key: 'challenge_lighthouse_what_is_different',
            title: 'Lighthouse challenge information',
            text: 'In two sentences or less, what sets your challenge apart from ordinary MICCAI challenges. In other words: What makes your challenge a lighthouse challenge?',
            value: '',
            type: 'textarea',
            validation: { required: true },
            errorState: false,
          },
          {
            key: 'challenge_lighthouse_closest_challenge',
            title: 'Previous challenge(s)',
            text: 'What is the closest challenge to your proposed lighthouse challenge? Are there previous versions of it? Specifically, if you applied for a 2024 challenge, what is the delta between the two iterations? (e.g., number of centers for new data, number of newly added data – This is not to be confused with details about the total data set)',
            value: '',
            type: 'textarea',
            validation: { required: true },
            errorState: false,
          },
          {
            key: 'challenge_lighthouse_test_set_already_used',
            title: 'Test set status',
            text: 'Was the test set (or parts of it) already used in previous challenges and/or previously made publicly available?',
            value: '',
            type: 'textarea',
            validation: { required: true },
            errorState: false,
          },
          {
            key: 'challenge_lighthouse_major_scientific_advances',
            title: 'What major scientific advances or insights are expected from the challenge?',
            text: 'Please describe the major scientific advances ore insights you expect to be gained from the challenge. Please include references to the state of the art in your description and list open research questions to which the challenge seeks answers or solutions.',
            value: '',
            type: 'textarea',
            validation: { required: true },
            errorState: false,
          },
          {
            key: 'challenge_lighthouse_clinical_affiliation',
            title: 'Clinical body affiliation',
            text: 'Please describe your proposed challenge’s affiliation with a clinical body, if any. How do you plan to engage the clinical community that your challenge is set to impact?',
            value: '',
            type: 'textarea',
            validation: { required: true },
            errorState: false,
          },
          {
            key: 'challenge_lighthouse_deadline_for_data',
            title: 'Deadline for data acquisition and annotation',
            text: 'What’s the deadline for data acquisition and annotation?',
            value: '',
            type: 'textarea',
            validation: { required: true },
            errorState: false,
          },
          {
            key: 'challenge_lighthouse_prize_money',
            title: 'How much prize money has been secured?',
            text: 'Please state how much prize money has already been secured for the challenge.',
            value: '',
            type: 'textarea',
            validation: { required: true },
            errorState: false,
          },
          {
            key: 'challenge_lighthouse_compute_per_participant',
            title: 'Computing requirements per participant',
            text: 'Roughly estimate how much computing power would be required per challenge participant?',
            value: '',
            type: 'textarea',
            validation: { required: true },
            errorState: false,
          },

          // {
          //   key: 'challenge_author_names',
          //   title: 'Challenge authors',
          //   text: 'Please list all authors of the challenge. These names will be used for the review process to <a href="https://cmt3.research.microsoft.com" target="_blank">cmt3.research.microsoft.com/</a> as well as for the challenge registration process. They won\'t be displayed in the design document. Separate your inputs with comma.',
          //   value: [],
          //   type: 'textarea',
          //   validation: { required: false },
          //   errorState: false,
          //   convertToList: true,
          // },
          // {
          //   key: 'challenge_author_emails',
          //   title: 'Challenge author emails',
          //   text: 'Please list all authors\' email addresses. They will be used in order to create accounts for the review process on <a href="https://cmt3.research.microsoft.com" target="_blank">cmt3.research.microsoft.com/</a>. They won\'t be displayed in the design document. Separate your inputs with comma.',
          //   value: [],
          //   type: 'textarea',
          //   validation: { required: false },
          //   errorState: false,
          //   convertToList: true,
          // },
        );
      }

      const conferenceQuestions = [
        {
          key: 'challenge_workshop',
          title: 'Associated workshops',
          text: 'If the challenge is part of a workshop, please indicate the workshop.',
          value: '',
          type: 'textarea',
          validation: { required: false },
          errorState: false,
        },
        {
          key: 'challenge_expected_number_of_participants',
          title: 'Expected number of participants',
          text: 'Please explain the basis of your estimate (e.g. numbers from previous challenges) and/or provide a list of potential participants and indicate if they have already confirmed their willingness to contribute.',
          value: '',
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'challenge_duration',
          title: 'Duration',
          text: 'How long does the challenge take? Possible values: half day, full day, 2 hours, etc.',
          value: '',
          // type: 'textarea',
          type: 'selectWithOther',
          options: ['Full day', 'Half day', '2 Hours'],
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'challenge_duration_explanation',
          title: 'Longer duration explanation',
          text: 'In case you selected half or full day, please explain why you need a long slot for your challenge.',
          value: '',
          type: 'textarea',
          validation: { required: false },
          errorState: false,
        },
        {
          key: 'challenge_publication_and_future',
          title: 'Publication and future plans',
          text: 'Please indicate if you plan to coordinate a publication of the challenge results.',
          value: '',
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'challenge_space_and_hardware_requirements',
          title: 'Space/ hardware requirements',
          text:
            'Please describe the platform used for any online challenge. For on-site challenges, indicate how you plan to provide a fair computing environment.\n' +
            'Please list any technical equipment or support needed (e.g., projectors, computers, monitors, loud speakers, microphones).',
          value: '',
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
      ]

      const taskQuestions = [
        {
          key: 'task_name',
          title: 'Title',
          text: '(You can change the title if neccessary, otherwise no need to modify)',
          value: [],
          default: '',
          type: 'text',
          validation: { required: true, minlength: 2 },
          errorState: false,
        },
        {
          key: 'task_abstract',
          title: 'Abstract',
          text: 'Provide a summary of the challenge purpose. This should include a general introduction in the topic from both a biomedical as well as from a technical point of view and clearly state the envisioned technical and/or biomedical impact of the challenge.',
          value: [],
          type: 'textarea',
          validation: { required: false },
          errorState: false,
        },
        {
          //JSON format such as {"Key 1", "Key 2"}
          key: 'task_keywords',
          title: 'Keywords',
          text: 'List the primary keywords that characterize the challenge. (Separate your inputs with comma like Keyword 1, Keyword 2)',
          value: [],
          type: 'text',
          validation: { required: false },
          errorState: false,
          convertToList: true,
        },
        {
          key: 'task_organizing_team',
          title: 'Organizing team',
          text: 'Provide information on the organizing team (names and affiliations).',
          value: '',
          type: 'textarea',
          validation: { required: true, minlength: 2 },
          errorState: false,
        },

        {
          key: 'task_contact_person',
          title: 'Contact Person',
          text: 'Provide information on the primary contact person.',
          value: [],
          type: 'textarea',
          validation: { required: true, minlength: 1 },
          errorState: false,
        },
        {
          key: 'task_lifecycle',
          title: 'Life cycle type',
          text:
            '<div>Define the intended submission cycle of the challenge. Include information on whether/how the challenge will be continued after the challenge has taken place. Not every challenge closes after the submission deadline (one-time event). Sometimes it is possible to submit results after the deadline (open call) or the challenge is repeated with some modifications (repeated event).\n</div>' +
            '<small>Examples:\n' +
            '          <ul>\n' +
            '            <li>One-time event with fixed conference submission deadline</li>\n' +
            '            <li>Open call (challenge opens for new submissions after conference deadline)</li>\n' +
            '            <li>Repeated event with annual fixed conference submission deadline</li>\n' +
            '            <li>Repeated event as open call challenge</li>\n' +
            '          </ul>\n' +
            '        </small>',
          value: [],
          // type: 'textarea',
          type: 'selectWithOther',
          options: [
            'One-time event with fixed conference submission deadline',
            'Open call  (challenge opens for new submissions after conference deadline)',
            'Repeated event with annual fixed conference submission deadline',
            'Repeated event as open call challenge',
          ],
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_conference_name',
          title: 'Event',
          text: 'Report the event (e.g. conference) that is associated with the challenge (if any).',
          value: [],
          type: 'textarea',
          validation: { required: false },
          errorState: false,
        },
        {
          key: 'task_platform',
          title: 'Report the platform (e.g. grand-challenge.org) used to run the challenge.',
          text: '<p>Report the platform (e.g. grand-challenge.org) used to run the challenge.<br><br><i>Please note:</i> If you would like to run your challenge on <b>grand-challenge.org</b>, please also fill out their <a href="https://grand-challenge.org/challenges/requests/create/" target="_blank">challenge request form</a> as soon as possible. You can upload the PDF from your MICCAI application and then fill most fields in their form with “see PDF”. You will also need to provide details regarding your compute and storage requirements. You can find more information about that <a href="https://grand-challenge.org/documentation/create-your-own-challenge/#budget" target="_blank">here</a>. Finally, please also note that the Grand Challenge platform strongly encourages open science and hence requires that you publish your training data with a permissive CC-BY license and that you encourage your participants to publish their source code with an appropriate license as well.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_url',
          title: 'Website',
          text: 'Provide the URL for the challenge website (if any).</p>',
          value: [],
          type: 'text',
          validation: { required: false, allowSpecialCharacters: false },
          errorState: false,
        },
        {
          key: 'task_interaction_level_policy',
          title: 'Allowed user interaction',
          text: '<p>Define the <b>allowed user interaction </b>of the algorithms assessed (e.g. only (semi-)automatic methods allowed).</p>',
          value: [],
          // type: 'textarea',
          type: 'selectMultipleWithOther',
          options: ['Fully automatic', 'Semi automatic', 'Fully interactive'],
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_training_data_policy',
          title: 'Training data policy',
          text:
            '<p>Define the policy on the <b>usage of training data</b>. The data used to train algorithms may, for example, be restricted to the data provided by the challenge or to publicly available data including (open) pre-trained nets.</p>' +
            '<small>Examples:' +
            '          <ul>' +
            '            <li>No policy defined.</li>' +
            '            <li>No additional data allowed.' +
            '            <li>Private data is allowed.</li>' +
            '            <li>Publicly available data is allowed.</li>' +
            '          </ul>' +
            '        </small>',
          value: [],
          // type: 'textarea',
          type: 'selectWithOther',
          options: [
            'No policy defined',
            'No additional data allowed',
            'Private data is allowed',
            'Publicly available data is allowed',
          ],
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_organizer_participation_policy',
          title: 'Organizer policy',
          text:
            "<p>Define the <b>participation policy for members of the organizers' institutes</b>. For example, members of the organizers' institutes may participate in the challenge but are not eligible for awards.</p>" +
            '<small>Examples:' +
            '          <ul>' +
            '            <li>May not participate.' +
            '            <li>May participate but not eligible for awards and not listed in leaderboard.' +
            '          </ul>' +
            '        </small>',
          value: [],
          type: 'selectWithOther',
          options: [
            'May not participate',
            'May participate but not eligible for awards and not listed in leaderboard',
          ],
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_award_policy',
          title: 'Award policy',
          text: '<p>Define the <b>award policy</b>. In particular, provide details with respect to challenge prizes.',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_results_announcement',
          title: 'Result announcement policy',
          text:
            '<p>Define the policy for <b>result announcement</b>.</p>' +
            '<small>Examples:\n' +
            '          <ul>\n' +
            '            <li> Top 3 performing methods will be announced publicly.</li>\n' +
            '            <li>Participating teams can choose whether the performance results will be made public.</li>\n' +
            '          </ul>\n' +
            '        </small>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },

        {
          key: 'task_pulication_policy',
          title: 'Publication policy',
          text:
            '<div>Define the <b>publication policy</b>. In particular, provide details on ...</div>' +
            '          <ul>\n' +
            '            <li>... who of the participating teams/the participating teams’ members qualifies as author</li>\n' +
            '            <li>... whether the participating teams may publish their own results separately, and (if so)</li>\n' +
            '            <li>... whether an embargo time is defined (so that challenge organizers can publish a challenge paper first).</li>\n' +
            '          </ul>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_result_submission_method',
          title: 'Submission method',
          text:
            '<div>Describe the method used for result submission. Preferably, provide a link to the <b>submission instructions</b>.</div>' +
            '<small>Examples:\n' +
            '          <ul>\n' +
            '            <li>Docker container on the Synapse platform. Link to submission instructions: <URL></li>\n' +
            '            <li>Algorithm output was sent to organizers via e-mail. Submission instructions were sent by e-mail.</li>\n' +
            '            <li>Algorithm container submission (type 2) on Grand Challenge.</li>\n' +
            '          </ul>\n' +
            '        </small>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_pre_evaluation',
          title: 'Pre-evaluation',
          text: '<p>Provide information on the possibility for participating teams to evaluate their <b>evaluate their algorithms before submitting final results.</b> For example, many challenges allow submission of multiple results, and only the last run is officially counted to compute challenge results.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_schedule',
          title: 'Schedule',
          text:
            '<div>Provide a <b>timetable</b> for the challenge. Preferably, this should include</div>' +
            '          <ul>\n' +
            '            <li>the release date(s) of the training cases (if any) URL</li>\n' +
            '            <li>the registration date/period</li>\n' +
            '            <li>the release date(s) of the test cases and validation cases (if any)</li>\n' +
            '            <li>the submission date(s)</li>\n' +
            '            <li>associated workshop days (if any)</li>\n' +
            '            <li>the release date(s) of the results</li>\n' +
            '          </ul>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_ethics_approval',
          title: 'Ethics approval',
          text: '<p>Indicate whether <b>ethics approval</b>is necessary for the data. If yes, provide details on the ethics approval, preferably institutional review board, location, date and number of the ethics approval (if applicable). Add the URL or a reference to the document of the ethics approval (if available).</p>',
          value: [],
          type: 'textarea',
          validation: { required: false },
          errorState: false,
        },
        {
          // this ok?
          key: 'task_licence',
          title: 'Data usage agreement',
          text:
            '<p>Clarify how the data can be used and distributed by the teams that participate in the challenge and by others during and after the challenge. This should include the explicit <b>listing of the license</b> applied (click <a href="https://creativecommons.org/licenses/" target="_blank">here</a> for more information).</p>',
          // '<small>Examples:\n' +
          // '          <ul>\n' +
          // '            <li>CC BY (Attribution)\n' +
          // '            <li>CC BY-SA (Attribution-ShareAlike)</li>\n' +
          // '            <li>CC BY-ND (Attribution-NoDerivs)</li>\n' +
          // '            <li>CC BY-NC (Attribution-NonCommercial)\n' +
          // '            <li>CC BY-NC-SA (Attribution-NonCommercial-ShareAlike)</li>\n' +
          // '            <li>CC BY-NC-ND (Attribution-NonCommercial-NoDerivs)</li>\n' +
          // '          </ul>\n' +
          // '        </small>',
          value: [],
          // type: 'textarea',
          type: 'selectWithOther',
          options: [
            'CC BY (Attribution)',
            'CC BY-SA (Attribution-ShareAlike)',
            'CC BY-ND (Attribution-NoDerivs)',
            'CC BY-NC (Attribution-NonCommercial)',
            'CC BY-NC-SA (Attribution-NonCommercial-ShareAlike)',
            'CC BY-NC-ND (Attribution-NonCommercial-NoDerivs)',
            'GNU General Public License',
            'MIT License',
            'Apache License',

          ],
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_code_availability_organizers',
          title: 'Code availability of the organizers',
          text: "<p>Provide information on the <b>accessibility of the organizers' evaluation software</b> (e.g. code to produce rankings). Preferably, provide a link to the code and add information on the supported platforms.</p>",
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_code_availability_participants',
          title: 'Code availability of the participating teams',
          text: "<p>In an analogous manner, provide information on the <b>accessibility of the  participating teams' code</b>.</p>",
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_conflict_of_interest',
          title: 'Conflicts of interest',
          text: '<p>Provide information related to conflicts of interest. In particular provide information related to <b>sponsoring/funding</b> of the challenge. Also, state explicitly who had/will have <b>access to the test case labels and when</b>.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_field_of_application',
          title: 'Field of application(s)',
          text:
            '<p>State the main <b>field(s) of application</b> that the participating algorithms target.</p>' +
            '<small>Examples:\n' +
            '          <ul>\n' +
            '            <li>Diagnosis</li>\n' +
            '            <li>Education</li>\n' +
            '            <li>Intervention assistance</li>\n' +
            '            <li>Intervention follow-up</li>\n' +
            '            <li>Intervention planning</li>\n' +
            '            <li>Prognosis</li>\n' +
            '            <li>Research</li>\n' +
            '            <li>Screening</li>\n' +
            '            <li>Training</li>\n' +
            '            <li>Cross-phase</li>\n' +
            '          </ul>\n' +
            '        </small>',
          value: [],
          // type: 'textarea',
          type: 'selectMultipleWithOther',
          options: [
            'Assistance',
            'CAD',
            'Cross phase',
            'Data reduction',
            'Decision support',
            'Diagnosis',
            'Education',
            'Intervention follow up',
            'Intervention planning',
            'Longitudinal study',
            'Medical data management',
            'Prevention',
            'Prognosis',
            'Research',
            'Screening',
            'Surgery',
            'Training',
            'Treatment planning',
          ],
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_task_category',
          title: 'Task Category(ies)',
          text:
            '<p>State the <b>task category(ies)</b>.</p>' +
            '<small>Examples:\n' +
            '          <ul>\n' +
            '            <li>Classification</li>\n' +
            '            <li>Detection</li>\n' +
            '            <li>Localization</li>\n' +
            '            <li>Modeling</li>\n' +
            '            <li>Prediction</li>\n' +
            '            <li>Reconstruction</li>\n' +
            '            <li>Registration</li>\n' +
            '            <li>Retrieval</li>\n' +
            '            <li>Segmentation</li>\n' +
            '            <li>Tracking</li>\n' +
            '          </ul>\n' +
            '        </small>',
          value: [],
          type: 'selectMultipleWithOther',
          options: [
            'Classification',
            'Denoising',
            'Detection',
            'Localization',
            'Modeling',
            'Prediction',
            'Reconstruction',
            'Registration',
            'Regression',
            'Restoration',
            'Retrieval',
            'Segmentation',
            'Simulation',
            'Stitching',
            'Tracing',
            'Tracking',
          ],
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_target_cohort',
          title: 'Target cohort',
          text: '<p>We distinguish between the target cohort and the challenge cohort. For example, a challenge could be designed around the task of medical instrument tracking in robotic kidney surgery. While the challenge could be based on ex vivo data obtained from a laparoscopic training environment with porcine organs (challenge cohort), the final biomedical application (i.e. robotic kidney surgery) would be targeted on real patients with certain characteristics defined by inclusion criteria such as restrictions regarding sex or age (target cohort)</p><p>Describe the <b>target cohort of task</b>, i.e. the subjects/objects from whom/which the data would be acquired in the final biomedical application.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_challenge_cohort',
          title: 'Challenge cohort',
          text: '<p>Describe the <b>challenge cohort</b>, i.e. the subject(s)/object(s) from whom/which the challenge data was acquired.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_imaging_modalities',
          title: 'Imaging technique(s)',
          text: '<p>Specify the <b>imaging technique(s)</b> applied in the challenge.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_contex_information_data',
          title: 'Context information: Image data',
          text: '<p>Provide additional information given along with the images. The information may correspond to directly to the <b>imaging data</b> (e.g. tumor volume).</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_contex_information_patient',
          title: 'Context information: Patient',
          text: '<p>Provide additional information given along with the images. The information may correspond to the <b>patient</b> in general (e.g. gender, medical history).</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_data_origin',
          title: 'Data origin',
          text: '<p>Describe the <b>data origin</b>, i.e. the region(s)/part(s) of subject(s)/object(s) from whom/which the image data would be acquired in the final biomedical application (e.g. brain shown in computed tomography (CT) data, abdomen shown in laparoscopic video data, operating room shown in video data, thorax shown in fluoroscopy video). If necessary, differentiate between target and challenge cohort.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_algorithm_target',
          title: 'Algorithm Target',
          text: '<p>Describe the <b>algorithm target</b>, i.e. the structure(s)/subject(s)/object(s)/component(s) that the participating algorithms have been designed to focus on (e.g. tumor in the brain, tip of a medical instrument, nurse in an operating theater, catheter in a fluoroscopy scan). If necessary, differentiate between target and challenge cohort.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_assesment_aim',
          title: 'Assessment aim(s)',
          text:
            '<p>Identify the <b> property(ies) of the algorithms to be optimized</b> to perform well in the challenge. If multiple properties are assessed, prioritize them (if appropriate). The properties should then be reflected in the metrics applied (parameter 26), and the priorities should be reflected in the ranking when combining multiple metrics that assess different properties.</p>' +
            '<small>\n' +
            '          <ul>\n' +
            '            <li>Example 1: Find highly accurate liver segmentation algorithm for CT images.</li>\n' +
            '            <li>Example 2: Find lung tumor detection algorithm with high sensitivity and specificity for mammography images.</li>\n' +
            '          </ul>\n' +
            '        </small>' +
            '<small>Corresponding metrics are listed below (parameter 26):' +
            '<p>Accuracy, Applicability, Complexity, Consistency, Ergonomics, Feasibility, Hardware requirements, Interaction, Integration in workflow, Precision, Reliability, Robustness, Runtime, Sensitivity, Specificity, Usability, User satisfaction</p></small>',
          value: [],
          // type: 'textarea',
          type: 'selectMultipleWithOther',
          options: [
            'Accuracy',
            'Applicability',
            'Complexity',
            'Consistency',
            'Ergonomics',
            'Feasibility',
            'Hardware requirements',
            'Interaction',
            'Integration in workflow',
            'Precision',
            'Reliability',
            'Robustness',
            'Runtime',
            'Sensitivity',
            'Specificity',
            'Usability',
            'User satisfaction',
          ],
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_acquisition_devices',
          title: 'Data acquisition device(s)',
          text: '<p>Specify the <b>device(s)</b> used to acquire the challenge data. This includes details on the device(s) used to acquire the imaging data (e.g. manufacturer) as well as information on additional devices used for performance assessment (e.g. tracking system used in a surgical setting).</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_acquisition_protocol',
          title: 'Data acquisition details',
          text: '<p>Describe relevant details on the imaging process/<b>data acquisition</b> for each acquisition device (e.g. image acquisition protocol(s)).</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_center',
          title: 'Center(s)/institute(s)',
          text: '<p>Specify the <b>center(s)/institute(s)</b> in which the data was acquired and/or the <b>ata providing platform/source</b> (e.g. previous challenge). If this information is not provided (e.g. for anonymization reasons), specify why.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_characteristic_data',
          title: 'Characteristics of the subjects',
          text: '<p>Describe relevant <b>characteristics</b> (e.g. level of expertise) <b>of the subjects</b> (e.g. surgeon)/objects (e.g. robot) involved in the data acquisition process (if any).</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_case_definition',
          title: 'Case definition',
          text:
            '<div>State what is meant by one <b>case</b> in this challenge. A case encompasses all data that is processed to produce one result that is compared to the corresponding reference result (i.e. the desired algorithm output).</div>' +
            '<small>Examples:\n' +
            '          <ul>\n' +
            '            <li>Training and test cases both represent a CT image of a human brain. Training cases have a weak annotation (tumor present or not and tumor volume (if any)) while the test cases are annotated with the tumor contour (if any).</li>\n' +
            '            <li>A case refers to all information that is available for one particular patient in a specific study. This information always includes the image information as specified in data source(s) (parameter 21) and may include context information (parameter 18). Both training and test cases are annotated with survival (binary) 5 years after (first) image was taken.</li>\n' +
            '          </ul>\n' +
            '        </small>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_number_of_cases',
          title: 'Number of cases',
          text: '<p>State individually total number of training, validation and test cases.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_explanation_number_proportion_data',
          title: 'Explanation of data proportion',
          text: '<p>Explain why a total number of cases and the specific <b>proportion</b> of training, validation and test cases was chosen.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_new_data',
          title: 'Further important characteristics of the cases',
          text: '<p>Challenge organizers are encouraged to (partly) use <b>unseen, unpublished data</b> for their challenges. Describe if new data will be used for the challenge and state the number of cases along with the proportion of new data.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_justification_of_data_characteristics',
          title: 'Further important characteristics of the cases',
          text: '<p>Mention <b>further important characteristics</b> of the training, validation and test cases (e.g. class distribution in classification tasks chosen according to real-world distribution vs. equal class distribution) and justify the choice.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_metod_reference',
          title: 'Method for determining the reference annotation',
          text: '<p>Describe the <b>method for determining the reference annotation</b> i.e. the desired algorithm output. Provide the information separately for the training, validation and test cases if necessary. Possible methods include manual image annotation, in silico ground truth generation and annotation by automatic methods.</p><br><p>If human annotation was involved, state the <b>number of annotators</b>.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_annoation_instructions',
          title: 'Instructions given to the annotators',
          text: '<p>Provide the <b>instructions given to the annotators</b> (if any) prior to the annotation. This may include description of a training phase with the software. Provide the information separately for the training, validation and test cases if necessary. Preferably, provide a link to the annotation protocol.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_annotators',
          title: 'Details on the subject(s)/algorithm(s) that annotated the cases',
          text: '<p>Provide <b>details on the subject(s)/algorithm(s) that annotated</b> the cases (e.g. information on level of expertise such as number of years of professional experience, medically-trained or not). Provide the information separately for the training, validation and test cases if necessary.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_annotation_aggregation',
          title: 'Method(s) used to merge multiple annotations',
          text: '<p>Describe the <b>method(s) used to merge multiple annotations</b> for one case (if any). Provide the information separately for the training, validation and test cases if necessary.</p>',
          value: [],
          type: 'textarea',
          validation: { required: false },
          errorState: false,
        },
        {
          key: 'task_pre_processing_methods',
          title: 'Data pre-processing method(s)',
          text: '<p>Describe the <b>method(s) used for pre-processing</b> the raw training data before it is provided to the participating teams. Provide the information separately for the training, validation and test cases if necessary.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_sources_of_error_images',
          title: 'Sources of error related to the image annotation',
          text: '<p>Describe the most relevant <b>possible error sources related to the image annotation</b>. If possible, estimate the magnitude (range) of these errors, using inter- and intra-annotator variability, for example. Provide the information separately for the training, validation and test cases, if necessary.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_sources_of_error_other',
          title: 'Other sources of error',
          text: '<p>In an analogous manner, describe and quantify other relevant sources of error.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_evaluation_metrics',
          title: 'Metric(s)',
          text:
            '<p>Define the metric(s) to assess a property of an algorithm. These metrics should reflect the desired algorithm properties described in assessment aim(s) (parameter 20). State which metric(s) were used to compute the ranking(s) (if any).</p>' +
            '<small>\n' +
            '          <ul>\n' +
            '            <li>Example 1: Dice Similarity Coefficient (DSC)</li>\n' +
            '            <li>Example 2: Area under curve (AUC)</li>\n' +
            '          </ul>\n' +
            '        </small>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_justification_of_metrics',
          title: 'Justification of metric(s)',
          text: '<p>Justify why the metric(s) was/were chosen, preferably with reference to the biomedical application.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_rank_computation_method',
          title: 'Method used to compute a performance rank',
          text: '<p>Describe the method used to compute a performance rank for all submitted algorithms based on the generated metric results on the test cases. Typically the text will describe how results obtained per case and metric are aggregated to arrive at a final score/ranking.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_missing_data',
          title: 'Submissions with missing results',
          text: '<p>Describe the method(s) used to manage submissions with missing results on test cases.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_justification_of_rank_computation_method',
          title: 'Justification of ranking',
          text: '<p>Justify why the described ranking scheme(s) was/were used.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_statistical_analyses',
          title: 'Details for the statistical methods',
          text:
            '<div>Provide details for the statistical methods used in the scope of the challenge analysis. This may include</div>' +
            '          <ul>\n' +
            '            <li>description of the missing data handling,</li>\n' +
            '            <li>details about the assessment of variability of rankings,</li>\n' +
            '            <li>description of any method used to assess whether the data met the assumptions, required for the particular statistical approach, or</li>\n' +
            '            <li>indication of any software product that was used for all data analysis methods.</li>\n' +
            '          </ul>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_justification_of_statistical_analyses',
          title: 'Justification of statistical methods',
          text: '<p>Justify why the described statistical method(s) was/were used.</p>',
          value: [],
          type: 'textarea',
          validation: { required: true },
          errorState: false,
        },
        {
          key: 'task_further_analyses',
          title: 'Further analyses',
          text:
            '<div>Present further analyses to be performed (if applicable), e.g. related to</div>' +
            '          <ul>\n' +
            '            <li>combining algorithms via ensembling,</li>\n' +
            '            <li>inter-algorithm variability,</li>\n' +
            '            <li>common problems/biases of the submitted methods, or</li>\n' +
            '            <li>ranking variability.</li>\n' +
            '          </ul>',
          value: [],
          type: 'textarea',
          validation: { required: false },
          errorState: false,
        },
      ]

      const additionalQuestions = [
        {
          key: 'challenge_references',
          title: 'References',
          text: 'Please include any reference important for the challenge design, for example publications on the data, the annotation process or the chosen metrics as well as DOIs referring to data or code.',
          value: '',
          type: 'textarea',
          validation: { required: false },
          errorState: false,
        },
        {
          key: 'challenge_further_comments',
          title: 'Further comments',
          text: 'Do you have any further comments that may be important for the challenge chairs to know?',
          value: '',
          type: 'textarea',
          validation: { required: false },
          errorState: false,
        },
      ]

      return [
        {
          formName: 'General',
          questions: generalQuestions
        },
        {
          formName: 'Conference',
          questions: conferenceQuestions
        },
        {
          formName: 'Tasks',
          useTaskForm: true,
          questions: taskQuestions
        },
        {
          formName: 'Additional',
          questions: additionalQuestions
        },
      ]
    },
    setActiveProposalOnline(state) {
      this.activeProposalOnline = state
    },
    buildProposal(proposalRaw) {
      this.proposal = []

      let proposal = this.getProposalTemplate(proposalRaw.challenge_is_lighthouse_challenge)
      this.created = proposalRaw.created_time
      this.proposalId = proposalRaw.id
      let tasksRaw = proposalRaw['challenge_tasks']
      this.tasks = tasksRaw

      let keys = [...Object.keys(proposalRaw)]
      let values = [...Object.values(proposalRaw)]
      if (tasksRaw.length > 0) {
        let taskKeys = Object.keys(tasksRaw[0])
        let taskValues = tasksRaw.map((item) => taskKeys.map((key) => item[key]))
        taskValues = taskValues[0].map((col, i) => taskValues.map((row) => row[i]))
        keys.push(...taskKeys)
        values.push(...taskValues)
      }

      proposal.forEach((form) => {
        this.proposal.push({
          formName: form.formName,
          useTaskForm: form.formName === 'Tasks',
          questions: form.questions.map((x) => {
            if (form.formName === 'Tasks') {

              let searchForKey = x.key
              let indexOfKey = keys.indexOf(searchForKey)
              let vals = indexOfKey !== -1 ? values[indexOfKey] : []

              return {
                ...x,
                value: vals.map((val, idx) => ({
                  ...x,
                  value: val,
                  errorState: false,
                  uniqueId: searchForKey + idx,
                })),
              }
              // return {
              //   ...x,
              //   // value: proposalRaw['challenge_tasks'].map((item) => item[searchForKey].toString()),
              //   value: proposalRaw['challenge_tasks'].map((item) =>
              //     item[searchForKey] !== null ? item[searchForKey] : ''
              //   ),
              // }
            }

            let searchForKey = x.key
            let indexOfKey = keys.indexOf(searchForKey)
            return {
              ...x,
              value: indexOfKey >= 0
                ? values[indexOfKey]
                  ? values[indexOfKey].toString()
                  : x.value
                : x.value,
            }
          }),
        })
      })
    },
    newProposal() {
      this.proposal = []
      this.proposalId = ''
      this.created = new Date()
      this.activeProposalOnline = false
      this.proposal = this.getProposalTemplate()
      this.proposalConference = { 'conferenceName': 'MICCAI 2025 Lighthouse Challenges', 'submitMessage': '<p>Thanks for preparing your structured challenge design document.</p>' }
    },
    resetCreated() {
      this.created = ''
    },
    createTask(name) {
      const item = {
        name: name,
        value: null,
        errorState: false,
      }
      this.tasks.push(item)
      this.proposal
        .find((y) => y.formName === 'Tasks')
        .questions.map((x, idx) => {
          return {
            ...x,
            value: x.value.push({
              ...item,
              key: item.name + idx,
              uniqueId: item.name + idx,
              questionKey: x.key,
            }),
          }
        })
    },
    resetTasks() {
      this.tasks = []
    },
    deleteTask(name) {
      this.tasks = this.tasks.filter((x) => x.name !== name)
      const taskTab = this.proposal.findIndex((y) => y.formName === 'Tasks')
      this.proposal[taskTab].questions = this.proposal[taskTab].questions.map((x) => {
        const list = x.value.filter((y) => y.name !== name)
        return {
          ...x,
          errorState: list.map((z) => z.errorState).includes(true),
          value: list,
        }
      })
    },
  },
})
