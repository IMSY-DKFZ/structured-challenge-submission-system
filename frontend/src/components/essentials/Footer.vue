<template>
    <footer class="footer bg-footer mt-auto py-3 text-muted lh-base small ">
        <div class="container footer-text text-left">
            <p class="">This project is being developed within the German Cancer Research Center (DKFZ) divisions of
                <a href="https://www.dkfz.de/en/cami/index.php" target="_blank"
                    class="footer-link link-underline link-underline-opacity-10 link-underline-opacity-0-hover">Intelligent
                    Medical
                    Systems
                    (IMSY)</a>,
                <a href="https://www.dkfz.de/en/mic/index.php" target="_blank"
                    class="footer-link link-underline link-underline-opacity-10 link-underline-opacity-0-hover">Division
                    of Medical Image
                    Computing
                    (MIC)</a> and <a href="https://www.helmholtz-imaging.de/" target="_blank"
                    class="footer-link link-underline link-underline-opacity-10 link-underline-opacity-0-hover">Helmholtz
                    Imaging (HI)</a>. © <span id="year">2024</span>, Copyright German Cancer Research Center. All rights
                reserved.
            </p>

            <p class="text-center">
                <router-link :to="{ name: 'Imprint' }"
                    class="footer-link link-underline link-underline-opacity-10 link-underline-opacity-0-hover px-1">Imprint</router-link>
                •
                <router-link :to="{ name: 'Data protection policy' }"
                    class="footer-link link-underline link-underline-opacity-10 link-underline-opacity-0-hover px-1">Data
                    protection
                    policy</router-link> •
                <router-link :to="{ name: 'Privacy policy' }"
                    class="footer-link link-underline link-underline-opacity-10 link-underline-opacity-0-hover px-1">Privacy
                    policy</router-link> •
                <router-link :to="{ name: 'Usage of cookies' }"
                    class="footer-link link-underline link-underline-opacity-10 link-underline-opacity-0-hover px-1">Usage
                    of
                    cookies</router-link>
            </p>
        </div>


    </footer>
</template>
<script>
export default {
    name: 'Footer',
}


</script>