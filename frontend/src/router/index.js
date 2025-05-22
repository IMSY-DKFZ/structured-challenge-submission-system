import { createRouter, createWebHistory } from 'vue-router'
import EmptyLayout from '../components/layouts/EmptyLayout.vue'
import MainLayout from '../components/layouts/MainLayout.vue'
import HomeLayout from '../components/layouts/HomeLayout.vue'
import { useAuthStore } from '@/stores/auth'


const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomeLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../pages/HomePage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'bias',
        name: 'Bias',
        component: () => import('../pages/BiasPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'news',
        name: 'News',
        component: () => import('../pages/NewsPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'conferences',
        name: 'Conferences',
        component: () => import('../pages/ConferencesPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'overview',
        name: 'Overview',
        component: () => import('../pages/OverviewPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'about',
        name: 'About',
        component: () => import('../pages/AboutPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: () => import('../pages/StatisticsPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'tips',
        name: 'Tips',
        component: () => import('../pages/TipsPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'team',
        name: 'Team',
        component: () => import('../pages/TeamPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'cookies',
        name: 'Usage of cookies',
        component: () => import('../pages/CookiePage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'imprint',
        name: 'Imprint',
        component: () => import('../pages/ImprintPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'data-protection-policy',
        name: 'Data protection policy',
        component: () => import('../pages/DataProtectionPolicyPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'privat-policy',
        name: 'Privacy policy',
        component: () => import('../pages/PrivacyPolicyPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
    ],
  },
  {
    path: '/submission-system',
    name: 'SubmissionSystem',
    redirect: { name: 'Welcome' },
    component: MainLayout,
    meta: {
      requiresAuth: false,
      groupName: 'Main',

    },
    children: [
      //Default Dashboard Pages
      {
        path: '',
        name: 'Welcome',
        component: () => import('../pages/WelcomePage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'workflow',
        name: 'Workflow',
        component: () => import('../pages/proposals/WorkflowPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'faq',
        name: 'FAQ',
        component: () => import('../pages/FAQPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      {
        path: 'contact',
        name: 'Contact',
        component: () => import('../pages/ContactPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },

      //Admin
      {
        path: 'challenges',
        name: 'Challenges',
        component: () => import('../pages/admin/ChallengesPage.vue'),
        meta: {
          access: ['admin', 'subadmin'],
          requiresAuth: true,
          groupName: 'Main',
        },
      },
      {
        path: 'challenges/:id',
        name: 'Challenges Overview',
        component: () => import('../pages/admin/ChallengesPage.vue'),
        meta: {
          access: ['admin', 'subadmin'],
          requiresAuth: true,
          groupName: 'Main',
        },
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('../pages/admin/UsersPage.vue'),
        meta: {
          access: ['admin', 'subadmin'],
          requiresAuth: true,
          groupName: 'Main',
        },
      },
      {
        path: 'users/:id',
        name: 'User Overview',
        component: () => import('../pages/admin/UsersPage.vue'),
        meta: {
          access: ['admin', 'subadmin'],
          requiresAuth: true,
          groupName: 'Main',
        },
      },
      {
        path: 'management',
        name: 'Management',
        component: () => import('../pages/admin/ManagementPage.vue'),
        meta: {
          access: ['admin', 'subadmin'],
          requiresAuth: true,
          groupName: 'Main',
        },
      },
      //Organizer

      {
        path: 'proposals',
        name: 'Proposals',
        component: () => import('../pages/proposals/ProposalsPage.vue'),
        meta: {
          access: ['organizer', 'admin', 'subAdmin'],
          requiresAuth: true,
          groupName: 'Main',
        },
      },
      {
        path: 'new-proposal',
        name: 'New Proposal',
        component: () => import('../pages/proposals/NewProposal.vue'),
        meta: {
          access: ['organizer', 'admin', 'subAdmin'],
          requiresAuth: true,
          groupName: 'Main',
        },
      },
      {
        path: 'edit-proposal/:id',
        name: 'Edit Proposal',
        component: () => import('../pages/proposals/EditProposal.vue'),
        meta: {
          access: ['organizer', 'admin', 'subAdmin'],
          requiresAuth: true,
          groupName: 'Main',
        },
      },

      // {
      //   path: 'overview',
      //   name: 'Overview',
      //   component: () => import('../pages/OverviewPage.vue'),
      //   meta: {
      //     access: [],
      //     requiresAuth: false,
      //     groupName: 'Main',
      //   },
      // },
      {
        path: 'overview/:id',
        name: 'Challenge Overview',
        component: () => import('../pages/ChallengeOverviewPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Main',
        },
      },
      // {
      //   path: 'statistics',
      //   name: 'Statistics',
      //   component: () => import('../pages/StatisticsPage.vue'),
      //   meta: {
      //     access: [],
      //     requiresAuth: false,
      //     groupName: 'Main',
      //   },
      // },

    ],
  },


  {
    path: '/submission-system/auth',
    name: 'authentication',
    redirect: '/submission-system/auth/login',
    component: EmptyLayout,
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('../pages/auth/Login.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Authentications',
        },
      },
      {
        path: 'confirmation',
        name: 'ConfirmationPage',
        component: () => import('../pages/auth/ConfirmationPage.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Authentications',
        },
      },
      {
        path: 'registration',
        name: 'Registration',
        component: () => import('../pages/auth/Registration.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Authentications',
        },
      },
      {
        path: 'reset-password-request',
        name: 'Reset password request',
        component: () => import('../pages/auth/ResetPasswordRequest.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Authentications',
        },
      },
      {
        path: 'reset-password',
        name: 'Reset password',
        component: () => import('../pages/auth/ResetPassword.vue'),
        meta: {
          access: [],
          requiresAuth: false,
          groupName: 'Authentications',
        },
      },
    ],
  },
  {
    path: '/submission-system/profile',
    name: 'profile',
    redirect: '/submission-system/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'User Profile',
        component: () => import('../pages/profile/Profile.vue'),
        meta: {
          access: [],
          groupName: 'Profile',
          requiresAuth: true,
        },
      },
      {
        path: 'edit-profile',
        name: 'Edit profile',
        component: () => import('../pages/profile/EditProfile.vue'),
        meta: {
          access: [],
          groupName: 'Profile',
          requiresAuth: true,
        },
      },
    ],
  },

  {
    // Dynamic route for MICCAI pattern, redirect to "SubmissionSystem"
    path: '/MICCAI:year(.*)',  // The dynamic part of the route with regex to capture the year
    redirect: { name: 'SubmissionSystem' }
  },


  {
    path: '/:catchAll(.*)*',
    redirect: { name: 'Home' },
  },
]

const router = createRouter({
  scrollBehavior: () => ({ left: 0, top: 0 }),
  history: createWebHistory(import.meta.env.BASE_URL),
  base: import.meta.env.BASE_URL,
  routes,
})

router.beforeEach((to, from, next) => {
  const userRole = useAuthStore().getUserRole.toLowerCase()
  const loggedIn = useAuthStore().getUserLoginState

  //CHECK security levels
  // 1.role needed
  // 2.login only
  // 3.public page
  if (to != null && to.meta.access != null && to.meta.access.length > 0) {
    // role is needed
    if (to.meta.access.includes(userRole)) {
      next()
    } else {
      next({ name: 'Login' })
    }
  } else if (to.meta.requiresAuth) {
    // login needed
    if (loggedIn) {
      next()
    } else {
      next({ name: 'Login' })
    }
  } else {
    next()
  }
})
export default router
