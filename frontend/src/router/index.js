import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Customers from '../views/Customers.vue'
import Parking from '../views/Parking.vue'
import Payments from '../views/Payments.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', name: 'Login', component: Login },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard },
    { path: '/customers', name: 'Customers', component: Customers },
    { path: '/parking', name: 'Parking', component: Parking },
    { path: '/payments', name: 'Payments', component: Payments }
  ]
})

// ប្រព័ន្ធការពារសុវត្ថិភាព (Navigation Guard)
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  
  // បើអត់មានសោរ (token) ហើយចង់ទៅទំព័រផ្សេងក្រៅពី Login ត្រូវបញ្ជូនទៅ Login វិញ
  if (to.name !== 'Login' && !token) {
    next({ name: 'Login' });
  } 
  // បើមានសោរហើយ តែចង់ទៅទំព័រ Login ម្តងទៀត ត្រូវបញ្ជូនទៅ Dashboard តែម្តង
  else if (to.name === 'Login' && token) {
    next({ name: 'Dashboard' });
  } 
  else {
    next();
  }
});

export default router
