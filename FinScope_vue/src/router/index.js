import { createRouter, createWebHistory } from 'vue-router'
import BankMap from '../views/BankMap.vue'
// import Board from '../views/Board.vue' // Old combined board view
import BoardList from '../views/BoardList.vue' // New
import BoardDetail from '../views/BoardDetail.vue' // New
import BoardForm from '../views/BoardForm.vue' // New
import CommoditiesPrice from '../views/CommoditiesPrice.vue'
import DepositPage from '../views/DepositPage.vue'
import Login from '../views/Login.vue'
import MainPage from '../views/MainPage.vue'
// import MyPage from '../views/MyPage.vue'; // Old MyPage
import MyPageLayout from '../views/MyPageLayout.vue'
import ProfileDisplaySection from '../views/mypage/ProfileDisplaySection.vue'
import ProfileEditSection from '../views/mypage/ProfileEditSection.vue'
import UserActivitiesSection from '../views/mypage/UserActivitiesSection.vue'
import SavedProductsSection from '../views/mypage/SavedProductsSection.vue'
import RecommendDeposit from '../views/RecommendDeposit.vue'
import StockInfo from '../views/StockInfo.vue'
import StockSearch from '../views/StockSearch.vue'
import Signup from '../views/Signup.vue'
import NaverLoginCallback from '@/views/NaverLoginCallback.vue'
import NewsDetail from '../views/NewsDetail.vue' // Import the new NewsDetail component
import { useAuthStore } from '@/stores/user'; // Import the auth store

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/bank-map',
      name: 'bank-map',
      component: BankMap,
    },
    {
      path: '/board', // Or '/board/list'
      name: 'board-list',
      component: BoardList,
    },
    {
      path: '/board/detail/:id',
      name: 'board-detail',
      component: BoardDetail,
      props: true, // Pass route params as props
    },
    {
      path: '/board/create',
      name: 'board-create',
      component: BoardForm,
      meta: { requiresAuth: true },
    },
    {
      path: '/board/edit/:id',
      name: 'board-edit',
      component: BoardForm,
      props: true, // Pass route params as props
      meta: { requiresAuth: true },
    },
    {
      path: '/commodities-price',
      name: 'commodities-price',
      component: CommoditiesPrice,
    },
    {
      path: '/deposit-page',
      name: 'deposit-page',
      component: DepositPage,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/',
      name: 'main',
      component: MainPage,
    },
    {
      path: '/my-page',
      component: MyPageLayout,
      meta: { requiresAuth: true },
      redirect: { name: 'my-page-profile' }, // Default redirect for /my-page
      children: [
        {
          path: '', // Default child, effectively /my-page
          name: 'my-page-profile',
          component: ProfileDisplaySection,
        },
        {
          path: 'edit', // /my-page/edit
          name: 'my-page-edit-profile',
          component: ProfileEditSection,
        },
        {
          path: 'activities', // /my-page/activities
          name: 'my-page-activities',
          component: UserActivitiesSection,
        },
        {
          path: 'saved-products', // /my-page/saved-products
          name: 'my-page-saved-products',
          component: SavedProductsSection,
        }
      ]
    },
    {
      path: '/recommend-deposit',
      name: 'recommend-deposit',
      component: RecommendDeposit,
    },
    {
      path: '/stock-info',
      name: 'stock-info',
      component: StockInfo,
    },
    {
      path: '/stock-search',
      name: 'stock-search',
      component: StockSearch,
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isLoggedIn = authStore.isLoggedIn;

  // Define routes that require authentication
  // Define routes that require authentication using meta fields
  // const strictAuthRoutes = ['my-page', 'board-create', 'board-edit']; // Old way

  if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
    // If trying to access a protected route and not logged in,
    // redirect to login page, saving the intended path
    console.log(`Navigation guard: ${to.name} requires auth, user not logged in. Redirecting to login.`);
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else if ((to.name === 'login' || to.name === 'signup') && isLoggedIn) {
    // If trying to access login/signup page but already logged in,
    // redirect to the main page
    next({ name: 'main' });
  } else {
    // Otherwise, allow navigation
    next();
  }
});

export default router
