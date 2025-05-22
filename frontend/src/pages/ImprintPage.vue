<template>
  <div>
    <VueTextSection>
      <template #title>This website is hosted by</template>
      <template #text>
        Deutsches Krebsforschungszentrum (German Cancer Research Center, DKFZ)
      </template>
      <div class="bg-info p-3">
        <img src="@/assets/images/dkfz.png" style="max-width: 15rem" alt="" />
      </div>
    </VueTextSection>
    <VueTextSection>
      <template #title>Address</template>
      <template #text>
        <div>
          Deutsches Krebsforschungszentrum <br />
          Im Neuenheimer Feld 280 <br />
          D-69120 Heidelberg <br />
          Germany
        </div>
      </template>
    </VueTextSection>
    <VueTextSection>
      <template #title>Legal Form</template>
      <template #text>
        <div>
          Deutsches Krebsforschungszentrum<br />
          Stiftung des öffentlichen Rechts (Foundation under Public Law)<br />
          Value added tax identification number: DE 143293537
        </div>
      </template>
    </VueTextSection>
    <VueTextSection>
      <template #title>Responsible for site content</template>
      <template #text>
        <div>
          Prof. Dr. Lena Maier-Hein<br />
          Head of Div. Computer Assisted Medical Interventions<br />
          German Cancer Research Center (DKFZ)<br />
          Im Neuenheimer Feld 223<br />
          D-69120 Heidelberg<br />
          Germany<br />
          E-mail: kontakt@dkfz.de
        </div>
      </template>
    </VueTextSection>
    <VueTextSection>
      <template #title>Name and address of the Data Protection Officer</template>
      <template #text>
        <div>
          Data Protection Officer<br />
          German Cancer Research Center - Foundation under public law<br />
          Im Neuenheimer Feld 280<br />
          69120 Heidelberg<br />
          Germany<br />
          Telephone: +49 (0)6221 420<br />
          Email: datenschutz@dkfz.de
        </div>
      </template>
    </VueTextSection>
    <VueTextSection>
      <template #title>Copyright:</template>
      <template #text>
        <div>Copyright German Cancer Research Center. All rights reserved.</div>
      </template>
    </VueTextSection>
    <VueTextSection>
      <template #title>Disclaimer</template>
      <template #text>
        <div>
          This website offers information about biomedical challenge proposals. Our goal is to keep
          this information up to date and accurate. If errors are brought to our attention, we will
          try to correct them. However, we accept no responsibility or liability whatsoever with
          regard to the material on this site. This material is:<br />
          <ul>
            <li>
              Information of a general nature only, not intended to address the specific
              circumstances of any particular individual or entity
            </li>
            <li>Not necessarily comprehensive, complete, accurate or up to date</li>
            <li>
              Not professional or medical advice (if you need specific advice, you should always
              consult a suitably qualified professional).
            </li>
          </ul>
          This disclaimer is not intended to contravene any requirements laid down in applicable
          national law nor to exclude liability for matters which may not be excluded under that
          law.
        </div>
      </template>
    </VueTextSection>
    <VueTextSection>
      <template #title>Data Protection Provisions</template>
      <template #text>
        <div>
          <p>
            The DKFZ is committed to protecting the privacy of all persons using its website and to
            treat any personal information provided in strictest confidence. The data are used
            exclusively for the purposes indicated and not disclosed to third parties (other than
            those specified above). Your data will be deleted as soon as they have served the
            purpose indicated but not later than in 2068. Without your knowledge, your web browser
            or client software may transfer information about your computer (for example IP address)
            to our server. Such information is never brought directly in touch with you, but is
            evaluated in anonymous form for statistical purposes, for system management or to
            improve performance of our internet service.
          </p>
        </div>
      </template>
    </VueTextSection>
  </div>
</template>

<script setup>
import VueTextSection from '@/components/VueTextSection.vue'
</script>
