import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './views/HomeView.vue';
import PostFeed from './components/PostFeed.vue';
import PostDetailsComponent from './components/PostDetailsComponent.vue';
import CreatePostComponent from './components/CreatePostComponent.vue';
import UpdatePostComponent from './components/UpdatePostComponent.vue';
import ProtectedResource from './components/ProtectedResource.vue';
import AccountDetailsComponent from './components/AccountDetailsComponent.vue';
import SessionExpiredModal from './components/SessionExpiredModal.vue';
import Test401Component from './components/Test401Component.vue';
import LoginComponent from './components/LoginComponent.vue'; // Adjust path if necessary
import RegisterComponent from './components/RegisterComponent.vue'; 

const routes = [
  { path: '/', component: HomeView },
  { path: '/signin', component: LoginComponent },
  { path: '/signup', component: RegisterComponent },
  { path: '/post-feed', name: 'PostFeed', component: PostFeed },
  { path: '/posts/:id', name: 'PostDetails', component: PostDetailsComponent, props: true },
  { path: '/create', name: 'CreatePost', component: CreatePostComponent },
  { path: '/update/:id', name: 'UpdatePost', component: UpdatePostComponent, props: true },
  { path: '/protected-resource', name: 'ProtectedResource', component: ProtectedResource },
  { path: '/account', name: 'AccountDetails', component: AccountDetailsComponent },
  { path: '/session-expired', name: 'SessionExpired', component: SessionExpiredModal },
  { path: '/test-401', name: 'Test401', component: Test401Component } // Added route for Test401Component
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
