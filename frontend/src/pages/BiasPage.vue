<template>
  <div class="">
    <div>
      <h1 class="text-center pb-4">BIAS Initiative</h1>
      <p>The number of biomedical image analysis challenges organized per year is steadily increasing. Recent research,
        however, revealed that common practice related to challenge reporting does not allow for adequate interpretation
        and reproducibility of results. To address the discrepancy between the impact of challenges and the quality
        (control), the Biomedical Image Analysis ChallengeS (BIAS) initiative developed a set of recommendations for the
        reporting of challenges. The BIAS statement aims to improve the transparency of the reporting of a biomedical
        image analysis challenge regardless of field of application, image modality or task category assessed.</p>
      <p>The <a href="https://doi.org/10.1016/j.media.2020.101796" target="_blank">parameter list</a> which is used to
        create challenge proposals was developed by the BIAS initiative that
        created a guideline on how to report and design challenges in a structured manner. The forms necessary to
        propose a (MICCAI endorsed) challenge can be downloaded below. For details, please check
        <router-link :to="{ name: 'Conferences' }" class="">MICCAI endorsed events(conferences)</router-link> or the
        <router-link :to="{ name: 'Tips' }" class="">Tips/Help</router-link> section.
      </p>
      <p class="text-center">
        <a :href="Suppl_2_StructuredDescriptionOfAChallengeDesignPdf" target="_blank"
          class="btn btn-primary me-3 shadow" type="button">
          <span class=""><i class="bi bi-file-pdf bg-light rounded-1 me-1" style="color:red"></i> Download PDF
            form <i class="bi bi-download"></i></span></a>
        <a :href="Suppl_2_StructuredDescriptionOfAChallengeDesignDocx" target="_blank"
          class="btn btn-primary me-3 shadow" type="button">
          <span class=""><i class="bi bi-file-word bg-light rounded-1 me-1" style="color:blue"></i> Download MS Word
            form <i class="bi bi-download"></i></span></a>

      </p><br>
      <h3>Equator network</h3>
      <p>The Enhancing the QUAlity and Transparency Of health Research (EQUATOR) network is a global initiative with the
        aim of improving the quality of research publications and research itself. A key mission in this context is to
        achieve accurate, complete and transparent reporting of health research studies to support reproducibility and
        usefulness. Between 2006 and 2019, more than 400 reporting guidelines have been published under the umbrella of
        the equator network. A well-known guideline is the <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC32201/"
          target="_blank">CONSORT statement</a> developed for reporting of randomized
        controlled trials. Prominent journals, such as Lancet, JAMA or the British Medical Journal require the CONSORT
        checklist to be submitted along with the actual paper when reporting results of a randomized controlled trial.
      </p>
      <p>The BIAS guideline was registered with the equator network: <a
          href="https://www.equator-network.org/reporting-guidelines/bias-transparent-reporting-of-biomedical-image-analysis-challenges/"
          target="_blank">BIAS: Transparent repoting of biomedical image analysis challenges</a></p><br>
      <h3>BIAS Members</h3>
      <ul class="">
        <li>Lena Maier-Hein (Chair), Annika Reinke, Matthias Eisenmann, Sinan
          Onogur, Annette Kopp-Schneider, DKFZ Heidelberg</li>
        <li>Spyridon Bakas, Perelman School of Medicine, University of
          Pennsylvania</li>
        <li>Michal Kozubek, Masaryk University</li>
        <li>Bennett A. Landman, Vanderbilt University</li>
        <li>Anne L. Martel, Sunnybrook Research Institute; University of Toronto
        </li>
        <li>Tal Arbel, McGill University</li>
        <li>Allan Hanbury, Technische Universität (TU) Wien; Complexity Science
          Hub Vienna</li>
        <li>Pierre Jannin, Université de Rennes 1, Inserm</li>
        <li>Henning Müller, University of Applied Sciences Western Switzerland
          (HES-SO); University of Geneva</li>
        <li>Julio Saez-Rodriguez, Heidelberg University; Heidelberg University
          Hospital; Westfälische Technische Hochschule (RWTH) Aachen</li>
        <li>Bram van Ginneken, Radboud University Medical Center; Fraunhofer
          MEVIS</li>
        <li>Paul Jäger, Fabian Isensee, Jens Petersen, Klaus Maier-Hein, DKFZ
          Heidelberg</li>
        <li>Carole H. Sudre, Michela Antonelli, M. Jorge Cardoso, King's College
          London (KCL); University College London (UCL)</li>
        <li>Veronika Cheplygina, IT University of Copenhagen</li>
        <li>Keyvan Farahani, Ronald M. Summers, National Cancer Institute (NIH)
        </li>
        <li>Ben Glocker, Imperial College London</li>
        <li>Charles E. Kahn, Perelman School of Medicine, University of
          Pennsylvania</li>
        <li>Jens Kleesiek, University Medicine Essen</li>
        <li>Tashin Kurc, Stony Brook University</li>
        <li>Geert Litjens, Radboud University Medical Center</li>
        <li>Bjoern Menze, University of Zurich</li>
        <li>Mauricio Reyes, Bern University Hospital</li>
        <li>Nicola Rieke, NVIDIA; Technical University of Munich (TUM)</li>
        <li>Bram Stieltjes, University Hospital of Basel</li>
        <li>Sotirios A. Tsaftaris, The University of Edinburgh</li>
      </ul>
    </div>
  </div>
</template>
<script>
import Suppl_2_StructuredDescriptionOfAChallengeDesignPdf from '@/assets/Suppl_2_StructuredDescriptionOfAChallengeDesign.pdf';
import Suppl_2_StructuredDescriptionOfAChallengeDesignDocx from '@/assets/Suppl_2_StructuredDescriptionOfAChallengeDesign.docx';

export default {
  name: 'BiasPage',
  data() {
    return {
      Suppl_2_StructuredDescriptionOfAChallengeDesignPdf, Suppl_2_StructuredDescriptionOfAChallengeDesignDocx
    };
  },
};
</script>
