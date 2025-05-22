<template>
  <div>
    <VueTextSection>
      <template #title>Create challenge proposals</template>
      <div class="accordion accordion-flush" id="accordionCreateChallengeProposals">
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challenge-1" aria-expanded="false" aria-controls="challenge-1">
              I want to create a task in my proposal but it doesn't work. What is wrong?
            </button>
          </h2>
          <div id="challenge-1" class="accordion-collapse collapse" data-bs-parent="#challenge-1">
            <VueTextSection>
              <template #text>
                <p>This may have multiple reasons:</p>
                <ul>
                  <li>
                    You did not enter a task name. Please put a name in the textfield to the left of
                    the create task button.
                  </li>
                  <li>
                    You already used this task name in that challenge. Please choose a different
                    name.
                  </li>
                  <li>
                    You used leading/ trailing whitespaces or special characters. Please remove
                    them.
                  </li>
                </ul>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challenge-2" aria-expanded="false" aria-controls="challenge-2">
              I cannot save my proposal. What should I do?
            </button>
          </h2>
          <div id="challenge-2" class="accordion-collapse collapse" data-bs-parent="#challenge-2">
            <VueTextSection>
              <template #text>
                <p>This may have multiple reasons:</p>
                <ul>
                  <li>You did not enter a challenge name. Please name the challenge.</li>
                  <li>
                    Your entry is not valid. E.g. you did use special characters in the task name
                    field. Make sure that everything is filled out in the right way.
                  </li>
                  <li>
                    You don't have any changes. The button will be enabled after you changed
                    something.
                  </li>
                </ul>
              </template>
            </VueTextSection>
          </div>
        </div>
        <!-- <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challenge-3" aria-expanded="false" aria-controls="challenge-3">
              I want to see what fields I missed in the form. How does it work?
            </button>
          </h2>
          <div id="challenge-3" class="accordion-collapse collapse" data-bs-parent="#challenge-3">
            <VueTextSection>
              <template #text>
                <p>
                  On the right, you will find a what's missing? button. Pressing it will show a
                  summary of missing parameters. These are also highlighted in your proposal form.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div> -->
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challenge-4" aria-expanded="false" aria-controls="challenge-4">
              How many parameters do I have to fill out to submit?
            </button>
          </h2>
          <div id="challenge-4" class="accordion-collapse collapse" data-bs-parent="#challenge-4">
            <VueTextSection>
              <template #text>
                <p>At least 90% of parameters have to be filled out.</p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challenge-5" aria-expanded="false" aria-controls="challenge-5">
              How many tasks can I create?
            </button>
          </h2>
          <div id="challenge-5" class="accordion-collapse collapse" data-bs-parent="#challenge-5">
            <VueTextSection>
              <template #text>
                <p>
                  In general, there is no limit. But keep in mind that every task has to be
                  implemented in your challenge.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <!-- <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challenge-6" aria-expanded="false" aria-controls="challenge-6">
              I want to submit a challenge proposal for next year's conference. How does it work? Do I have to
              submit it again next year?
            </button>
          </h2>
          <div id="challenge-6" class="accordion-collapse collapse" data-bs-parent="#challenge-6">
            <VueTextSection>
              <template #text>
                <p>
                  Please create your challenge and indicate year. It will be in the same review process as the other
                  proposals. If accepted, you don't need to submit it again for next year!
                </p>
              </template>
            </VueTextSection>
          </div>
        </div> -->
        <!-- <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challenge-7" aria-expanded="false" aria-controls="challenge-7">
              I want to submit a challenge for 2024 AND 2025. How does it work? Do I have to submit it again next year?
            </button>
          </h2>
          <div id="challenge-7" class="accordion-collapse collapse" data-bs-parent="#challenge-7">
            <VueTextSection>
              <template #text>
                <p>
                  If you want to submit a proposal for both MICCAI 2024 and 2025, please create two separate proposals
                  and indicate their difference and/or why it is important to run the challenge in both years.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div> -->
      </div>
    </VueTextSection>
    <VueTextSection>
      <template #title>Submit challenge proposals</template>
      <div class="accordion accordion-flush" id="accordionSubmitChallengeProposals">
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#submitProposal-1" aria-expanded="false" aria-controls="#submitProposal-1">
              How can I submit my proposal?
            </button>
          </h2>
          <div id="submitProposal-1" class="accordion-collapse collapse" data-bs-parent="#submitProposal-1">
            <VueTextSection>
              <template #text>
                <p>
                  After completing your challenge proposal, make sure that all changes are saved.
                  Afterwards, click on <button class="my-1 btn btn-primary btn-sm">
                    <i class=" bi bi-send-arrow-down"></i> Generate proposal</button> button on the right panel and
                  follow the
                  instructions. After that you will be able to download your proposal file. Please don't forget to
                  upload
                  it to CMT before deadline.
                </p>
                <p>
                  <span class="text-danger">Remark: </span>You are only able to submit a proposal if
                  you filled out 90% of parameters and created at least one task. Furthermore,
                  submitting after the deadline is not possible.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#submitProposal-2" aria-expanded="false" aria-controls="submitProposal-2">
              I submitted my proposal, what happens next?
            </button>
          </h2>
          <div id="submitProposal-2" class="accordion-collapse collapse" data-bs-parent="#submitProposal-2">
            <VueTextSection>
              <template #text>
                <p>
                  After uploading your proposal to CMT, it will be reviewed by multiple reviewers. Please wait for their
                  feedback. If a revision is required, you will be asked to write a rebuttal based
                  on the feedback. Afterwards, a MICCAI challenge (co-)chair will inform you about
                  the status of your proposal.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#submitProposal-3" aria-expanded="false" aria-controls="submitProposal-3">
              When is the deadline for proposal submission?
            </button>
          </h2>
          <div id="submitProposal-3" class="accordion-collapse collapse" data-bs-parent="#submitProposal-3">
            <VueTextSection>
              <template #text>
                <p>Please see the submission timeline section on welcome page</p>
              </template>
            </VueTextSection>
          </div>
        </div>
      </div>
    </VueTextSection>
    <VueTextSection>
      <template #title>I accidentally ...</template>
      <div class="accordion accordion-flush" id="accordionAccidentally">
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#accidentally-1" aria-expanded="false" aria-controls="#accidentally-1">
              I submitted my proposal by accident, what can I do to get it back for editing?
            </button>
          </h2>
          <div id="accidentally-1" class="accordion-collapse collapse" data-bs-parent="#accidentally-1">
            <VueTextSection>
              <template #text>
                <p>Please contact the technical support.</p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#accidentally-2" aria-expanded="false" aria-controls="accidentally-2">
              I deleted my proposal by accident. Can I get it back?
            </button>
          </h2>
          <div id="accidentally-2" class="accordion-collapse collapse" data-bs-parent="#accidentally-2">
            <VueTextSection>
              <template #text>
                <p>Deleted proposals can not be recovered. Please create a new proposal.</p>
              </template>
            </VueTextSection>
          </div>
        </div>
      </div>
    </VueTextSection>
    <VueTextSection>
      <template #title>Challenge review</template>
      <div class="accordion accordion-flush" id="accordionChallengeReview">
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challengeReview-1" aria-expanded="false" aria-controls="#challengeReview-1">
              How does the review process work?
            </button>
          </h2>
          <div id="challengeReview-1" class="accordion-collapse collapse" data-bs-parent="#challengeReview-1">
            <VueTextSection>
              <template #text>
                <p>
                  Each reviewer will be assigned to one or multiple challenge(s). After they were
                  informed, they have to sign in as reviewers, open the review menu entry and have a
                  careful look at the challenge proposal. They should further use the parameter
                  checklist for their review that can be downloaded from the review view. For their
                  review, they have to answer to a few questions and send their feedback. After all
                  reviews are given, a meta reviewer will have a look at the feedback and the
                  proposal and will take the final decision. In some cases, the meta reviewer might
                  ask the challenge organizers to write a rebuttal on their proposal.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challengeReview-2" aria-expanded="false" aria-controls="challengeReview-2">
              Can I become a reviewer?
            </button>
          </h2>
          <div id="challengeReview-2" class="accordion-collapse collapse" data-bs-parent="#challengeReview-2">
            <VueTextSection>
              <template #text>
                <p>
                  There is a separate call for challenge reviewers. More information can be found on
                  the MICCAI homepage.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
      </div>
    </VueTextSection>
    <VueTextSection>
      <template #title>7 reasons why challenges were rejected</template>
      <div class="accordion accordion-flush" id="accordionChallengeRejectedReasons">
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challengeRejectedReasons-1" aria-expanded="false"
              aria-controls="#challengeRejectedReasons-1">
              1. Small datasets
            </button>
          </h2>
          <div id="challengeRejectedReasons-1" class="accordion-collapse collapse"
            data-bs-parent="#challengeRejectedReasons-1">
            <VueTextSection>
              <template #text>
                <p>
                  The dataset is one of the main components of your challenge. The rankings rely on
                  the dataset as well as the general performance of the participating algorithms. In
                  machine learning, you should try to acquire as much data as possible to avoid poor
                  approximation of the algorithms. Of course, this is tough in the medical domain,
                  but challenges with only very few cases may not attract a lot of researchers which
                  therefore may lead to rejection.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challengeRejectedReasons-2" aria-expanded="false"
              aria-controls="challengeRejectedReasons-2">
              2. Training-test dataset imbalance
            </button>
          </h2>
          <div id="challengeRejectedReasons-2" class="accordion-collapse collapse"
            data-bs-parent="#challengeRejectedReasons-2">
            <VueTextSection>
              <template #text>
                <p>
                  The dataset should reflect the natural variability of the imaged objects. In the
                  best case, it was acquired from multiple sources. The split of the dataset into
                  training and test is very important for the algorithm performances. Be aware that
                  imbalanced training data may lead to worse results. Furthermore, make sure that
                  training and test data share similar distributions, but the test data should also
                  be sufficient to test the generalization capabilities of algorithms.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challengeRejectedReasons-3" aria-expanded="false"
              aria-controls="challengeRejectedReasons-3">
              3. Metric/assessment aim doesn't fit the challenge goal
            </button>
          </h2>
          <div id="challengeRejectedReasons-3" class="accordion-collapse collapse"
            data-bs-parent="#challengeRejectedReasons-3">
            <VueTextSection>
              <template #text>
                <p>
                  The metrics should be well chosen. Don't use a metric because many other
                  researcher are using it without thinking it through. For example, the Dice
                  Similarity metric is very popular in segmentation tasks, but it is not well-suited
                  for small objects to be segmented. Define the goal of your challenge, define
                  assessment aims and find the metrics that fit best. If you are unsure, here are
                  some reads to consider:
                </p>
                <ul>

                  <li>Common Limitations of Image Processing Metrics: A Picture Story</li>
                  <li>
                    A discovery dive into the world of evaluation — Do’s, don’ts and other
                    considerations (blogpost)
                  </li>
                </ul>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challengeRejectedReasons-4" aria-expanded="false"
              aria-controls="challengeRejectedReasons-4">
              4. No statistical or uncertainty analyses
            </button>
          </h2>
          <div id="challengeRejectedReasons-4" class="accordion-collapse collapse"
            data-bs-parent="#challengeRejectedReasons-4">
            <VueTextSection>
              <template #text>
                <p>
                  Organizing a challenge also includes the analysis of results. The algorithm
                  performance should be validated in a thoughtful manner. Is the ranking robust
                  against small perturbations? What would happen to the ranking if you slightly
                  change the test dataset? What would happen if you combine some of the submitted
                  methods? Statistics is important. Don't leave it out. Check out the following
                  links for details:
                </p>
                <ul>
                  <li>
                    Methods and open-source toolkit for analyzing and visualizing challenge results
                    (publication)
                  </li>
                  <li>
                    Open-source toolkit for analyzing and visualizing challenge results (toolkit)
                  </li>
                </ul>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challengeRejectedReasons-5" aria-expanded="false"
              aria-controls="challengeRejectedReasons-5">
              5. Challenge motivation not convincing
            </button>
          </h2>
          <div id="challengeRejectedReasons-5" class="accordion-collapse collapse"
            data-bs-parent="#challengeRejectedReasons-5">
            <VueTextSection>
              <template #text>
                <p>
                  Why do you want to run your challenge? What is your motivation? Are you trying to
                  find algorithms that exceed the current state of the art? Do you try to find
                  solutions for an ill-posed problem? These questions should be pondered thoroughly
                  from beginning.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challengeRejectedReasons-6" aria-expanded="false"
              aria-controls="challengeRejectedReasons-6">
              6. Too little information provided/no justification
            </button>
          </h2>
          <div id="challengeRejectedReasons-6" class="accordion-collapse collapse"
            data-bs-parent="#challengeRejectedReasons-6">
            <VueTextSection>
              <template #text>
                <p>
                  Challenges are validation studies. As such, the design should be completely
                  transparent and design choices should be justified and comprehensible. In the
                  past, challenges were rejected because some design choices were not justified at
                  all or not reproducible. We will present some examples of the most unclear
                  parameters of rejected challenges. As described above, the dataset is highly
                  important. It should be absolutely clear why you chose a specific training/test
                  split. Next, the annotation process is as important as the data. Questions such
                  as: 'Who annotated the data?' 'What was the experience level of annotaters?' 'Did
                  multiple annotators annotate the data?' should be clearly answered as well as a
                  link to the labeling protocol should be provided. Make sure to justify why you
                  chose specific performance metrics. The metric should reflect your challenge goal
                  (see below) and should assess valid properties. Be aware of mutually dependent
                  metrics. The ranking computation should be clear, in the best case, write it in a
                  pseudoalgorithmic form. Make clear why this computation was chosen. How does the
                  submission of results work for the participants? Are they required to generate
                  docker containers? Upload results? Upload code? All these questions are important
                  to know.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#challengeRejectedReasons-7" aria-expanded="false"
              aria-controls="challengeRejectedReasons-7">
              7. Many typos, grammatical errors, incomplete sentences
            </button>
          </h2>
          <div id="challengeRejectedReasons-7" class="accordion-collapse collapse"
            data-bs-parent="#challengeRejectedReasons-7">
            <VueTextSection>
              <template #text>
                <p>
                  Finally, take your best shot when filling out the submission form. We know, it's
                  tough, there are many parameters. But all of them matter. The reviewers will know
                  immediately when you filled the parameters out in a rush. You don't submit a paper
                  full of typos, grammatical errors and incomplete sentences, right? So you also
                  don't want to submit a challenge proposal in such a way.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
      </div>
    </VueTextSection>
    <VueTextSection>
      <template #title>Feedback and questions</template>
      <div class="accordion accordion-flush" id="accordionFeedback">
        <!-- <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#feedback-1" aria-expanded="false" aria-controls="#feedback-1">
              I have a question to the MICCAI organizers. How can I contact them?
            </button>
          </h2>
          <div id="feedback-1" class="accordion-collapse collapse" data-bs-parent="#feedback-1">
            <VueTextSection>
              <template #text>
                <p>Please use our contact form and choose MICCAI challenge chairs as recipient.</p>
              </template>
            </VueTextSection>
          </div>
        </div> -->
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#feedback-2" aria-expanded="false" aria-controls="feedback-2">
              I've found a bug in the system, how can I report it?
            </button>
          </h2>
          <div id="feedback-2" class="accordion-collapse collapse" data-bs-parent="#feedback-2">
            <VueTextSection>
              <template #text>
                <!-- <p>Please contact the technical support as recipient.</p> -->
                <p>Please contact the technical support.</p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#feedback-3" aria-expanded="false" aria-controls="feedback-3">
              Can I give feedback to the submission system?
            </button>
          </h2>
          <div id="feedback-3" class="accordion-collapse collapse" data-bs-parent="#feedback-3">
            <VueTextSection>
              <template #text>
                <!-- <p>Yes. Please use our contact form and choose Technical support as recipient.</p> -->
                <p>Yes. Please contact the technical support.</p>
              </template>
            </VueTextSection>
          </div>
        </div>
      </div>
    </VueTextSection>
    <VueTextSection>
      <template #title>General questions related to the submission system</template>
      <div class="accordion accordion-flush" id="accordionGeneralQuestions">
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#generalQuestions-1" aria-expanded="false" aria-controls="#generalQuestions-1">
              How can I log out?
            </button>
          </h2>
          <div id="generalQuestions-1" class="accordion-collapse collapse" data-bs-parent="#generalQuestions-1">
            <VueTextSection>
              <template #text>
                <p>Click your name on the left panel. Then click the "Sign out" button at the bottom of the pop-up
                  window.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#generalQuestions-2" aria-expanded="false" aria-controls="generalQuestions-2">
              How can I edit my profile?
            </button>
          </h2>
          <div id="generalQuestions-2" class="accordion-collapse collapse" data-bs-parent="#generalQuestions-2">
            <VueTextSection>
              <template #text>
                <p>Click your name on the left panel. Then click the "Edit profile" button.</p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#generalQuestions-3" aria-expanded="false" aria-controls="generalQuestions-3">
              How can I change the view from (e.g.) organizer to reviewer?
            </button>
          </h2>
          <div id="generalQuestions-3" class="accordion-collapse collapse" data-bs-parent="#generalQuestions-3">
            <VueTextSection>
              <template #text>
                <p>
                  If you have been given access to the corresponding role you can change to it by
                  clicking on the account menu button and then selecting change role
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#generalQuestions-4" aria-expanded="false" aria-controls="generalQuestions-4">
              How can I delete my account?
            </button>
          </h2>
          <div id="generalQuestions-4" class="accordion-collapse collapse" data-bs-parent="#generalQuestions-4">
            <VueTextSection>
              <template #text>
                <p>
                  Please contact the technical support. Write a short
                  statement that your account should be deleted.
                </p>
                <p>
                  <span class="text-danger">Please keep in mind</span> that this decision cannot be
                  withdrawn.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#generalQuestions-5" aria-expanded="false" aria-controls="generalQuestions-5">
              I downloaded my proposal, but it differs from my current version. What should I do?
            </button>
          </h2>
          <div id="generalQuestions-5" class="accordion-collapse collapse" data-bs-parent="#generalQuestions-5">
            <VueTextSection>
              <template #text>
                <p>
                  This may happen if you downloaded the proposal in the past. Please clear the cache
                  of your browser and try it again.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#generalQuestions-6" aria-expanded="false" aria-controls="generalQuestions-6">
              Can I link proposals from the ISBI submission system to the MICCAI submission system?
            </button>
          </h2>
          <div id="generalQuestions-6" class="accordion-collapse collapse" data-bs-parent="#generalQuestions-6">
            <VueTextSection>
              <template #text>
                <p>Unfortunately, this is not supported.</p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#generalQuestions-7" aria-expanded="false" aria-controls="generalQuestions-7">
              What does BIAS mean?
            </button>
          </h2>
          <div id="generalQuestions-7" class="accordion-collapse collapse" data-bs-parent="#generalQuestions-7">
            <VueTextSection>
              <template #text>
                <p>
                  The Biomedical Image Analysis ChallengeS (BIAS) statement aims to improve the
                  transparency of the reporting of a biomedical image analysis challenge regardless
                  of field of application, image modality or task category assessed in the
                  challenge. The initiative developed a set of recommendations for the reporting of
                  challenges including checklists for designing and reporting challenges. The
                  submission system is built on those checklists.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
              data-bs-target="#generalQuestions-8" aria-expanded="false" aria-controls="generalQuestions-8">
              My parameters changed after my proposal was accepted. Shall I tell somebody?
            </button>
          </h2>
          <div id="generalQuestions-8" class="accordion-collapse collapse" data-bs-parent="#generalQuestions-8">
            <VueTextSection>
              <template #text>
                <p>
                  Yes, you have to. Please inform the MICCAI challenge chairs. Furthermore, you have
                  to update your challenge proposal within the submission system. Please open the
                  workflow view for details.
                </p>
              </template>
            </VueTextSection>
          </div>
        </div>
      </div>
    </VueTextSection>
  </div>
</template>

<script setup>
import VueTextSection from '@/components/VueTextSection.vue'
</script>

<style scoped></style>
