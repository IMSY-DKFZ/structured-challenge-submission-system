<template>
  <div class="col-md-3 col-lg-2 bg-body-tertiary min-vh-md-100">
    <div class="py-3">
      <div class="d-none d-md-block  text-center">
        <router-link class="dropdown-item" :to="{ name: 'About' }"><img alt="logo"
            src="@/assets/images/MICCAI_logo_bkg_1.png" class="card-logo" /></router-link>
        <hr>
        <div v-if="userIsLoggedIn">
          <RoleSwitch />
        </div>
        <div class="d-flex justify-content-center">

          <div class="dropdown d-block pb-3" v-if="userIsLoggedIn">
            <div style="cursor: pointer"
              class="d-flex align-items-center text-decoration-none btn btn-sm btn-primary shadow text-wrap"
              data-bs-toggle="dropdown" aria-expanded="true">
              <div class="py-0">
                {{ userName }} <i class="bi bi-caret-down-fill"></i>
              </div>
            </div>
            <ul class="dropdown-menu shadow" style="position: absolute" data-popper-placement="bottom-end">
              <li>
                <router-link class="dropdown-item" :to="{ name: 'User Profile' }">Profile</router-link>
              </li>
              <li>
                <router-link class="dropdown-item" :to="{ name: 'Edit profile' }">Edit profile</router-link>
              </li>
              <li>
                <hr class="dropdown-divider" />
              </li>
              <li>
                <div>
                  <button type="button" class="btn dropdown-item" @click="logout()">
                    Sign out
                  </button>
                </div>
              </li>
            </ul>
          </div>
          <!-- <div class="dropdown d-block d-md-none" v-if="userIsLoggedIn">
            <div style="cursor: pointer" class="d-flex align-items-center text-decoration-none dropdown-toggle py-1"
              data-bs-toggle="dropdown" aria-expanded="true">
              <div class="py-2">
                {{ userName }}
              </div>
            </div>
            <ul class="dropdown-menu shadow" style="position: absolute" data-popper-placement="bottom-end">
              <li data-bs-toggle="collapse" data-bs-target="#sidebarMenu" aria-controls="sidebarMenu"
                aria-expanded="false" class="nav-item" v-for="(item, idx) in menuUser" :key="idx + item.name">
                <router-link class="dropdown-item" :to="item.to">
                  <div>
                    {{ item.name }}
                  </div>
                </router-link>
                <hr v-if="idx === menuUser.length - 1" class="dropdown-divider" />
                <div v-if="idx === menuUser.length - 1">
                  <button type="button" class="btn dropdown-item" @click="logout()">
                    Sign out
                  </button>
                </div>
              </li>
            </ul>
          </div> -->
          <div v-else class="d-flex justify-content-between my-3 gap-3">
            <router-link :to="{
              name: 'Login',
            }" class="btn btn-outline-success btn-sm"><i class="bi bi-unlock"></i> Login</router-link>
            <router-link :to="{
              name: 'Registration',
            }" class="btn btn-outline-primary btn-sm"><i class="bi bi-person-plus"></i> Registration</router-link>
          </div>
        </div>
      </div>
      <!-- <div v-if="userIsLoggedIn">
        <RoleSwitch />
      </div> -->

      <!--DESKTOP-->
      <div class="d-none d-md-block " v-for="(menu, index) in restrictedMenu" :key="index">
        <ul class="nav flex-column">
          <li class="nav-item pb-2" v-for="(item, idx) in menu.menu" :key="idx">
            <router-link v-if="item.action"
              :class="[isTabActive(item.to) ? 'bg-primary-subtle text-primary-emphasis' : '']"
              class="nav-link py-0 my-0" :to="item.to">
              <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex gap-2 align-items-center" :style="{ color: item.color ? item.color : '' }">
                  <i :class="`bi fs-5 bi-${item.icon}`"></i>
                  <span>
                    {{ item.name }}
                  </span>
                </div>
                <!-- <router-link :to="item.action.to" v-if="proposalNew">
                  <i class="bi fs-5 bi-play-circle"></i>
                </router-link>
                <router-link :to="item.action.to" v-else>
                  <i class="bi fs-5 bi-plus-circle"></i>
                </router-link> -->
              </div>
            </router-link>
            <router-link v-else-if="index === restrictedMenu.length - 1" class="nav-link py-0 my-0" :to="item.to">
              <div class="row g-1 p-0 m-0 link-secondary" style="color: rgb(145, 148, 154)">
                {{ item.name }}
              </div>
            </router-link>
            <router-link v-else class="nav-link py-0"
              :class="[isTabActive(item.to) ? 'bg-primary-subtle text-primary-emphasis' : '']" :to="item.to">
              <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex gap-2 align-items-center" :style="{ color: item.color ? item.color : '' }">
                  <i :class="`bi fs-5 bi-${item.icon}`"></i>
                  <span>
                    {{ item.name }}
                  </span>
                </div>
              </div>
            </router-link>
          </li>
        </ul>
        <!-- <hr /> -->
      </div>

      <!--        MOBILE-->
      <div class="d-block d-md-none" v-for="(menu, index) in restrictedMenu" :key="index">
        <ul class="nav flex-column">
          <li data-bs-toggle="collapse" data-bs-target="#sidebarMenu" aria-controls="sidebarMenu" aria-expanded="false"
            class="nav-item" v-for="(item, idx) in menu.menu" :key="idx">
            <hr v-if="index === restrictedMenu.length - 1 && idx === 0" />

            <router-link v-if="item.action"
              :class="[isTabActive(item.to) ? 'bg-primary-subtle text-primary-emphasis' : '']" class="nav-link"
              :to="item.to">
              <div class="d-flex justify-content-center align-items-center">
                <div class="d-flex gap-2 align-items-center" :style="{ color: item.color ? item.color : '' }">
                  <i :class="`bi fs-5 bi-${item.icon}`"></i>
                  <span>
                    {{ item.name }}
                  </span>
                </div>
                <!-- <router-link :to="item.action.to" v-if="proposalNew">
                  <i class="bi fs-5 bi-play-circle"></i>
                </router-link>
                <router-link :to="item.action.to" v-else>
                  <i class="bi fs-5 bi-plus-circle"></i>
                </router-link> -->
              </div>
            </router-link>
            <router-link v-else-if="index === restrictedMenu.length - 1" class="nav-link" :to="item.to">
              <div class="row g-1 pb-3 link-secondary" style="color: rgb(145, 148, 154)">
                {{ item.name }}
              </div>
            </router-link>
            <router-link v-else class="nav-link"
              :class="[isTabActive(item.to) ? 'bg-primary-subtle text-primary-emphasis' : '']" :to="item.to">
              <div class="d-flex justify-content-center align-items-center">
                <div class="d-flex gap-2 align-items-center" :style="{ color: item.color ? item.color : '' }">
                  <i :class="`bi fs-5 bi-${item.icon}`"></i>
                  <span>
                    {{ item.name }}
                  </span>
                </div>
              </div>
            </router-link>
          </li>
        </ul>
      </div>
      <!-- <div class="p-2 pt-5 d-flex flex-column">
        <a href="https://www.dkfz.de" target="_blank" class="mx-auto d-block"><img style="width: auto; height: 25px;"
            src="@/assets/images/DKFZ_Logo_blue.png" alt=""></a><a href="https://helmholtz-imaging.de/" target="_blank"
          class="mx-auto d-block"><img style="width: auto; height: 25px; " src="@/assets/images/HI_Logo_small.png"
            alt="" title=""></a>
		<a href="https://miccai.org/" target="_blank"
          class="mx-auto d-block"><img style="width: auto; height: 25px; " src="@/assets/images/MICCAI_logo_bkg_1.png"
            alt="" title=""></a>
      </div> -->
      <!-- <div class="p-2 text-muted lh-sm"><small>®Copyright German Cancer Research Center. All rights reserved.</small>

      </div> -->
    </div>
  </div>
</template>

<script>
import { useProposalStore } from '@/stores/proposal'
import { useAuthStore } from '@/stores/auth'
import RoleSwitch from '@/components/user/RoleSwitch.vue'
export default {
  name: 'SideBar',
  components: { RoleSwitch },
  computed: {
    restrictedMenu() {
      return this.menus.filter((x) => {
        if (x.access === '' || x.access.includes(useAuthStore().getUserRole)) {
          return x
        }
      })
    },
    userName() {
      return useAuthStore().getUserName
    },
    userData() {
      return useAuthStore().getUserData
    },
    userIsLoggedIn() {
      return useAuthStore().getUserLoginState
    },
    proposalNew() {
      return useProposalStore().proposalActive
    },
  },
  async mounted() {
    if (useAuthStore().isLoggedIn) {
      await useAuthStore().getAndSetUserDataMe()
    } else if (localStorage.getItem('accessToken')) {
      await useAuthStore().getAndSetUserDataMe()
    } else {
      useAuthStore().clearTokens()
    }
  },
  methods: {
    isTabActive(tab) {
      if (
        this.$route?.fullPath.toLowerCase().includes('/overview') &&
        tab.toLowerCase() === '/submission-system/overview'
      ) {
        return true
      } else if (
        this.$route?.fullPath.toLowerCase().includes('/users') &&
        tab.toLowerCase() === '/submission-system/users'
      ) {
        return true
      } else if (
        this.$route?.fullPath.toLowerCase().includes('/challenges') &&
        tab.toLowerCase() === '/submission-system/challenges'
      ) {
        return true
      } else {
        return this.$route?.fullPath.toLowerCase() === tab.toLowerCase()
      }
    },
    async logout() {
      await useAuthStore().logOutUser()
    },
  },
  data() {
    return {
      menus: [
        {
          access: ['admin', 'subAdmin'],
          menu: [
            { name: 'Challenges', to: '/submission-system/challenges', icon: 'trophy', color: 'red' },
            { name: 'Users', to: '/submission-system/users', icon: 'person-video2', color: 'red' },
            // { name: 'Management', to: '/management', icon: 'gear' },

          ],
        },
        {
          access: ['organizer'],
          menu: [
            {
              name: 'Challenge Proposals',
              to: '/submission-system/proposals',
              action: {
                to: 'new-proposal',
              },
              icon: 'file-earmark-text',
            },

          ],
        },

        {
          access: '',
          menu: [
            { name: 'Welcome', to: '/submission-system/', icon: 'layers-half' },
          ],
        },
        {
          access: '',
          menu: [

            { name: 'Workflow', to: '/submission-system/workflow', icon: 'book' },
          ],
        },
        // {
        //   access: '',
        //   menu: [
        //     { name: 'About', to: '/submission-system/about', icon: 'info-square' },
        //   ],
        // },
        {
          access: '',
          menu: [
            { name: 'FAQ', to: '/submission-system/faq', icon: 'question-square' },
          ],
        },


        // {
        // access: '',
        // menu: [
        // { name: 'About', to: '/', icon: 'info-square' },
        // { name: 'Overview', to: '/overview', icon: 'globe-americas' },
        // { name: 'Statistics', to: '/statistics', icon: 'bar-chart-line' },
        // { name: 'FAQ', to: '/faq', icon: 'question-square' },
        // ],
        // },
        {
          access: '',
          menu: [
            { name: 'Contact', to: '/submission-system/contact', icon: 'envelope-at' },
            // { name: 'Team', to: '/team', icon: 'people' },
          ],
        },
        {
          access: '',
          menu: [
            // { name: 'Imprint', to: '/imprint' },
            // { name: 'Data protection policy', to: '/data-protection-policy' },
            // { name: 'Privacy policy', to: '/privat-policy' },
            // { name: 'Usage of cookies', to: '/cookies' },
          ],
        },
      ],
      menuUser: [
        { name: 'Profile', to: '/submission-system/profile' },
        { name: 'Edit profile', to: '/submission-system/profile/edit-profile' },
      ],
    }
  },
}
</script>

<style scoped></style>
