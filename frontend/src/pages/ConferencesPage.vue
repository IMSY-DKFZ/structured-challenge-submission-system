<template>
  <div class="">
    <div>
      <h1 class="text-center pb-4">Conferences that have used the submission system</h1>
      <p>The submission system is used for the MICCAI conferences since 2018:</p>
      <ul>
        <li>2025: MICCAI</li>
        <li>2025: MICCAI lighthouse challenges</li>
        <li>2024: MICCAI</li>
        <li>2023: MICCAI</li>
        <li>2022: MICCAI</li>
        <li>2021: MICCAI, ISBI</li>
        <li>2020: MICCAI, ISBI, MIDL</li>
        <li>2019: MICCAI</li>
        <li>2018: MICCAI</li>
      </ul>
      <p>Please click the button below to access submission system for current
        applications:</p>
      <p class="text-center"><router-link :to="{ name: 'SubmissionSystem' }"
          class="btn btn-lg btn-primary d-none d-lg-inline-block" role="button">Submission
          system </router-link></p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConferencesPage'
}
</script>