<template>
  <div>
    <VueTextSection>
      <template #title>Informed consent for registration </template>
      <template #text>
        <div>
          <h4>1. Purpose of collecting and storing personal data</h4>
          <p>
            For your registration on challenge submission system, we need the following
            data: a username, a password and an email address. The latter is necessary to create a
            way to contact you. All other information (full name, institution) is optional. We refer
            to these data as personal data. Challenge proposal data, as defined in the privacy
            policy, includes all challenge design parameters, inserted in challenge proposals. This
            data may contain personal data, depending on what you insert. The parameter (4) Organizs
            will ask you for names, affiliations and email addresses of the organizing committee.
            The names will be published in case of acceptence. By registering to the submission
            system, you agree that you are in charge of the challenge proposal data, making sure,
            that you are allowed to insert potential personal data and that all organizers agree
            that their names will be published.
          </p>
          <h4>2. Deletion of the data</h4>
          <p>
            A withdrawal of the consent is possible at any time and implicates the immediate
            termination of the process, including the deletion of all personal data (please contact
            kontakt@dkfz.de). Your personal data will be deleted at the
            latest after 50 years. Challenge proposals related to your user account, will be
            assigned to the administrators in order to keep challenge data. If you wish to delete
            the challenge data as well, please inform the contact person. I have been advised to
            inform the contact person (part of the challenge proposal data) in case my challenge
            proposals should also be deleted.
          </p>
          <h4>3. Transmission of data to third parties</h4>
          <p>
            Any transfer of my personal and challenge proposal data to third parties as described in
            the Privacy Policy, Section 2 (with the exception of the users described in the Privacy
            Policy, Section 2) may only be carried out with my express consent.
          </p>
          <h4>4. Consequences of non-consent</h4>
          <p>
            If you do not agree to the privacy policy and the data protection policy, no
            registration is possible.
          </p>
          <h4>5. Consent</h4>
          <p>
            I agree to the collection of my personal data as described in Section 1. The consent is
            voluntary and I was informed that registration without consent is not possible. I agree
            that I am allowed to insert potential personal data to the challenge proposal data. The
            personal data are processed exclusively by Administrators as defined in Privacy Policy,
            Section 2, who are required to maintain secrecy. The storing, readout, request and
            similar processing of data is organized by the DKFZ IT infrastructure hosting the
            server.<br />
            I am aware that the 'administrator', 'sub-administrator', 'reviewer' and 'meta-reviewer'
            roles can view and comment on my challenge proposal data (Privacy Policy, Section 2).
            The data are accessed in order to submit, review, process and register challenge
            proposals. The challenge proposal data may also be processed for scientific analyses and
            publications, and for structured access to information on past MICCAI challenges as
            described in Privacy Policy, Section 1 and 2.<br />
            By ticking the checkbox below the data protection policy, I agree that I will be
            registered to the MICCAI 2024 submission tool for biomedical challenges. In addition, I
            agree that my personal and challenge proposal data will be used for the purposes
            described above. Furthermore, I consent that the Administrators (as defined in Privacy
            Policy, Section 2) are allowed to possess and process the challenge proposal data for
            the described purposes.
          </p>
        </div>
      </template>
    </VueTextSection>
  </div>
</template>

<script setup>
import VueTextSection from '@/components/VueTextSection.vue'
</script>
