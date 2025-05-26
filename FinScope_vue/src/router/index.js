import { createRouter, createWebHistory } from 'vue-router'
import BankMap from '../views/BankMap.vue'
import Board from '../views/Board.vue'
import CommoditiesPrice from '../views/CommoditiesPrice.vue'
import DepositPage from '../views/DepositPage.vue'
import Login from '../views/Login.vue'
import MainPage from '../views/MainPage.vue'
import MyPage from '../views/MyPage.vue'
import RecommendDeposit from '../views/RecommendDeposit.vue'
import StockInfo from '../views/StockInfo.vue'
import Signup from '../views/Signup.vue'
import NaverLoginCallback from '@/views/NaverLoginCallback.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/bank-map',
      name: 'bank-map',
      component: BankMap,
    },
    {
      path: '/board',
      name: 'board',
      component: Board,
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
      name: 'my-page',
      component: MyPage,
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
      path: '/signup',
      name: 'signup',
      component: Signup,
    },
    {
      path: '/login/naver/callback',
      name: 'naver-callback',
      component: NaverLoginCallback
    }
  ],
})

export default router
