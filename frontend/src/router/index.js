import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Users from '../views/Users.vue'
import Customers from '../views/Customers.vue'
import Parking from '../views/Parking.vue'
import ParkingSpaces from '../views/ParkingSpaces.vue'
import Contracts from '../views/Contracts.vue'
import Payments from '../views/Payments.vue'
import Notifications from '../views/Notifications.vue'
import Reports from '../views/Reports.vue'
import Settings from '../views/Settings.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', name: 'Login', component: Login },
    { path: '/dashboard', name: 'Dashboard', component: Dashboard },
    { path: '/users', name: 'Users', component: Users },
    { path: '/customers', name: 'Customers', component: Customers },
    { path: '/parking', name: 'Parking', component: Parking, alias: '/vehicles' },
    { path: '/spaces', name: 'ParkingSpaces', component: ParkingSpaces, alias: '/parking-spaces' },
    { path: '/contracts', name: 'Contracts', component: Contracts },
    { path: '/payments', name: 'Payments', component: Payments },
    { path: '/notifications', name: 'Notifications', component: Notifications },
    { path: '/reports', name: 'Reports', component: Reports },
    { path: '/settings', name: 'Settings', component: Settings }
  ]
})

// ប្រព័ន្ធការពារសុវត្ថិភាព និងការបែងចែកសិទ្ធិតាម Role (Navigation Guard)
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const role = (localStorage.getItem('user_role') || 'admin').toLowerCase();
  
  // បើអត់មានសោរ (token) ហើយចង់ទៅទំព័រផ្សេងក្រៅពី Login ត្រូវបញ្ជូនទៅ Login វិញ
  if (to.name !== 'Login' && !token) {
    next({ name: 'Login' });
    return;
  } 
  // បើមានសោរហើយ តែចង់ទៅទំព័រ Login ម្តងទៀត ត្រូវបញ្ជូនទៅ Dashboard តែម្តង
  if (to.name === 'Login' && token) {
    next({ name: 'Dashboard' });
    return;
  } 

  // បែងចែកសិទ្ធិប្រើប្រាស់តាម Role ជាក់ស្តែង (RBAC)
  if (role === 'customer') {
    const customerAllowed = ['Login', 'Dashboard', 'ParkingSpaces', 'Contracts', 'Payments', 'Notifications'];
    if (!customerAllowed.includes(to.name)) {
      alert("ទំព័រនេះសម្រាប់តែ Administrator និង Cashier ប៉ុណ្ណោះ!");
      next({ name: 'Dashboard' });
      return;
    }
  } else if (role === 'cashier') {
    const cashierForbidden = ['Users', 'Settings'];
    if (cashierForbidden.includes(to.name)) {
      alert("ទំព័រនេះសម្រាប់តែ Administrator ប៉ុណ្ណោះ!");
      next({ name: 'Dashboard' });
      return;
    }
  }

  next();
});

export default router
