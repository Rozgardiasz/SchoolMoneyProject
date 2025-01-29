import { createRouter, createWebHistory } from 'vue-router';
import LoginScreen from '@/components/LoginPage.vue';
import Home from '@/components/HomePage.vue';
import Register from '@/components/RegisterPage.vue';
import Profile from '@/components/ProfilePage.vue';
import ClassPage from '@/components/ClassPage.vue';
import FoundRisePage from '@/components/FoundRisePage.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginScreen,
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
  },
  {
    path: '/class/:classItem',
    name: 'ClassPage',
    component: ClassPage,
    props: true, // Pozwala na przekazywanie classItem jako props
  },
  {
    path: '/foundrise/:collection',
    name: 'FoundRisePage',
    component: FoundRisePage,
    props: true, // Pozwala na przekazywanie collection jako props
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
