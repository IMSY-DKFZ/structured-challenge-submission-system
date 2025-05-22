<template>
  <div class="">
    <h1 class="text-center pb-4">Tips and Help - How to organize a successful challenge</h1>
    <p>You want to organize a great challenge but are afraid that it might get rejected? You are new to the field of
      challenges and want to avoid common pitfalls? We collected points that will help you get your challenge accepted!
    </p>
    <h2 class="py-2">1. Complete and transparent reporting</h2>
    <p>Validation studies such as challenges need to be reproducible and interpretable. To achieve this, we recommend
      you to report all important challenge design parameters. Below, you can download the checklist for challenge
      design parameters which can directly be filled out. </p>
    <h2 class="py-2">2. Large dataset sizes</h2>
    <p>The dataset is one of the main components of your challenge. The rankings rely on the dataset as well as the
      general performance of the participating algorithms. In machine learning, you should try to acquire as much data
      as possible to avoid poor approximation of the algorithms. Of course, this is tough in the medical domain, but
      challenges with only very few cases may not attract a lot of researchers which therefore may lead to rejection.
    </p>
    <h2 class="py-2">3. Training-test dataset balance</h2>
    <p>The dataset should reflect the natural variability of the imaged objects. In the best case, it was acquired from
      multiple sources. The split of the dataset into training and test is very important for the algorithm
      performances. Be aware that imbalanced training data may lead to worse results. Furthermore, make sure that
      training and test data share similar distributions, but the test data should also be sufficient to test the
      generalization capabilities of algorithms.</p>
    <h2 class="py-2">4. Metrics/assessment aims reflecting the challenge goal</h2>
    <p>The metrics should be well chosen. Don't use a metric because many other researcher are using it without thinking
      it through. For example, the Dice Similarity metric is very popular in segmentation tasks, but it is not
      well-suited for small objects to be segmented. Define the goal of your challenge, define assessment aims and find
      the metrics that fit best. If you are unsure, here are some reads to consider: </p>
    <ul class="">
      <li><i class="fa fa-angle-double-right"></i><a href="https://arxiv.org/abs/2104.05642" target="_blank">Common
          Limitations of Image
          Processing Metrics: A Picture Story</a></li>
      <li><i class="fa fa-angle-double-right"></i><a
          href="https://medium.com/miccai-educational-initiative/a-discovery-dive-into-the-world-of-evaluation-dos-don-ts-and-other-considerations-4189ab46fe06"
          target="_blank">A
          discovery dive into the world of evaluation — Do’s, don’ts and other considerations (blogpost)</a></li>
      <li><i class="fa fa-angle-double-right"></i><a
          href="https://bmcmedimaging.biomedcentral.com/articles/10.1186/s12880-015-0068-x" target="_blank">Metrics for
          evaluating 3D
          medical image segmentation: analysis, selection, and tool</a></li>

      <p></p>
    </ul>
    <h2 class="py-2">5. Statistical and/or uncertainty analysis</h2>
    <p>Organizing a challenge also includes the analysis of results. The algorithm performance should be validated in a
      thoughtful manner. Is the ranking robust against small perturbations? What would happen to the ranking if you
      slightly change the test dataset? What would happen if you combine some of the submitted methods? Statistics is
      important. Don't leave it out. Check out the following links for details:</p>
    <ul class="">
      <li><i class="fa fa-angle-double-right"></i><a href="https://www.nature.com/articles/s41598-021-82017-6"
          target="_blank">Methods
          and open-source toolkit for analyzing and visualizing challenge results (publication)</a></li>
      <li><i class="fa fa-angle-double-right"></i><a href="https://github.com/wiesenfa/challengeR"
          target="_blank">Open-source toolkit
          for analyzing and visualizing challenge results (toolkit)</a></li>
      <p></p>
    </ul>
    <h2 class="py-2">6. Challenge motivation</h2>
    <p>Why do you want to run your challenge? What is your motivation? Are you trying to find algorithms that exceed the
      current state of the art? Do you try to find solutions for an ill-posed problem? These questions should be
      pondered thoroughly from beginning. </p>
    <h2 class="py-2">7. Details and justification</h2>
    <p>Challenges are validation studies. As such, the design should be completely transparent and design choices should
      be justified and comprehensible. In the past, challenges were rejected because some design choices were not
      justified at all or not reproducible. We will present some examples of the most unclear parameters of rejected
      challenges. As described above, the dataset is highly important. It should be absolutely clear why you chose a
      specific training/test split. Next, the annotation process is as important as the data. Questions such as: 'Who
      annotated the data?' 'What was the experience level of annotaters?' 'Did multiple annotators annotate the data?'
      should be clearly answered as well as a link to the labeling protocol should be provided. Make sure to justify why
      you chose specific performance metrics. The metric should reflect your challenge goal (see below) and should
      assess valid properties. Be aware of mutually dependent metrics. The ranking computation should be clear, in the
      best case, write it in a pseudoalgorithmic form. Make clear why this computation was chosen. How does the
      submission of results work for the participants? Are they required to generate docker containers? Upload results?
      Upload code? All these questions are important to know. </p>
    <h2 class="py-2">8. Avoiding typos, grammatical errors, incomplete sentences</h2>
    <p>Finally, take your best shot when filling out the submission form. We know, it's tough, there are many
      parameters. But all of them matter. The reviewers will know immediately when you filled the parameters out in a
      rush. You don't submit a paper full of typos, grammatical errors and incomplete sentences, right? So you also
      don't want to submit a challenge proposal in such a way. </p>
  </div>
</template>

<script>
export default {
  name: 'TipsPage'
}
</script>
