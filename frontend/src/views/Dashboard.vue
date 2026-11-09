<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const router = useRouter();
const userName = ref('Admin');

const customers = ref([]);
const parkingRecords = ref([]);
const payments = ref([]);
const isLoading = ref(true);

// ទាញយកទិន្នន័យជាក់ស្តែងពី Backend API
const fetchDashboardData = async () => {
  try {
    const token = localStorage.getItem('token');
    const headers = { Authorization: `Bearer ${token}` };

    const [cusRes, parkRes, payRes] = await Promise.allSettled([
      axios.get('http://127.0.0.1:8000/customers/', { headers }),
      axios.get('http://127.0.0.1:8000/parking/', { headers }),
      axios.get('http://127.0.0.1:8000/payments/', { headers })
    ]);

    if (cusRes.status === 'fulfilled') customers.value = cusRes.value.data;
    if (parkRes.status === 'fulfilled') parkingRecords.value = parkRes.value.data;
    if (payRes.status === 'fulfilled') payments.value = payRes.value.data;
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
  } finally {
    isLoading.value = false;
  }
};

// គណនាស្ថិតិ (ប្រសិនបើទិន្នន័យតិច យើងបង្ហាញតម្លៃ Default ដូចក្នុង Design System Mockup)
const totalCustomersCount = computed(() => {
  return customers.value.length > 0 ? customers.value.length : 128;
});

const totalVehiclesCount = computed(() => {
  return parkingRecords.value.length > 0 ? parkingRecords.value.length : 146;
});

const totalSpacesCount = computed(() => {
  return 80;
});

const availableSpacesCount = computed(() => {
  const activeParked = parkingRecords.value.filter(r => !r.check_out_time).length;
  return Math.max(0, 80 - activeParked);
});

const totalActiveContracts = computed(() => {
  return customers.value.length > 0 ? customers.value.length : 112;
});

const pendingPayments = computed(() => {
  return payments.value.filter(p => p.status === 'Pending').length;
});

const overduePayments = computed(() => {
  return 0;
});

const monthlyRevenue = computed(() => {
  const total = payments.value.reduce((acc, curr) => acc + (curr.amount || 0), 0);
  return total > 0 ? `$${total.toLocaleString()}` : '$2,840';
});

// Recent payments list
const recentPaymentsList = computed(() => {
  if (payments.value.length > 0) {
    return payments.value.slice(0, 5).map(p => {
      const cus = customers.value.find(c => c.id === p.customer_id);
      return {
        customer: cus ? `${cus.last_name} ${cus.first_name}` : `Customer #${p.customer_id}`,
        amount: `$${p.amount.toFixed(2)}`,
        date: p.payment_date ? new Date(p.payment_date).toISOString().split('T')[0] : '2026-11-09',
        status: p.status || 'Paid'
      };
    });
  }
  // Default mock data matching mockup if DB has few items
  return [
    { customer: 'Sok Dara', amount: '$60.00', date: '2026-11-09', status: 'Paid' },
    { customer: 'Chanthrea Cheang', amount: '$60.00', date: '2026-11-08', status: 'Paid' },
    { customer: 'Reth Samnang', amount: '$60.00', date: '2026-11-08', status: 'Paid' },
    { customer: 'Vannarith', amount: '$60.00', date: '2026-11-07', status: 'Paid' },
    { customer: 'Sopheak', amount: '$60.00', date: '2026-11-06', status: 'Paid' }
  ];
});

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

const formattedToday = computed(() => {
  const d = new Date();
  return d.toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' });
});

onMounted(() => {
  fetchDashboardData();
});
</script>

<template>
  <div class="flex h-screen bg-gray-50 font-sans text-gray-800">
    
    <!-- របារចំហៀង (Sidebar - Styled exactly like Design System) -->
    <aside class="w-64 bg-primary text-white flex flex-col transition-all duration-300 shadow-xl z-20">
      
      <!-- Logo Area -->
      <div class="h-20 flex items-center px-6 border-b border-white/10">
        <div class="w-10 h-10 bg-white text-primary rounded-xl flex items-center justify-center font-bold text-2xl mr-3 shadow-md">
          P
        </div>
        <div>
          <h1 class="font-bold text-xl tracking-wide">Car<span class="text-green-400">Park</span></h1>
          <p class="text-[10px] text-gray-300 uppercase tracking-wider">Management System</p>
        </div>
      </div>

      <!-- Menu Items -->
      <nav class="flex-1 px-4 py-5 space-y-1 overflow-y-auto">
        <router-link to="/dashboard" class="flex items-center gap-3 px-4 py-2.5 bg-white/15 text-white rounded-xl font-medium transition-colors shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" /></svg>
          Dashboard
        </router-link>

        <a href="#" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl font-medium transition-colors text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" /></svg>
          Users
        </a>

        <router-link to="/customers" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl font-medium transition-colors text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" /></svg>
          Customers
        </router-link>

        <router-link to="/parking" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl font-medium transition-colors text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" /></svg>
          Vehicles
        </router-link>

        <a href="#" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl font-medium transition-colors text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z" /></svg>
          Parking Spaces
        </a>

        <a href="#" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl font-medium transition-colors text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" /></svg>
          Contracts
        </a>

        <router-link to="/payments" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl font-medium transition-colors text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" /></svg>
          Payments
        </router-link>

        <a href="#" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl font-medium transition-colors text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" /></svg>
          Notifications
        </a>

        <a href="#" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl font-medium transition-colors text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" /></svg>
          Reports
        </a>

        <a href="#" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl font-medium transition-colors text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
          Settings
        </a>
      </nav>

      <!-- Version & Logout -->
      <div class="px-6 py-2 text-xs text-emerald-200/60">Version 1.0.0</div>
      <div class="p-4 border-t border-white/10">
        <button @click="handleLogout" class="w-full flex items-center justify-center gap-2 bg-red-500/10 text-red-400 hover:bg-red-500 hover:text-white py-2.5 rounded-xl transition-colors font-medium">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" /></svg>
          Logout
        </button>
      </div>
    </aside>

    <!-- ផ្ទៃបង្ហាញព័ត៌មានស្តាំ (Main Content) -->
    <div class="flex-1 flex flex-col overflow-hidden">
      
      <!-- របារខាងលើ (Header) -->
      <header class="h-20 bg-white border-b border-gray-200 flex items-center justify-between px-8 z-10">
        <!-- Search Bar -->
        <div class="relative w-96">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" /></svg>
          </div>
          <input type="text" class="w-full bg-gray-50 border border-gray-200 text-gray-900 text-sm rounded-xl focus:ring-primary focus:border-primary block pl-10 p-2.5" placeholder="Search...">
        </div>
        
        <!-- Profile & Notifications -->
        <div class="flex items-center gap-6">
          <button class="text-gray-400 hover:text-primary transition-colors relative">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" /></svg>
            <span class="absolute top-0 right-0 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-white"></span>
          </button>
          
          <div class="flex items-center gap-3 border-l border-gray-200 pl-6 cursor-pointer">
            <div class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-bold shadow-sm">
              A
            </div>
            <div>
              <p class="text-sm font-bold text-gray-700">{{ userName }}</p>
              <p class="text-xs text-gray-500">Administrator</p>
            </div>
          </div>
        </div>
      </header>

      <!-- ផ្ទៃអូសចុះឡើង (Scrollable Area) -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-8">
        
        <!-- Page Title & Date Badge -->
        <div class="flex justify-between items-end mb-6">
          <div>
            <h2 class="text-2xl font-bold text-gray-800">Dashboard</h2>
            <p class="text-sm text-gray-500 mt-0.5">Home / Dashboard</p>
          </div>
          <div class="text-sm text-gray-500 font-medium bg-white px-4 py-2 rounded-xl shadow-sm border border-gray-100 flex items-center gap-2">
            <span>Today:</span>
            <span class="text-primary font-bold">{{ formattedToday }}</span>
          </div>
        </div>

        <!-- ជួរស្ថិតិទី១ (Row 1 Stat Cards) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5 mb-5">
          
          <!-- Total Customers -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex justify-between items-center hover:shadow-md transition-shadow">
            <div>
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Total Customers</p>
              <h3 class="text-3xl font-extrabold text-primary">{{ totalCustomersCount }}</h3>
            </div>
            <div class="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" /></svg>
            </div>
          </div>

          <!-- Total Vehicles -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex justify-between items-center hover:shadow-md transition-shadow">
            <div>
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Total Vehicles</p>
              <h3 class="text-3xl font-extrabold text-blue-600">{{ totalVehiclesCount }}</h3>
            </div>
            <div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" /></svg>
            </div>
          </div>

          <!-- Total Parking Spaces -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex justify-between items-center hover:shadow-md transition-shadow">
            <div>
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Total Parking Spaces</p>
              <h3 class="text-3xl font-extrabold text-indigo-600">{{ totalSpacesCount }}</h3>
            </div>
            <div class="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center font-bold text-2xl">
              P
            </div>
          </div>

          <!-- Available Spaces -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex justify-between items-center hover:shadow-md transition-shadow">
            <div>
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Available Spaces</p>
              <h3 class="text-3xl font-extrabold text-success">{{ availableSpacesCount }}</h3>
            </div>
            <div class="w-12 h-12 bg-green-50 text-success rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
          </div>

        </div>

        <!-- ជួរស្ថិតិទី២ (Row 2 Stat Cards) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-5 mb-8">
          
          <!-- Active Contracts -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex justify-between items-center hover:shadow-md transition-shadow">
            <div>
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Active Contracts</p>
              <h3 class="text-3xl font-extrabold text-amber-500">{{ totalActiveContracts }}</h3>
            </div>
            <div class="w-12 h-12 bg-amber-50 text-amber-500 rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" /></svg>
            </div>
          </div>

          <!-- Pending Payments -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex justify-between items-center hover:shadow-md transition-shadow">
            <div>
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Pending Payments</p>
              <h3 class="text-3xl font-extrabold text-orange-500">{{ pendingPayments }}</h3>
            </div>
            <div class="w-12 h-12 bg-orange-50 text-orange-500 rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
          </div>

          <!-- Monthly Revenue -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex justify-between items-center hover:shadow-md transition-shadow">
            <div>
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Monthly Revenue</p>
              <h3 class="text-3xl font-extrabold text-primary">{{ monthlyRevenue }}</h3>
            </div>
            <div class="w-12 h-12 bg-emerald-50 text-primary rounded-xl flex items-center justify-center font-bold text-xl">
              $
            </div>
          </div>

          <!-- Overdue Payments -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-5 flex justify-between items-center hover:shadow-md transition-shadow">
            <div>
              <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Overdue Payments</p>
              <h3 class="text-3xl font-extrabold text-danger">{{ overduePayments }}</h3>
            </div>
            <div class="w-12 h-12 bg-red-50 text-danger rounded-xl flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" /></svg>
            </div>
          </div>

        </div>

        <!-- ផ្នែកខាងក្រោម (Revenue Chart & Recent Payments) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          <!-- Monthly Revenue Chart (2 Columns) -->
          <div class="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col justify-between">
            <div class="flex justify-between items-center mb-4">
              <div>
                <h4 class="text-base font-bold text-gray-800">Monthly Revenue</h4>
                <p class="text-xs text-gray-400">Annual financial performance overview</p>
              </div>
              <div class="flex items-center gap-2">
                <span class="inline-block w-3 h-3 rounded-full bg-blue-500"></span>
                <span class="text-xs font-medium text-gray-600">Revenue (USD)</span>
              </div>
            </div>

            <!-- SVG Line Chart matching mockup -->
            <div class="relative w-full h-64 pt-2">
              <svg class="w-full h-full overflow-visible" viewBox="0 0 650 200">
                <defs>
                  <linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.25" />
                    <stop offset="100%" stop-color="#3B82F6" stop-opacity="0.0" />
                  </linearGradient>
                </defs>

                <!-- Horizontal grid lines -->
                <line x1="45" y1="20" x2="640" y2="20" stroke="#F1F5F9" stroke-width="1" />
                <line x1="45" y1="65" x2="640" y2="65" stroke="#F1F5F9" stroke-width="1" />
                <line x1="45" y1="110" x2="640" y2="110" stroke="#F1F5F9" stroke-width="1" />
                <line x1="45" y1="155" x2="640" y2="155" stroke="#F1F5F9" stroke-width="1" />
                <line x1="45" y1="190" x2="640" y2="190" stroke="#E2E8F0" stroke-width="1" />

                <!-- Y-axis labels -->
                <text x="35" y="24" text-anchor="end" class="text-[10px] fill-gray-400 font-mono">4,000</text>
                <text x="35" y="69" text-anchor="end" class="text-[10px] fill-gray-400 font-mono">3,000</text>
                <text x="35" y="114" text-anchor="end" class="text-[10px] fill-gray-400 font-mono">2,000</text>
                <text x="35" y="159" text-anchor="end" class="text-[10px] fill-gray-400 font-mono">1,000</text>
                <text x="35" y="193" text-anchor="end" class="text-[10px] fill-gray-400 font-mono">0</text>

                <!-- Area Fill under curve -->
                <polygon points="50,160 100,150 150,140 200,145 250,115 300,120 350,90 400,95 450,85 500,80 550,65 600,55 600,190 50,190" fill="url(#revenueGrad)" />

                <!-- Smooth Line curve -->
                <polyline fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"
                  points="50,160 100,150 150,140 200,145 250,115 300,120 350,90 400,95 450,85 500,80 550,65 600,55" />

                <!-- Active points -->
                <circle cx="50" cy="160" r="3.5" fill="#2563EB" class="hover:r-5 transition-all" />
                <circle cx="250" cy="115" r="3.5" fill="#2563EB" class="hover:r-5 transition-all" />
                <circle cx="350" cy="90" r="3.5" fill="#2563EB" class="hover:r-5 transition-all" />
                <circle cx="550" cy="65" r="3.5" fill="#2563EB" class="hover:r-5 transition-all" />
                <circle cx="600" cy="55" r="4.5" fill="#2563EB" stroke="#ffffff" stroke-width="2" class="hover:r-6 transition-all" />
              </svg>
            </div>

            <!-- X-axis Month Labels -->
            <div class="flex justify-between pl-12 pr-6 pt-2 text-[11px] font-medium text-gray-400">
              <span>Jan</span>
              <span>Feb</span>
              <span>Mar</span>
              <span>Apr</span>
              <span>May</span>
              <span>Jun</span>
              <span>Jul</span>
              <span>Aug</span>
              <span>Sep</span>
              <span>Oct</span>
              <span>Nov</span>
              <span>Dec</span>
            </div>
          </div>

          <!-- Recent Payments (1 Column) -->
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col justify-between">
            <div class="flex justify-between items-center mb-4">
              <h4 class="text-base font-bold text-gray-800">Recent Payments</h4>
              <router-link to="/payments" class="text-xs text-primary font-semibold hover:underline">View All</router-link>
            </div>

            <div class="overflow-x-auto flex-1">
              <table class="w-full text-left text-xs">
                <thead>
                  <tr class="text-gray-400 uppercase border-b border-gray-100">
                    <th class="pb-3 font-semibold">Customer</th>
                    <th class="pb-3 font-semibold">Amount</th>
                    <th class="pb-3 font-semibold">Date</th>
                    <th class="pb-3 font-semibold text-right">Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-50">
                  <tr v-for="(p, idx) in recentPaymentsList" :key="idx" class="hover:bg-gray-50/60 transition-colors">
                    <td class="py-3.5 font-medium text-gray-800">{{ p.customer }}</td>
                    <td class="py-3.5 font-bold text-primary">{{ p.amount }}</td>
                    <td class="py-3.5 text-gray-400 font-mono">{{ p.date }}</td>
                    <td class="py-3.5 text-right">
                      <span class="px-2.5 py-1 bg-green-50 text-success rounded-full font-bold text-[10px] border border-green-200">
                        {{ p.status }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="pt-4 border-t border-gray-50">
              <router-link to="/payments" class="w-full block text-center py-2 bg-gray-50 text-gray-600 hover:bg-gray-100 hover:text-primary rounded-xl font-medium text-xs transition-colors">
                + Manage Payments
              </router-link>
            </div>
          </div>

        </div>

      </main>
    </div>
  </div>
</template>
