<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Sidebar from '../components/Sidebar.vue';
import Navbar from '../components/Navbar.vue';
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
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden relative">
      <Navbar title="Reports & Analytics" subtitle="Home / Reports" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        <!-- Top Title & Export Button -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <div class="flex items-center gap-3">
              <h2 class="text-2xl font-extrabold text-gray-800">របាយការណ៍ និងស្ថិតិ (Reports & Analytics)</h2>
              <span class="px-2.5 py-1 text-xs font-bold bg-green-50 text-primary rounded-full border border-green-200">
                Live Database
              </span>
            </div>
            <p class="text-sm text-gray-500 mt-1">ទិដ្ឋភាពទូទៅនៃប្រតិបត្តិការហិរញ្ញវត្ថុ ការកក់កិច្ចសន្យា និងចំណតរថយន្ត</p>
          </div>

          <button @click="exportReport" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl text-sm font-bold shadow-md transition-all flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
            ទាញយករបាយការណ៍ជា Excel (CSV)
          </button>
        </div>

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
