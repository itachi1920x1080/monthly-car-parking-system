<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const userName = ref('Admin');
const isLoading = ref(true);

// ទិន្នន័យពិតពី API
const payments = ref([]);
const parkingRecords = ref([]);
const contracts = ref([]);
const customers = ref([]);

// ឈ្មោះខែជាភាសាខ្មែរ
const khmerMonths = [
  'មករា', 'កុម្ភៈ', 'មីនា', 'មេសា', 'ឧសភា', 'មិថុនា',
  'កក្កដា', 'សីហា', 'កញ្ញា', 'តុលា', 'វិច្ឆិកា', 'ធ្នូ'
];

// ទាញយកទិន្នន័យពី Backend APIs
const fetchReportsData = async () => {
  isLoading.value = true;
  try {
    const token = localStorage.getItem('token');
    const headers = { Authorization: `Bearer ${token}` };

    const [payRes, parkRes, contractRes, custRes] = await Promise.allSettled([
      axios.get('http://127.0.0.1:8000/payments/', { headers }),
      axios.get('http://127.0.0.1:8000/parking/', { headers }),
      axios.get('http://127.0.0.1:8000/contracts/', { headers }),
      axios.get('http://127.0.0.1:8000/customers/', { headers })
    ]);

    if (payRes.status === 'fulfilled') payments.value = payRes.value.data;
    if (parkRes.status === 'fulfilled') parkingRecords.value = parkRes.value.data;
    if (contractRes.status === 'fulfilled') contracts.value = contractRes.value.data;
    if (custRes.status === 'fulfilled') customers.value = custRes.value.data;

  } catch (error) {
    if (error.response && error.response.status === 401) {
      handleLogout();
    }
  } finally {
    isLoading.value = false;
  }
};

// ស្វែងរកឈ្មោះអតិថិជនតាម ID
const getCustomerName = (customerId) => {
  const found = customers.value.find(c => c.id === customerId);
  return found ? `${found.last_name} ${found.first_name}` : `#CUS-${customerId}`;
};

// ស្ថិតិរួមសរុប (Summary Metrics) គណនាពីទិន្នន័យពិត
const summary = computed(() => {
  // ចំណូលសរុបពីវិក្កយបត្រ Paid
  const paidList = payments.value.filter(p => p.status === 'Paid');
  const totalRevenue = paidList.reduce((sum, p) => sum + (p.amount || 0), 0);

  // ចំនួនរថយន្តបានបម្រើសរុប
  const totalVehiclesServiced = parkingRecords.value.length;

  // រយៈពេលចតមធ្យម
  const completed = parkingRecords.value.filter(p => p.check_out_time && p.check_in_time);
  let averageDuration = '0 ម៉ោង';
  if (completed.length > 0) {
    const totalMs = completed.reduce((sum, p) => {
      return sum + (new Date(p.check_out_time) - new Date(p.check_in_time));
    }, 0);
    const avgHours = (totalMs / completed.length / (1000 * 60 * 60)).toFixed(1);
    averageDuration = `${avgHours} ម៉ោង`;
  } else if (parkingRecords.value.length > 0) {
    averageDuration = 'កំពុងចត';
  }

  // កិច្ចសន្យាសកម្ម
  const activeLeases = contracts.value.filter(c => c.status === 'Active').length;

  return {
    totalRevenue,
    totalVehiclesServiced,
    averageDuration,
    activeLeases: activeLeases > 0 ? activeLeases : contracts.value.length
  };
});

// របាយការណ៍ប្រចាំខែ (Monthly Reports Breakdown) គណនាជាក់ស្តែង
const monthlyReports = computed(() => {
  const currentYear = new Date().getFullYear();
  const currentMonthIdx = new Date().getMonth(); // 0-based: 10 = Nov

  const reports = [];

  // បង្កើតតារាងពីខែបច្ចុប្បន្នថយក្រោយទៅខែមករា
  for (let m = currentMonthIdx; m >= 0; m--) {
    const monthName = `${khmerMonths[m]} ${currentYear}`;
    
    // ចំណូលក្នុងខែនេះ
    const monthPayments = payments.value.filter(p => {
      if (!p.payment_date) return false;
      const d = new Date(p.payment_date);
      return d.getFullYear() === currentYear && d.getMonth() === m && p.status === 'Paid';
    });
    const revenue = monthPayments.reduce((sum, p) => sum + (p.amount || 0), 0);

    // ចំនួនឡានចតក្នុងខែនេះ
    const monthParkings = parkingRecords.value.filter(p => {
      if (!p.check_in_time) return false;
      const d = new Date(p.check_in_time);
      return d.getFullYear() === currentYear && d.getMonth() === m;
    });

    // ចំនួនកិច្ចសន្យាក្នុងខែនេះ
    const monthContracts = contracts.value.filter(c => {
      if (!c.start_date) return false;
      const d = new Date(c.start_date);
      return d.getFullYear() === currentYear && d.getMonth() === m;
    });

    reports.push({
      month: monthName,
      revenue: revenue,
      parkings: monthParkings.length,
      contracts: monthContracts.length,
      status: m === currentMonthIdx ? 'កំពុងដំណើរការ' : 'បានបញ្ចប់'
    });
  }

  return reports;
});

// ទាញយករបាយការណ៍ជា Excel (CSV) ជាមួយ UTF-8 BOM
const exportReport = () => {
  if (monthlyReports.value.length === 0 && payments.value.length === 0) {
    alert("មិនមានទិន្នន័យសម្រាប់ទាញយកទេ!");
    return;
  }

  let csv = "របាយការណ៍ហិរញ្ញវត្ថុ និងចំណតរថយន្ត CarPark\n\n";
  
  // ១. តារាងសង្ខេបប្រចាំខែ
  csv += "ខែ/ឆ្នាំ,ចំណូលសរុប (USD),ចំនួនរថយន្តចត,ចំនួនកិច្ចសន្យា,ស្ថានភាព\n";
  monthlyReports.value.forEach(r => {
    csv += `"${r.month}","${r.revenue.toFixed(2)}","${r.parkings}","${r.contracts}","${r.status}"\n`;
  });

  csv += "\n\nព័ត៌មានលម្អិតវិក្កយបត្របង់ប្រាក់ជាក់ស្តែង (Payment Invoices)\n";
  csv += "វិក្កយបត្រ ID,ឈ្មោះអតិថិជន,ចំនួនទឹកប្រាក់ ($),កាលបរិច្ឆេទ,ស្ថានភាព\n";
  payments.value.forEach(p => {
    const id = `#INV-${p.id.toString().padStart(4, '0')}`;
    const name = getCustomerName(p.customer_id);
    const amount = p.amount.toFixed(2);
    const date = p.payment_date ? new Date(p.payment_date).toISOString().split('T')[0] : '';
    csv += `"${id}","${name}","${amount}","${date}","${p.status}"\n`;
  });

  const blob = new Blob(["\uFEFF" + csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.setAttribute("href", url);
  link.setAttribute("download", `CarPark_Report_${new Date().toISOString().split('T')[0]}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

onMounted(() => {
  fetchReportsData();
});
</script>

<template>
  <div class="flex h-screen bg-[#f8fafc] font-sans text-gray-800">
    <!-- Sidebar -->
    <aside class="w-[260px] bg-primary text-white flex flex-col transition-all duration-300 z-20 shrink-0 shadow-xl">
      <div class="h-20 flex items-center px-6 border-b border-white/5">
        <div class="w-10 h-10 bg-white text-primary rounded-xl flex items-center justify-center font-bold text-2xl mr-3 shadow-md">P</div>
        <div>
          <h1 class="font-bold text-xl tracking-wide">Car<span class="text-green-400">Park</span></h1>
          <p class="text-[9px] text-gray-300 uppercase tracking-wider font-medium">Management System</p>
        </div>
      </div>
      
      <nav class="flex-1 px-4 py-4 space-y-1 overflow-y-auto mt-2 text-sm font-medium">
        <router-link to="/dashboard" active-class="bg-white/10 text-white font-semibold" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
          Dashboard
        </router-link>
        <router-link to="/users" active-class="bg-white/10 text-white font-semibold" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
          Users
        </router-link>
        <router-link to="/customers" active-class="bg-white/10 text-white font-semibold" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
          Customers
        </router-link>
        <router-link to="/parking" active-class="bg-white/10 text-white font-semibold" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7h12.5M8 7v8.5A2.5 2.5 0 0010.5 18h3.8M8 7l-4.5 4.5M20.5 7v11M16 11h4.5M16 14.5h4.5" /></svg>
          Vehicles
        </router-link>
        <router-link to="/spaces" active-class="bg-white/10 text-white font-semibold" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
          Parking Spaces
        </router-link>
        <router-link to="/contracts" active-class="bg-white/10 text-white font-semibold" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
          Contracts
        </router-link>
        <router-link to="/payments" active-class="bg-white/10 text-white font-semibold" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>
          Payments
        </router-link>
        <router-link to="/notifications" active-class="bg-white/10 text-white font-semibold" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
          Notifications
        </router-link>
        <router-link to="/reports" active-class="bg-white/10 text-white font-semibold" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
          Reports
        </router-link>
        <router-link to="/settings" active-class="bg-white/10 text-white font-semibold" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
          Settings
        </router-link>
      </nav>
      
      <div class="p-5 border-t border-white/10">
        <p class="text-[10px] text-gray-300 mb-3 opacity-60">Version 1.0.0</p>
        <button @click="handleLogout" class="w-full flex items-center gap-2 text-red-400 hover:text-red-300 hover:bg-white/5 px-3 py-2 rounded-xl transition-colors font-medium text-sm">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          Logout
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden relative">
      <header class="h-20 bg-white border-b border-gray-100 flex items-center justify-between px-8 z-10">
        <div class="flex items-center gap-3">
          <h2 class="text-xl font-bold text-gray-800">របាយការណ៍ និងស្ថិតិ (Reports & Analytics)</h2>
          <span class="px-2.5 py-1 text-xs font-bold bg-green-50 text-primary rounded-full">
            ទិន្នន័យផ្សាយបន្តផ្ទាល់ (Live Database)
          </span>
        </div>

        <div class="flex items-center gap-4">
          <button @click="exportReport" class="px-4 py-2 bg-emerald-600 text-white rounded-xl text-sm font-bold hover:bg-emerald-700 transition-colors flex items-center gap-2 shadow-sm">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
            ទាញយករបាយការណ៍ជា Excel (CSV)
          </button>
          
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-full bg-primary text-white flex items-center justify-center font-bold text-sm shadow-sm">A</div>
            <div>
              <p class="text-sm font-bold text-gray-800 leading-tight">{{ userName }}</p>
              <p class="text-xs text-gray-500">Administrator</p>
            </div>
          </div>
        </div>
      </header>

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        <!-- 4 Summary Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
            <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">ចំណូលសរុប (Total Revenue)</p>
            <h3 class="text-3xl font-extrabold text-primary">${{ summary.totalRevenue.toFixed(2) }}</h3>
          </div>
          <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
            <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">រថយន្តបានបម្រើ (Vehicles)</p>
            <h3 class="text-3xl font-extrabold text-blue-600">{{ summary.totalVehiclesServiced }} គ្រឿង</h3>
          </div>
          <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
            <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">រយៈពេលចតមធ្យម</p>
            <h3 class="text-3xl font-extrabold text-purple-600">{{ summary.averageDuration }}</h3>
          </div>
          <div class="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
            <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">កិច្ចសន្យាសកម្ម (Leases)</p>
            <h3 class="text-3xl font-extrabold text-amber-500">{{ summary.activeLeases }}</h3>
          </div>
        </div>

        <!-- Monthly Breakdown Table -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden mb-8">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center">
            <div>
              <h3 class="font-bold text-base text-gray-800">របាយការណ៍ហិរញ្ញវត្ថុ និងប្រតិបត្តិការប្រចាំខែ</h3>
              <p class="text-xs text-gray-400 mt-0.5">ទិន្នន័យជាក់ស្តែងគណនាចេញពី Database</p>
            </div>
            <span class="text-xs text-gray-500 bg-gray-100 px-3 py-1 rounded-full font-mono font-medium">ឆ្នាំ 2026</span>
          </div>
          <table class="w-full text-left text-sm">
            <thead class="bg-gray-50 text-gray-400 uppercase text-xs border-b border-gray-100 font-semibold">
              <tr>
                <th class="px-6 py-4">ខែ/ឆ្នាំ</th>
                <th class="px-6 py-4">ចំណូលសរុប (USD)</th>
                <th class="px-6 py-4">រថយន្តចត</th>
                <th class="px-6 py-4">កិច្ចសន្យាថ្មី</th>
                <th class="px-6 py-4">ស្ថានភាព</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-if="monthlyReports.length === 0">
                <td colspan="5" class="px-6 py-8 text-center text-gray-400">មិនទាន់មានទិន្នន័យប្រតិបត្តិការនៅឡើយទេ...</td>
              </tr>
              <tr v-for="(row, idx) in monthlyReports" :key="idx" class="hover:bg-gray-50/80 transition-colors">
                <td class="px-6 py-4 font-bold text-gray-800">{{ row.month }}</td>
                <td class="px-6 py-4 font-bold text-primary">${{ row.revenue.toFixed(2) }}</td>
                <td class="px-6 py-4 font-mono">{{ row.parkings }} គ្រឿង</td>
                <td class="px-6 py-4 font-mono">{{ row.contracts }}</td>
                <td class="px-6 py-4">
                  <span 
                    class="px-2.5 py-1 rounded-full text-xs font-bold"
                    :class="row.status === 'កំពុងដំណើរការ' ? 'bg-blue-50 text-blue-600 border border-blue-200' : 'bg-green-50 text-green-600 border border-green-200'"
                  >
                    {{ row.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Recent Real Financial Invoices Table -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center">
            <div>
              <h3 class="font-bold text-base text-gray-800">ប្រវត្តិវិក្កយបត្របង់ប្រាក់ពិតប្រាកដ (Financial Audit Ledger)</h3>
              <p class="text-xs text-gray-400 mt-0.5">រាល់ប្រតិបត្តិការដែលបានកត់ត្រាក្នុង Database</p>
            </div>
            <router-link to="/payments" class="text-xs font-bold text-primary hover:underline">+ គ្រប់គ្រងការបង់ប្រាក់</router-link>
          </div>
          <table class="w-full text-left text-sm">
            <thead class="bg-gray-50 text-gray-400 uppercase text-xs border-b border-gray-100 font-semibold">
              <tr>
                <th class="px-6 py-4">វិក្កយបត្រ (Invoice)</th>
                <th class="px-6 py-4">អតិថិជន (Customer)</th>
                <th class="px-6 py-4">កាលបរិច្ឆេទ (Date)</th>
                <th class="px-6 py-4">ចំនួនទឹកប្រាក់</th>
                <th class="px-6 py-4">ស្ថានភាព</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-if="payments.length === 0">
                <td colspan="5" class="px-6 py-8 text-center text-gray-400">មិនទាន់មានវិក្កយបត្របង់ប្រាក់នៅឡើយទេ...</td>
              </tr>
              <tr v-for="pay in payments" :key="pay.id" class="hover:bg-gray-50/80 transition-colors">
                <td class="px-6 py-4 font-mono font-bold text-gray-900">#INV-{{ pay.id.toString().padStart(4, '0') }}</td>
                <td class="px-6 py-4 font-medium text-gray-800">{{ getCustomerName(pay.customer_id) }}</td>
                <td class="px-6 py-4 text-gray-500 font-mono text-xs">
                  {{ pay.payment_date ? new Date(pay.payment_date).toLocaleString('en-GB') : '-' }}
                </td>
                <td class="px-6 py-4 font-bold text-primary">${{ pay.amount.toFixed(2) }}</td>
                <td class="px-6 py-4">
                  <span 
                    class="px-2.5 py-1 rounded-full text-xs font-bold"
                    :class="pay.status === 'Paid' ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-amber-50 text-amber-700 border border-amber-200'"
                  >
                    {{ pay.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

      </main>
    </div>
  </div>
</template>
