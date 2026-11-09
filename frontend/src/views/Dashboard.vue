<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Sidebar from '../components/Sidebar.vue';
import Navbar from '../components/Navbar.vue';

// នាំចូលបណ្ណាល័យគូរក្រាហ្វិក
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler } from 'chart.js';
import { Line } from 'vue-chartjs';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler);

const router = useRouter();
const userRole = ref(localStorage.getItem('user_role') || 'admin');
const userName = ref(localStorage.getItem('user_name') || 'Admin');

const isAdmin = computed(() => userRole.value.toLowerCase() === 'admin');
const isCashier = computed(() => userRole.value.toLowerCase() === 'cashier');
const isCustomer = computed(() => userRole.value.toLowerCase() === 'customer');

// អថេរសម្រាប់ផ្ទុកទិន្នន័យពិតពី API
const totalCustomers = ref(0);
const totalVehicles = ref(0);
const totalSpaces = ref(80);
const activeContracts = ref(0);
const pendingPayments = ref(0);
const overduePayments = ref(0);
const monthlyRevenue = ref(0);
const recentPayments = ref([]);
const customersList = ref([]);

const availableSpaces = computed(() => {
  return Math.max(0, totalSpaces.value - totalVehicles.value);
});

const fetchDashboardData = async () => {
  try {
    const token = localStorage.getItem('token');
    const headers = { Authorization: `Bearer ${token}` };

    const [custRes, parkRes, payRes, contractRes] = await Promise.allSettled([
      axios.get('http://127.0.0.1:8000/customers/', { headers }),
      axios.get('http://127.0.0.1:8000/parking/', { headers }),
      axios.get('http://127.0.0.1:8000/payments/', { headers }),
      axios.get('http://127.0.0.1:8000/contracts/', { headers })
    ]);

    if (custRes.status === 'fulfilled') {
      customersList.value = custRes.value.data;
      totalCustomers.value = custRes.value.data.length;
    }

    if (parkRes.status === 'fulfilled') {
      totalVehicles.value = parkRes.value.data.filter(p => !p.check_out_time).length;
    }
    
    if (payRes.status === 'fulfilled') {
      const payData = payRes.value.data;
      const paidInvoices = payData.filter(p => p.status === 'Paid');
      monthlyRevenue.value = paidInvoices.reduce((sum, p) => sum + (p.amount || 0), 0);

      pendingPayments.value = payData.filter(p => p.status === 'Pending').length;
      overduePayments.value = payData.filter(p => p.status === 'Overdue').length;
      recentPayments.value = payData.slice(-5).reverse();
    }

    if (contractRes.status === 'fulfilled') {
      const contracts = contractRes.value.data;
      const active = contracts.filter(c => c.status === 'Active').length;
      activeContracts.value = active > 0 ? active : contracts.length;
    }

  } catch (error) {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      router.push('/login');
    }
  }
};

const getCustomerName = (customerId) => {
  const found = customersList.value.find(c => c.id === customerId);
  return found ? `${found.last_name} ${found.first_name}` : `#CUS-${customerId}`;
};

// ការកំណត់ទិន្នន័យសម្រាប់តារាងក្រាហ្វិក (Line Chart)
const chartData = computed(() => ({
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
  datasets: [
    {
      label: 'Revenue (USD)',
      data: [0, 900, 1300, 1200, 1900, 1800, 2400, 2300, 2500, 2800, monthlyRevenue.value, null],
      borderColor: '#2563eb',
      backgroundColor: 'rgba(37, 99, 235, 0.1)',
      borderWidth: 2,
      pointBackgroundColor: '#2563eb',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: '#2563eb',
      fill: true,
      tension: 0.4
    }
  ]
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: '#f3f4f6', drawBorder: false }
    },
    x: {
      grid: { display: false, drawBorder: false }
    }
  }
};

onMounted(() => {
  fetchDashboardData();
});
</script>

<template>
  <div class="flex h-screen bg-[#f8fafc] font-sans text-gray-800">
    <!-- Reusable Sidebar with Role Differentiation -->
    <Sidebar />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden relative">
      <!-- Reusable Top Navbar -->
      <Navbar title="Dashboard" subtitle="Home / Dashboard" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        
        <!-- ========================================== -->
        <!-- 1. ADMIN ROLE DASHBOARD HEADER & BANNER     -->
        <!-- ========================================== -->
        <div v-if="isAdmin" class="mb-8">
          <div class="bg-gradient-to-r from-purple-900 via-indigo-900 to-slate-900 rounded-3xl p-7 text-white shadow-lg relative overflow-hidden">
            <div class="absolute -right-10 -bottom-10 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl pointer-events-none"></div>
            <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <div class="inline-flex items-center gap-2 px-3 py-1 bg-purple-500/30 text-purple-200 border border-purple-400/30 rounded-full text-xs font-semibold mb-3">
                  <span>👑</span> <span>Administrator Control Center</span>
                </div>
                <h2 class="text-2xl md:text-3xl font-extrabold tracking-tight">សួស្តី Administrator! គ្រប់គ្រងប្រព័ន្ធចំណតទាំងមូល</h2>
                <p class="text-purple-200/80 text-sm mt-1.5 max-w-2xl leading-relaxed">
                  លោកអ្នកមានសិទ្ធិពេញលេញលើការបង្កើត Users, កំណត់ថ្លៃសេវា, ពិនិត្យរបាយការណ៍ចំណូល និងតាមដានសុវត្ថិភាពទូទៅ។
                </p>
              </div>
              <div class="flex flex-wrap items-center gap-3 shrink-0">
                <router-link to="/users" class="px-4 py-2.5 bg-white text-purple-900 hover:bg-purple-50 rounded-xl text-sm font-bold shadow transition-all flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
                  គ្រប់គ្រង Users
                </router-link>
                <router-link to="/reports" class="px-4 py-2.5 bg-purple-800/80 hover:bg-purple-700/80 text-white rounded-xl text-sm font-bold border border-purple-600/40 transition-all flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
                  របាយការណ៍ហិរញ្ញវត្ថុ
                </router-link>
                <router-link to="/settings" class="p-2.5 bg-purple-800/80 hover:bg-purple-700/80 text-white rounded-xl border border-purple-600/40 transition-all" title="Settings">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- ========================================== -->
        <!-- 2. CASHIER ROLE DASHBOARD HEADER & BANNER   -->
        <!-- ========================================== -->
        <div v-else-if="isCashier" class="mb-8">
          <div class="bg-gradient-to-r from-blue-900 via-sky-900 to-indigo-950 rounded-3xl p-7 text-white shadow-lg relative overflow-hidden">
            <div class="absolute -right-10 -bottom-10 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
            <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <div class="inline-flex items-center gap-2 px-3 py-1 bg-blue-500/30 text-blue-200 border border-blue-400/30 rounded-full text-xs font-semibold mb-3">
                  <span>💼</span> <span>Cashier & Operations Desk</span>
                </div>
                <h2 class="text-2xl md:text-3xl font-extrabold tracking-tight">សួស្តីបេឡា! បញ្ជរប្រតិបត្តិការប្រចាំថ្ងៃ</h2>
                <p class="text-blue-200/80 text-sm mt-1.5 max-w-2xl leading-relaxed">
                  គ្រប់គ្រងការចេញចូលយានយន្ត កត់ត្រាការបង់ប្រាក់ ចេញវិក្កយបត្រ KHQR និងតាមដានទីតាំងចំណតទំនេរភ្លាមៗ។
                </p>
              </div>
              <div class="flex flex-wrap items-center gap-3 shrink-0">
                <router-link to="/parking" class="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl text-sm font-bold shadow transition-all flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7h12.5M8 7v8.5A2.5 2.5 0 0010.5 18h3.8M8 7l-4.5 4.5M20.5 7v11M16 11h4.5M16 14.5h4.5" /></svg>
                  + កត់ត្រាយានយន្តចូល/ចេញ
                </router-link>
                <router-link to="/payments" class="px-4 py-2.5 bg-white text-blue-900 hover:bg-blue-50 rounded-xl text-sm font-bold shadow transition-all flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>
                  គិតប្រាក់ (KHQR)
                </router-link>
                <router-link to="/spaces" class="px-4 py-2.5 bg-blue-800/80 hover:bg-blue-700/80 text-white rounded-xl text-sm font-bold border border-blue-600/40 transition-all flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6z" /></svg>
                  មើលចំណតទំនេរ
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- ========================================== -->
        <!-- 3. CUSTOMER ROLE DASHBOARD HEADER & BANNER  -->
        <!-- ========================================== -->
        <div v-else class="mb-8">
          <div class="bg-gradient-to-r from-emerald-900 via-teal-900 to-slate-900 rounded-3xl p-7 text-white shadow-lg relative overflow-hidden">
            <div class="absolute -right-10 -bottom-10 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
            <div class="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <div class="inline-flex items-center gap-2 px-3 py-1 bg-emerald-500/30 text-emerald-200 border border-emerald-400/30 rounded-full text-xs font-semibold mb-3">
                  <span>🚗</span> <span>Customer Self-Service Portal</span>
                </div>
                <h2 class="text-2xl md:text-3xl font-extrabold tracking-tight">សួស្តី {{ userName }}! ផតថលអតិថិជនចំណតរថយន្ត</h2>
                <p class="text-emerald-200/80 text-sm mt-1.5 max-w-2xl leading-relaxed">
                  ពិនិត្យមើលព័ត៌មានកិច្ចសន្យាជួលចំណតប្រចាំខែ ស្ថានភាពទីតាំងចំណត និងបង់ថ្លៃសេវាតាមរយៈ KHQR បានយ៉ាងឆាប់រហ័ស។
                </p>
              </div>
              <div class="flex flex-wrap items-center gap-3 shrink-0">
                <router-link to="/payments" class="px-5 py-2.5 bg-emerald-400 hover:bg-emerald-300 text-slate-900 rounded-xl text-sm font-extrabold shadow-lg transition-all flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>
                  បង់ប្រាក់ KHQR ឥឡូវនេះ
                </router-link>
                <router-link to="/spaces" class="px-4 py-2.5 bg-white/10 hover:bg-white/20 text-white rounded-xl text-sm font-bold border border-white/20 transition-all flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6z" /></svg>
                  ប្លង់ចំណត
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- ======================================================== -->
        <!-- VIEW CONTENT: ADMIN & CASHIER STATS (FULL SYSTEM CARDS)  -->
        <!-- ======================================================== -->
        <template v-if="isAdmin || isCashier">
          <!-- 8 Stat Cards (2 Rows) -->
          <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-6">
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center hover:shadow-md transition-shadow">
              <div>
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">អតិថិជនសរុប (Customers)</p>
                <h3 class="text-3xl font-extrabold text-primary">{{ totalCustomers }}</h3>
              </div>
              <div class="w-12 h-12 bg-green-50 text-success rounded-full flex items-center justify-center">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
              </div>
            </div>
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center hover:shadow-md transition-shadow">
              <div>
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">យានយន្តកំពុងចត (Vehicles)</p>
                <h3 class="text-3xl font-extrabold text-blue-600">{{ totalVehicles }}</h3>
              </div>
              <div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7h12.5M8 7v8.5A2.5 2.5 0 0010.5 18h3.8M8 7l-4.5 4.5M20.5 7v11M16 11h4.5M16 14.5h4.5" /></svg>
              </div>
            </div>
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center hover:shadow-md transition-shadow">
              <div>
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">ចំណតសរុប (Total Spaces)</p>
                <h3 class="text-3xl font-extrabold text-purple-600">{{ totalSpaces }}</h3>
              </div>
              <div class="w-12 h-12 bg-purple-50 text-purple-600 rounded-full flex items-center justify-center font-bold text-xl">P</div>
            </div>
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center hover:shadow-md transition-shadow">
              <div>
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">ចំណតនៅសល់ទំនេរ (Available)</p>
                <h3 class="text-3xl font-extrabold text-emerald-600">{{ availableSpaces }}</h3>
              </div>
              <div class="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center hover:shadow-md transition-shadow">
              <div>
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">កិច្ចសន្យាដំណើរការ (Contracts)</p>
                <h3 class="text-3xl font-extrabold text-amber-500">{{ activeContracts > 0 ? activeContracts : 1 }}</h3>
              </div>
              <div class="w-12 h-12 bg-amber-50 text-amber-500 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
              </div>
            </div>
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center hover:shadow-md transition-shadow">
              <div>
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">រង់ចាំបង់ប្រាក់ (Pending)</p>
                <h3 class="text-3xl font-extrabold text-orange-600">{{ pendingPayments }}</h3>
              </div>
              <div class="w-12 h-12 bg-orange-50 text-orange-600 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
              </div>
            </div>
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center hover:shadow-md transition-shadow">
              <div>
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">ចំណូលប្រចាំខែ (Revenue)</p>
                <h3 class="text-3xl font-extrabold text-primary">${{ monthlyRevenue.toFixed(2) }}</h3>
              </div>
              <div class="w-12 h-12 bg-green-50 text-primary rounded-full flex items-center justify-center font-bold text-xl">$</div>
            </div>
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center hover:shadow-md transition-shadow">
              <div>
                <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">ហួសកាលកំណត់ (Overdue)</p>
                <h3 class="text-3xl font-extrabold text-rose-500">{{ overduePayments }}</h3>
              </div>
              <div class="w-12 h-12 bg-rose-50 text-rose-500 rounded-full flex items-center justify-center">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
              </div>
            </div>
          </div>

          <!-- Chart and Recent Payments Area -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Chart Area (For Admin & Cashier) -->
            <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col">
              <div class="flex justify-between items-start mb-6">
                <div>
                  <h3 class="text-lg font-bold text-gray-800">ចំណូលប្រចាំខែ (Monthly Revenue Overview)</h3>
                  <p class="text-xs text-gray-400 mt-1">ការវិភាគស្ថិតិចំណូលហិរញ្ញវត្ថុប្រចាំឆ្នាំ</p>
                </div>
                <div class="flex items-center gap-2 text-xs font-medium text-gray-600">
                  <span class="w-2.5 h-2.5 rounded-full bg-blue-600"></span> Revenue (USD)
                </div>
              </div>
              <div class="relative flex-1 min-h-[300px]">
                <Line :data="chartData" :options="chartOptions" />
              </div>
            </div>

            <!-- Recent Payments List -->
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col">
              <div class="flex justify-between items-center mb-6">
                <h3 class="text-lg font-bold text-gray-800">ការបង់ប្រាក់ចុងក្រោយ</h3>
                <router-link to="/payments" class="text-primary text-sm font-bold hover:underline">មើលទាំងអស់</router-link>
              </div>
              
              <div class="flex-1">
                <div class="grid grid-cols-4 text-xs font-bold text-gray-400 uppercase tracking-wider mb-4">
                  <div class="col-span-2">អតិថិជន</div>
                  <div>ចំនួនទឹកប្រាក់</div>
                  <div class="text-right">ស្ថានភាព</div>
                </div>
                
                <div class="space-y-4">
                  <div v-for="pay in recentPayments" :key="pay.id" class="grid grid-cols-4 items-center text-sm">
                    <div class="col-span-2 font-medium text-gray-800 truncate pr-2">{{ getCustomerName(pay.customer_id) }}</div>
                    <div class="font-bold text-primary">${{ pay.amount.toFixed(2) }}</div>
                    <div class="text-right">
                      <span class="px-2.5 py-1 bg-green-50 text-green-600 rounded-full text-[10px] font-bold border border-green-100">Paid</span>
                    </div>
                  </div>
                  <div v-if="recentPayments.length === 0" class="text-center text-gray-400 py-4 text-sm">
                    មិនទាន់មានទិន្នន័យបង់ប្រាក់នៅឡើយទេ។
                  </div>
                </div>
              </div>

              <router-link to="/payments" class="mt-6 w-full py-2.5 bg-gray-50 text-gray-700 rounded-xl font-bold text-sm text-center hover:bg-gray-100 transition-colors border border-gray-200">
                + គ្រប់គ្រងការបង់ប្រាក់
              </router-link>
            </div>
          </div>
        </template>

        <!-- ======================================================== -->
        <!-- VIEW CONTENT: CUSTOMER PORTAL (PERSONALIZED USER CARDS) -->
        <!-- ======================================================== -->
        <template v-else>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- 1. My Assigned Space -->
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">ទីតាំងចំណតរបស់អ្នក</span>
                <span class="w-8 h-8 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">🅿️</span>
              </div>
              <h3 class="text-2xl font-extrabold text-emerald-700">Zone A - 05</h3>
              <p class="text-xs text-gray-500 mt-1">ជាន់ផ្ទាល់ដី (Ground Floor - VIP)</p>
              <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs">
                <span class="text-gray-500">ស្ថានភាព៖</span>
                <span class="font-bold text-emerald-600">បានកក់រួចរាល់ (Reserved)</span>
              </div>
            </div>

            <!-- 2. My Contract Status -->
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">កិច្ចសន្យាជួលប្រចាំខែ</span>
                <span class="w-8 h-8 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold">📜</span>
              </div>
              <h3 class="text-2xl font-extrabold text-blue-600">Active (សកម្ម)</h3>
              <p class="text-xs text-gray-500 mt-1">សុពលភាព៖ 30 ថ្ងៃ (បន្តដោយស្វ័យប្រវត្តិ)</p>
              <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs">
                <span class="text-gray-500">កាលបរិច្ឆេទផុតកំណត់៖</span>
                <span class="font-bold text-gray-700">30 វិច្ឆិកា 2026</span>
              </div>
            </div>

            <!-- 3. Monthly Invoice / Fee -->
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">ថ្លៃសេវាប្រចាំខែ</span>
                <span class="w-8 h-8 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center font-bold">$</span>
              </div>
              <h3 class="text-2xl font-extrabold text-primary">$40.00 / ខែ</h3>
              <p class="text-xs text-gray-500 mt-1">កញ្ចប់ Standard Sedan</p>
              <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs">
                <span class="text-gray-500">វិក្កយបត្រខែនេះ៖</span>
                <span class="font-bold text-emerald-600">បានទូទាត់រួច (Paid)</span>
              </div>
            </div>

            <!-- 4. Available Spaces -->
            <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
              <div class="flex items-center justify-between mb-4">
                <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">ចំណតសាធារណៈនៅសល់</span>
                <span class="w-8 h-8 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center font-bold">🚗</span>
              </div>
              <h3 class="text-2xl font-extrabold text-teal-600">{{ availableSpaces }} កន្លែង</h3>
              <p class="text-xs text-gray-500 mt-1">ពីចំណតសរុប {{ totalSpaces }} កន្លែង</p>
              <div class="mt-4 pt-3 border-t border-gray-100 flex items-center justify-between text-xs">
                <span class="text-gray-500">អត្រាចំណតទំនេរ៖</span>
                <span class="font-bold text-teal-700">{{ Math.round((availableSpaces / totalSpaces) * 100) }}% ទំនេរ</span>
              </div>
            </div>
          </div>

          <!-- Customer Detail Cards (Digital Pass & Quick KHQR) -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Digital Member Card / Parking Pass -->
            <div class="bg-gradient-to-br from-slate-900 via-primary to-slate-900 rounded-3xl p-7 text-white shadow-xl relative overflow-hidden flex flex-col justify-between min-h-[260px]">
              <div class="flex justify-between items-start">
                <div>
                  <span class="text-[10px] tracking-widest uppercase font-bold text-emerald-300">Monthly Parking Member Pass</span>
                  <h4 class="text-xl font-black mt-1">CarPark VIP Member</h4>
                </div>
                <div class="w-10 h-10 bg-white/10 rounded-xl flex items-center justify-center font-bold text-emerald-400">P</div>
              </div>

              <div class="my-6">
                <p class="text-xs text-emerald-200/70 uppercase">ផ្លាកលេខយានយន្ត / License Plate</p>
                <p class="text-2xl font-mono font-black tracking-wider text-white mt-1">ភ្នំពេញ 2BP-8899</p>
              </div>

              <div class="flex justify-between items-end pt-4 border-t border-white/10 text-xs">
                <div>
                  <p class="text-[10px] text-emerald-200/60 uppercase">ឈ្មោះម្ចាស់ប័ណ្ណ / Cardholder</p>
                  <p class="font-bold text-sm text-white">{{ userName }}</p>
                </div>
                <div class="text-right">
                  <p class="text-[10px] text-emerald-200/60 uppercase">ទីតាំងចំណត / Slot</p>
                  <p class="font-bold text-sm text-emerald-300 font-mono">Slot A-05</p>
                </div>
              </div>
            </div>

            <!-- Instant KHQR Payment Box -->
            <div class="bg-white rounded-3xl shadow-sm border border-gray-100 p-7 flex flex-col sm:flex-row items-center gap-6">
              <div class="w-40 h-40 bg-red-600 rounded-2xl p-2.5 flex flex-col items-center justify-between text-white shrink-0 shadow-md">
                <div class="text-[10px] font-black tracking-wider uppercase">BAKONG KHQR</div>
                <div class="bg-white p-2 rounded-xl">
                  <!-- Simulated KHQR graphic -->
                  <div class="w-24 h-24 bg-gray-900 flex items-center justify-center rounded">
                    <svg class="w-16 h-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" /></svg>
                  </div>
                </div>
                <div class="text-[9px] font-bold">SCAN TO PAY</div>
              </div>
              <div class="flex-1 text-center sm:text-left">
                <span class="inline-block px-2.5 py-1 bg-red-50 text-red-600 border border-red-200 rounded-full text-xs font-bold mb-2">
                  បង់ប្រាក់រហ័សតាម KHQR
                </span>
                <h4 class="font-extrabold text-lg text-gray-800">ស្កេនទូទាត់ថ្លៃចំណតប្រចាំខែ</h4>
                <p class="text-xs text-gray-500 mt-1 leading-relaxed">
                  លោកអ្នកអាចប្រើប្រាស់ App ធនាគារណាមួយ (ABA, Acleda, Canadia, Wing) ដើម្បីស្កេន និងបង់ប្រាក់បានភ្លាមៗ។
                </p>
                <div class="mt-4 flex items-center gap-3">
                  <router-link to="/payments" class="px-4 py-2 bg-primary hover:bg-emerald-700 text-white rounded-xl text-xs font-bold transition-colors">
                    មើលវិក្កយបត្រទាំងអស់
                  </router-link>
                  <router-link to="/notifications" class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl text-xs font-bold transition-colors">
                    ការជូនដំណឹង
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </template>

      </main>
    </div>
  </div>
</template>
