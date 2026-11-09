<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
// នាំចូលបណ្ណាល័យគូរក្រាហ្វិក
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler } from 'chart.js';
import { Line } from 'vue-chartjs';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler);

const router = useRouter();
const userName = ref('Admin');

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

    // ទាញទិន្នន័យព្រមគ្នាទាំង ៤ (Customers, Parking, Payments, Contracts)
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
      // រាប់ចំនួនឡានដែលកំពុងចត (អត់ទាន់មានម៉ោងចេញ)
      totalVehicles.value = parkRes.value.data.filter(p => !p.check_out_time).length;
    }
    
    if (payRes.status === 'fulfilled') {
      const payData = payRes.value.data;
      // បូកសរុបចំណូល (យកតែវិក្កយបត្រដែល Paid)
      const paidInvoices = payData.filter(p => p.status === 'Paid');
      monthlyRevenue.value = paidInvoices.reduce((sum, p) => sum + (p.amount || 0), 0);

      // រាប់វិក្កយបត្រ Pending និង Overdue
      pendingPayments.value = payData.filter(p => p.status === 'Pending').length;
      overduePayments.value = payData.filter(p => p.status === 'Overdue').length;

      // យកប្រវត្តិបង់ប្រាក់ ៥ ចុងក្រោយ
      recentPayments.value = payData.slice(-5).reverse();
    }

    if (contractRes.status === 'fulfilled') {
      const contracts = contractRes.value.data;
      const active = contracts.filter(c => c.status === 'Active').length;
      activeContracts.value = active > 0 ? active : contracts.length;
    }

  } catch (error) {
    if (error.response && error.response.status === 401) {
      handleLogout();
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
      // ទិន្នន័យក្លែងក្លាយសម្រាប់ខែមុនៗ + ទិន្នន័យពិតប្រចាំខែនេះនៅខែ Nov
      data: [0, 900, 1300, 1200, 1900, 1800, 2400, 2300, 2500, 2800, monthlyRevenue.value, null],
      borderColor: '#2563eb', // ពណ៌ខៀវ
      backgroundColor: 'rgba(37, 99, 235, 0.1)',
      borderWidth: 2,
      pointBackgroundColor: '#2563eb',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: '#2563eb',
      fill: true,
      tension: 0.4 // ធ្វើឲ្យខ្សែកោងស្អាត
    }
  ]
}));

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false } // លាក់ Legend ដើម្បីឲ្យស្រឡះ
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

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  return new Date(dateString).toISOString().split('T')[0];
};

onMounted(() => {
  fetchDashboardData();
});
</script>

<template>
  <div class="flex h-screen bg-[#f8fafc] font-sans text-gray-800">
    
    <!-- Sidebar ដិតពណ៌បៃតង -->
    <aside class="w-[260px] bg-primary text-white flex flex-col transition-all duration-300 z-20">
      <div class="h-20 flex items-center px-6">
        <div class="w-10 h-10 bg-white text-primary rounded-xl flex items-center justify-center font-bold text-2xl mr-3 shadow-md">P</div>
        <div>
          <h1 class="font-bold text-xl tracking-wide">Car<span class="text-green-400">Park</span></h1>
          <p class="text-[9px] text-gray-300 uppercase tracking-wider font-medium">Management System</p>
        </div>
      </div>
      
      <nav class="flex-1 px-4 py-4 space-y-1.5 overflow-y-auto mt-4 text-sm font-medium">
        <router-link to="/dashboard" class="flex items-center gap-3 px-4 py-3 bg-white/10 text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
          Dashboard
        </router-link>
        <a href="#" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
          Users
        </a>
        <router-link to="/customers" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
          Customers
        </router-link>
        <router-link to="/parking" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7h12.5M8 7v8.5A2.5 2.5 0 0010.5 18h3.8M8 7l-4.5 4.5M20.5 7v11M16 11h4.5M16 14.5h4.5" /></svg>
          Vehicles
        </router-link>
        <a href="#" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
          Parking Spaces
        </a>
        <router-link to="/contracts" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
          Contracts
        </router-link>
        <router-link to="/payments" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>
          Payments
        </router-link>
        <a href="#" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
          Notifications
        </a>
        <a href="#" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
          Reports
        </a>
        <a href="#" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
          Settings
        </a>
      </nav>
      
      <div class="p-6">
        <p class="text-[10px] text-primary-300 mb-4 opacity-60">Version 1.0.0</p>
        <button @click="handleLogout" class="w-full flex items-center gap-2 text-red-400 hover:text-red-300 transition-colors font-medium text-sm">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          Logout
        </button>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden relative">
      
      <!-- Top Header -->
      <header class="h-20 bg-white border-b border-gray-100 flex items-center justify-between px-8 z-10">
        <div class="relative w-96">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
          </div>
          <input type="text" class="w-full bg-white border border-gray-200 text-gray-900 text-sm rounded-full focus:ring-primary focus:border-primary block pl-10 py-2.5 transition-shadow" placeholder="Search...">
        </div>
        
        <div class="flex items-center gap-6">
          <button class="text-gray-400 hover:text-primary transition-colors relative">
            <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
            <span class="absolute 1 top-0 right-0 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
          
          <div class="flex items-center gap-3 cursor-pointer">
            <div class="w-9 h-9 rounded-full bg-primary text-white flex items-center justify-center font-bold text-sm shadow-sm">A</div>
            <div>
              <p class="text-sm font-bold text-gray-800 leading-tight">{{ userName }}</p>
              <p class="text-xs text-gray-500">Administrator</p>
            </div>
          </div>
        </div>
      </header>

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        
        <!-- Title & Date -->
        <div class="flex justify-between items-end mb-8">
          <div>
            <h2 class="text-2xl font-bold text-gray-800">Dashboard</h2>
            <p class="text-sm text-gray-500 mt-1">Home / Dashboard</p>
          </div>
          <div class="text-sm font-medium bg-white px-4 py-2 rounded-full shadow-sm border border-gray-100 text-gray-500">
            Today: <span class="text-primary font-bold">Nov 09, 2026</span>
          </div>
        </div>

        <!-- 8 Stat Cards (2 Rows) -->
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-6">
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center">
            <div>
              <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Total Customers</p>
              <h3 class="text-3xl font-bold text-primary">{{ totalCustomers }}</h3>
            </div>
            <div class="w-12 h-12 bg-green-50 text-success rounded-full flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
            </div>
          </div>
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center">
            <div>
              <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Total Vehicles</p>
              <h3 class="text-3xl font-bold text-blue-600">{{ totalVehicles }}</h3>
            </div>
            <div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7h12.5M8 7v8.5A2.5 2.5 0 0010.5 18h3.8M8 7l-4.5 4.5M20.5 7v11M16 11h4.5M16 14.5h4.5" /></svg>
            </div>
          </div>
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center">
            <div>
              <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Total Parking Spaces</p>
              <h3 class="text-3xl font-bold text-purple-600">{{ totalSpaces }}</h3>
            </div>
            <div class="w-12 h-12 bg-purple-50 text-purple-600 rounded-full flex items-center justify-center font-bold text-xl">P</div>
          </div>
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center">
            <div>
              <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Available Spaces</p>
              <h3 class="text-3xl font-bold text-green-500">{{ availableSpaces }}</h3>
            </div>
            <div class="w-12 h-12 bg-green-50 text-green-500 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center">
            <div>
              <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Active Contracts</p>
              <h3 class="text-3xl font-bold text-orange-500">{{ activeContracts > 0 ? activeContracts : 1 }}</h3>
            </div>
            <div class="w-12 h-12 bg-orange-50 text-orange-500 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            </div>
          </div>
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center">
            <div>
              <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Pending Payments</p>
              <h3 class="text-3xl font-bold text-orange-600">{{ pendingPayments }}</h3>
            </div>
            <div class="w-12 h-12 bg-orange-50 text-orange-600 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
          </div>
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center">
            <div>
              <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Monthly Revenue</p>
              <h3 class="text-3xl font-bold text-primary">${{ monthlyRevenue.toFixed(2) }}</h3>
            </div>
            <div class="w-12 h-12 bg-green-50 text-primary rounded-full flex items-center justify-center font-bold text-xl">$</div>
          </div>
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex justify-between items-center">
            <div>
              <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Overdue Payments</p>
              <h3 class="text-3xl font-bold text-red-500">{{ overduePayments }}</h3>
            </div>
            <div class="w-12 h-12 bg-red-50 text-red-500 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            </div>
          </div>
        </div>

        <!-- Chart and Recent Payments Area -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          <!-- Chart Area -->
          <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col">
            <div class="flex justify-between items-start mb-6">
              <div>
                <h3 class="text-lg font-bold text-gray-800">Monthly Revenue</h3>
                <p class="text-xs text-gray-400 mt-1">Annual financial performance overview</p>
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
              <h3 class="text-lg font-bold text-gray-800">Recent Payments</h3>
              <router-link to="/payments" class="text-primary text-sm font-bold hover:underline">View All</router-link>
            </div>
            
            <div class="flex-1">
              <div class="grid grid-cols-4 text-xs font-bold text-gray-400 uppercase tracking-wider mb-4">
                <div class="col-span-2">Customer</div>
                <div>Amount</div>
                <div class="text-right">Status</div>
              </div>
              
              <div class="space-y-4">
                <div v-for="pay in recentPayments" :key="pay.id" class="grid grid-cols-4 items-center text-sm">
                  <div class="col-span-2 font-medium text-gray-800">{{ getCustomerName(pay.customer_id) }}</div>
                  <div class="font-bold text-primary">${{ pay.amount.toFixed(2) }}</div>
                  <div class="text-right">
                    <span class="px-2.5 py-1 bg-green-50 text-green-600 rounded-full text-[10px] font-bold border border-green-100">Paid</span>
                  </div>
                </div>
                <div v-if="recentPayments.length === 0" class="text-center text-gray-400 py-4 text-sm">
                  No recent payments found.
                </div>
              </div>
            </div>

            <router-link to="/payments" class="mt-6 w-full py-2.5 bg-gray-50 text-gray-600 rounded-xl font-bold text-sm text-center hover:bg-gray-100 transition-colors border border-gray-200">
              + Manage Payments
            </router-link>
          </div>
          
        </div>

      </main>
    </div>
  </div>
</template>
