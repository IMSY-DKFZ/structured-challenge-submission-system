<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-body-tertiary">
        <div class="container-fluid d-flex justify-content-between">
            <button class="navbar-toggler me-auto" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="navbar-brand mx-auto pe-md-0 pe-4 me-md-0 me-5">
                <a v-if="colorStore.isDarkTheme" href="https://www.dkfz.de" target="_blank" class="px-2"><img
                        style="width: auto; height: 23px;" src="@/assets/images/DKFZ_Logo_lightblue.png" alt=""></a>
                <a v-else href="https://www.dkfz.de" target="_blank" class="px-2"><img
                        style="width: auto; height: 23px;" src="@/assets/images/DKFZ_Logo_blue.png" alt=""></a>
                <a v-if="colorStore.isDarkTheme" href="https://helmholtz-imaging.de/" target="_blank" class="px-2"><img
                        style="width: auto; height: 23px; " src="@/assets/images/HI_Logo_small_white.png" alt=""
                        title=""></a>
                <a v-else href="https://helmholtz-imaging.de/" target="_blank" class="px-2"><img
                        style="width: auto; height: 23px; " src="@/assets/images/HI_Logo_small.png" alt="" title=""></a>
            </div>
            <!-- Button for mobile view -->
            <div class="ms-auto mx-auto d-lg-none">
                <router-link v-if="!isSubmissionSystem" :to="{ name: 'SubmissionSystem' }" class="btn btn-primary "
                    role="button">Submission
                    system <i class="bi bi-box-arrow-in-up-right"></i></router-link>
            </div>

            <div class="collapse navbar-collapse flex-column" id="navbarNav">
                <ul class="navbar-nav mx-auto gap-1 gap-lg-2">
                    <li class="nav-item">
                        <router-link :to="{ name: 'Home' }" class="nav-link nav-link-home">Home</router-link>

                    </li>
                    <li class="nav-item">
                        <router-link :to="{ name: 'Bias' }" class="nav-link nav-link-home">Bias</router-link>

                    </li>
                    <li class="nav-item">
                        <router-link :to="{ name: 'News' }" class="nav-link nav-link-home">News/Updates</router-link>

                    </li>
                    <li class="nav-item">
                        <router-link :to="{ name: 'Conferences' }"
                            class="nav-link nav-link-home">Conferences</router-link>

                    </li>
                    <li class="nav-item">
                        <router-link :to="{ name: 'About' }" class="nav-link nav-link-home">About</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link :to="{ name: 'Statistics' }"
                            class="nav-link nav-link-home">Statistics</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link :to="{ name: 'Tips' }" class="nav-link nav-link-home">Tips/Help</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link :to="{ name: 'Team' }" class="nav-link nav-link-home">Team</router-link>
                    </li>
                </ul>
                <ThemeSwitch class="d-lg-none" />
            </div>

            <!-- Button for full view -->
            <router-link v-if="!isSubmissionSystem" :to="{ name: 'SubmissionSystem' }"
                class="btn btn-primary d-none d-lg-inline-block shadow" role="button">Submission
                system <i class="bi bi-box-arrow-in-up-right"></i></router-link>
            <ThemeSwitch class="d-none d-lg-inline-block" />


        </div>
    </nav>
</template>
<script setup>
import ThemeSwitch from '@/components/themeSwitch.vue'
import { useColorStore } from '@/stores/colorMode';
const colorStore = useColorStore();
</script>
<script>
export default {
    name: 'NavBar',
    data() {
        return {
            currentMainRoute: this.$route.matched[0].name
        };
    },
    computed: {
        isSubmissionSystem() {
            return this.currentMainRoute === "SubmissionSystem";
        }
    },
    watch: {
        // Watch route changes to update the button visibility dynamically
        $route(to) {
            this.currentMainRoute = to.matched[0].name;
        }
    }
}


</script>