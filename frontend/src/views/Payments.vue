<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const payments = ref([]);
const customers = ref([]);
const userName = ref('Admin');

// អថេរសម្រាប់គ្រប់គ្រង Modal និង ជំហានបង់ប្រាក់
const showModal = ref(false);
const paymentStep = ref(1); // 1 = បំពេញទិន្នន័យ, 2 = ស្កេន QR Code
const paymentMethod = ref('Cash'); // Cash ឬ Bank
const isProcessing = ref(false);
const isSubmitting = ref(false);

const newPayment = ref({
  customer_id: '',
  amount: 60.00,
  status: 'Paid'
});

// ទាញយកប្រវត្តិបង់ប្រាក់
const fetchPayments = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://127.0.0.1:8000/payments/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    payments.value = response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      alert("សោររបស់អ្នកផុតកំណត់ហើយ! សូម Login ម្តងទៀត។");
      handleLogout();
    }
  }
};

// ទាញយកបញ្ជីអតិថិជន ដើម្បីងាយស្រួលជ្រើសរើសក្នុង Modal
const fetchCustomers = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://127.0.0.1:8000/customers/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    customers.value = response.data;
  } catch (error) {
    console.error("Error fetching customers:", error);
  }
};

// ស្វែងរកឈ្មោះអតិថិជនតាមរយៈ ID
const getCustomerName = (customerId) => {
  const found = customers.value.find(c => c.id === customerId);
  return found ? `${found.last_name} ${found.first_name}` : `Customer #${customerId}`;
};

// អនុគមន៍សម្រាប់ពិនិត្យមើលមុននឹង Save (Cash ឬ Bank)
const handleProceedPayment = () => {
  if (!newPayment.value.customer_id) {
    alert("សូមជ្រើសរើស ឬបញ្ចូលលេខសម្គាល់អតិថិជន!");
    return;
  }
  if (!newPayment.value.amount || Number(newPayment.value.amount) <= 0) {
    alert("សូមបញ្ចូលចំនួនទឹកប្រាក់ដែលត្រឹមត្រូវ!");
    return;
  }

  if (paymentMethod.value === 'Bank') {
    // បើជ្រើសរើស Bank ប្តូរទៅទំព័រទី 2 ដើម្បីបង្ហាញ QR Code
    paymentStep.value = 2;
  } else {
    // បើលុយសុទ្ធ (Cash) រក្សាទុកយកតែម្តង
    createPayment();
  }
};

// អនុគមន៍បញ្ជាក់ថាបានស្កេនរួចរាល់ (Simulate Bank Webhook)
const confirmBankPayment = () => {
  isProcessing.value = true;
  // ក្លែងធ្វើការរង់ចាំធនាគារដំណើរការ 1.5 វិនាទី
  setTimeout(async () => {
    await createPayment();
    isProcessing.value = false;
  }, 1500);
};

// អនុគមន៍រក្សាទុកទៅកាន់ Database
const createPayment = async () => {
  isSubmitting.value = true;
  try {
    const token = localStorage.getItem('token');
    await axios.post('http://127.0.0.1:8000/payments/', {
      customer_id: parseInt(newPayment.value.customer_id),
      amount: parseFloat(newPayment.value.amount),
      status: newPayment.value.status
    }, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    // Reset ទិន្នន័យពេលជោគជ័យ
    showModal.value = false;
    paymentStep.value = 1;
    newPayment.value = { customer_id: '', amount: 60.00, status: 'Paid' };
    paymentMethod.value = 'Cash';
    
    await fetchPayments();
    alert("ទូទាត់ប្រាក់ជោគជ័យ! (Payment Successful)");
  } catch (error) {
    const msg = error.response?.data?.detail || "មានបញ្ហា! សូមប្រាកដថាលេខអតិថិជននេះពិតជាមានក្នុងប្រព័ន្ធមែន។";
    alert(typeof msg === 'string' ? msg : JSON.stringify(msg));
  } finally {
    isSubmitting.value = false;
  }
};

// អនុគមន៍ទាញយករបាយការណ៍ជា Excel (CSV)
const exportToCSV = () => {
  if (payments.value.length === 0) {
    alert("មិនមានទិន្នន័យសម្រាប់ទាញយកទេ!");
    return;
  }
  
  // ១. បង្កើតក្បាលតារាង (Headers)
  let csvContent = "វិក្កយបត្រ (ID),លេខអតិថិជន (CUS ID),ឈ្មោះអតិថិជន (Customer Name),ចំនួនទឹកប្រាក់ (USD),កាលបរិច្ឆេទ (Date),ស្ថានភាព (Status)\n";
  
  // ២. បញ្ចូលទិន្នន័យម្តងមួយជួរៗ
  payments.value.forEach(pay => {
    const id = `INV-${pay.id.toString().padStart(4, '0')}`;
    const cusId = pay.customer_id;
    const cusName = getCustomerName(pay.customer_id);
    const amount = pay.amount.toFixed(2);
    const date = pay.payment_date ? new Date(pay.payment_date).toLocaleString('en-GB') : '';
    const status = pay.status;
    
    csvContent += `${id},${cusId},"${cusName}",${amount},"${date}",${status}\n`;
  });
  
  // ៣. បង្កើតជា File និងបញ្ជាឲ្យ Download (UTF-8 BOM \uFEFF)
  const blob = new Blob(["\uFEFF" + csvContent], { type: 'text/csv;charset=utf-8;' }); 
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  
  const today = new Date().toISOString().split('T')[0];
  link.setAttribute("href", url);
  link.setAttribute("download", `CarPark_Revenue_Report_${today}.csv`);
  
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('en-GB'); 
};

onMounted(() => {
  fetchPayments();
  fetchCustomers();
});
</script>

<template>
  <div class="flex h-screen bg-gray-50 font-sans text-gray-800">
    
    <!-- របារចំហៀង (Sidebar) -->
    <aside class="w-64 bg-primary text-white flex flex-col transition-all duration-300 shadow-xl z-20">
      <div class="h-20 flex items-center px-6 border-b border-white/10">
        <div class="w-10 h-10 bg-white text-primary rounded-lg flex items-center justify-center font-bold text-2xl mr-3 shadow-md">P</div>
        <div>
          <h1 class="font-bold text-xl tracking-wide">Car<span class="text-green-400">Park</span></h1>
          <p class="text-[10px] text-gray-300 uppercase tracking-wider">Management System</p>
        </div>
      </div>
      <nav class="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
        <router-link to="/dashboard" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-lg font-medium transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" /></svg>
          Dashboard
        </router-link>
        <router-link to="/customers" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-lg font-medium transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" /></svg>
          Customers
        </router-link>
        <router-link to="/parking" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-lg font-medium transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" /></svg>
          Parking
        </router-link>
        <router-link to="/payments" class="flex items-center gap-3 px-4 py-3 bg-white/15 text-white rounded-lg font-medium transition-colors shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" /></svg>
          Payments
        </router-link>
      </nav>
      
      <!-- Version & Logout -->
      <div class="px-6 py-2 text-xs text-emerald-200/60">Version 1.0.0</div>
      <div class="p-4 border-t border-white/10">
        <button @click="handleLogout" class="w-full flex items-center justify-center gap-2 bg-red-500/10 text-red-400 hover:bg-red-500 hover:text-white py-2.5 rounded-lg transition-colors font-medium">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" /></svg>
          Logout
        </button>
      </div>
    </aside>

    <!-- ផ្ទៃបង្ហាញព័ត៌មាន (Main Content) -->
    <div class="flex-1 flex flex-col overflow-hidden relative">
      <!-- Header -->
      <header class="h-20 bg-white border-b border-gray-200 flex items-center justify-between px-8 z-10">
        <div class="flex items-center gap-4">
          <h2 class="text-xl font-bold text-gray-800">Payments Management</h2>
          <span class="text-xs text-gray-500 bg-gray-100 px-2.5 py-1 rounded-full font-medium">Admin Portal</span>
        </div>
        <div class="flex items-center gap-4">
          <div class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-bold shadow-sm">A</div>
          <div>
            <p class="text-sm font-bold text-gray-700">{{ userName }}</p>
            <p class="text-xs text-gray-500">Administrator</p>
          </div>
        </div>
      </header>

      <!-- តារាងបង់ប្រាក់ -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-8">
        
        <!-- Breadcrumbs & Actions -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div>
            <h3 class="text-2xl font-bold text-gray-800">Payment Records</h3>
            <p class="text-sm text-gray-500 mt-0.5">Home / Payments</p>
          </div>
          
          <!-- ប៊ូតុងទាំង ២ (Export CSV & Create Payment) -->
          <div class="flex items-center gap-3">
            <button @click="exportToCSV" class="bg-gray-800 text-white px-4 py-2.5 rounded-xl font-medium hover:bg-gray-900 transition-colors shadow-sm flex items-center gap-2 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" /></svg>
              Export Report (CSV)
            </button>

            <button @click="showModal = true; paymentStep = 1" class="bg-primary text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-secondary transition-all flex items-center gap-2 shadow-md shadow-primary/20 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
              + បង្កើតវិក្កយបត្រថ្មី (New Payment)
            </button>
          </div>
        </div>

        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
            <div>
              <h4 class="text-base font-bold text-gray-800">ប្រវត្តិបង់ប្រាក់ប្រចាំខែទាំងអស់</h4>
              <p class="text-xs text-gray-500 mt-0.5">សរុបមាន {{ payments.length }} កំណត់ត្រាក្នុងប្រព័ន្ធ</p>
            </div>
            <div class="text-xs font-semibold px-3 py-1 bg-emerald-50 text-emerald-700 rounded-lg border border-emerald-100">
              Auto-sync Active
            </div>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-gray-500">
              <thead class="text-xs text-gray-700 uppercase bg-gray-50 border-b border-gray-100">
                <tr>
                  <th scope="col" class="px-6 py-4">វិក្កយបត្រ (Invoice ID)</th>
                  <th scope="col" class="px-6 py-4">អតិថិជន (Customer)</th>
                  <th scope="col" class="px-6 py-4">ចំនួនទឹកប្រាក់</th>
                  <th scope="col" class="px-6 py-4">កាលបរិច្ឆេទបង់ (Date)</th>
                  <th scope="col" class="px-6 py-4">ស្ថានភាព (Status)</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-if="payments.length === 0">
                  <td colspan="5" class="px-6 py-12 text-center text-gray-400">
                    <div class="flex flex-col items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10 mb-2 text-gray-300"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" /></svg>
                      <p>មិនទាន់មានប្រវត្តិបង់ប្រាក់នៅឡើយទេ...</p>
                      <button @click="showModal = true; paymentStep = 1" class="mt-3 text-xs text-primary font-semibold hover:underline">+ បង្កើតកំណត់ត្រាដំបូង</button>
                    </div>
                  </td>
                </tr>
                <tr v-for="pay in payments" :key="pay.id" class="hover:bg-gray-50/80 transition-colors">
                  <td class="px-6 py-4 font-mono font-semibold text-gray-900">
                    #INV-{{ pay.id.toString().padStart(4, '0') }}
                  </td>
                  <td class="px-6 py-4">
                    <div class="font-medium text-gray-800">{{ getCustomerName(pay.customer_id) }}</div>
                    <div class="text-xs text-gray-400 font-mono">ID: #{{ pay.customer_id }}</div>
                  </td>
                  <td class="px-6 py-4 font-bold text-primary text-base">
                    ${{ pay.amount.toFixed(2) }}
                  </td>
                  <td class="px-6 py-4 text-gray-600">
                    {{ formatDate(pay.payment_date) }}
                  </td>
                  <td class="px-6 py-4">
                    <span v-if="pay.status === 'Paid'" class="inline-flex items-center gap-1.5 px-3 py-1 bg-green-50 text-success rounded-full text-xs font-bold border border-green-200">
                      <span class="w-1.5 h-1.5 rounded-full bg-success"></span>
                      Paid (បង់រួច)
                    </span>
                    <span v-else-if="pay.status === 'Pending'" class="inline-flex items-center gap-1.5 px-3 py-1 bg-amber-50 text-warning rounded-full text-xs font-bold border border-amber-200">
                      <span class="w-1.5 h-1.5 rounded-full bg-warning"></span>
                      Pending (រង់ចាំ)
                    </span>
                    <span v-else class="inline-flex items-center gap-1.5 px-3 py-1 bg-red-50 text-danger rounded-full text-xs font-bold border border-red-200">
                      <span class="w-1.5 h-1.5 rounded-full bg-danger"></span>
                      {{ pay.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>

      <!-- Modal បង់ប្រាក់ដែលរួមបញ្ចូល Bank KHQR Code -->
      <div v-if="showModal" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4 backdrop-blur-sm transition-all">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden transform transition-all border border-gray-100">
          
          <!-- ជំហានទី ១៖ ផ្ទាំងបំពេញព័ត៌មាន -->
          <div v-if="paymentStep === 1">
            <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/70">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" /></svg>
                </div>
                <div>
                  <h3 class="text-lg font-bold text-gray-900">ទូទាត់វិក្កយបត្រចំណត</h3>
                  <p class="text-xs text-gray-500">Record New Monthly Payment</p>
                </div>
              </div>
              <button @click="showModal = false" class="text-gray-400 hover:text-red-500 p-1 rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>

            <form @submit.prevent="handleProceedPayment" class="p-6 space-y-4">
              <!-- ជ្រើសរើសអតិថិជន -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">អតិថិជន (Customer)</label>
                <select v-if="customers.length > 0" v-model="newPayment.customer_id" required class="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary text-sm bg-white">
                  <option value="" disabled>-- សូមជ្រើសរើសអតិថិជន --</option>
                  <option v-for="c in customers" :key="c.id" :value="c.id">
                    #{{ c.id }} - {{ c.last_name }} {{ c.first_name }} ({{ c.phone_number }})
                  </option>
                </select>
                <input v-else v-model.number="newPayment.customer_id" type="number" required class="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary text-sm" placeholder="បញ្ចូលលេខ ID អតិថិជន (Customer ID)">
              </div>

              <!-- ចំនួនទឹកប្រាក់ ($) -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">ចំនួនទឹកប្រាក់ (Amount in USD)</label>
                <div class="relative">
                  <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-500 font-bold">$</div>
                  <input v-model.number="newPayment.amount" type="number" step="0.01" min="0" required class="w-full pl-8 pr-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary text-sm font-semibold text-gray-800" placeholder="60.00">
                </div>
              </div>
              
              <!-- ជម្រើសវិធីបង់ប្រាក់ -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">វិធីទូទាត់ប្រាក់ (Payment Method)</label>
                <div class="grid grid-cols-2 gap-4">
                  <label class="cursor-pointer">
                    <input type="radio" v-model="paymentMethod" value="Cash" class="peer sr-only" name="payment">
                    <div class="rounded-xl border-2 border-gray-200 p-3.5 text-center peer-checked:border-primary peer-checked:bg-green-50/70 hover:bg-gray-50 transition-all">
                      <span class="block text-xl mb-1">💵</span>
                      <span class="font-bold text-gray-700 text-sm">Cash (លុយសុទ្ធ)</span>
                    </div>
                  </label>
                  <label class="cursor-pointer">
                    <input type="radio" v-model="paymentMethod" value="Bank" class="peer sr-only" name="payment">
                    <div class="rounded-xl border-2 border-gray-200 p-3.5 text-center peer-checked:border-blue-500 peer-checked:bg-blue-50/70 hover:bg-gray-50 transition-all">
                      <span class="block text-xl mb-1">🏦</span>
                      <span class="font-bold text-gray-700 text-sm">KHQR / ABA</span>
                    </div>
                  </label>
                </div>
              </div>

              <!-- ស្ថានភាព -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1.5">ស្ថានភាព (Payment Status)</label>
                <select v-model="newPayment.status" class="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary/20 focus:border-primary text-sm bg-white font-medium">
                  <option value="Paid">Paid (បានបង់រួច)</option>
                  <option value="Pending">Pending (រង់ចាំការបង់)</option>
                </select>
              </div>

              <div class="pt-3">
                <button type="submit" :disabled="isSubmitting" class="w-full bg-primary text-white py-3.5 rounded-xl font-bold text-base hover:bg-secondary transition-colors shadow-lg shadow-primary/25 disabled:opacity-70">
                  <span v-if="isSubmitting">កំពុងរក្សាទុក...</span>
                  <span v-else>{{ paymentMethod === 'Bank' ? 'បង្កើត QR សម្រាប់ស្កេន (Generate KHQR)' : 'បញ្ជាក់ការបង់ប្រាក់ (Confirm Payment)' }}</span>
                </button>
              </div>
            </form>
          </div>

          <!-- ជំហានទី ២៖ ផ្ទាំង KHQR Code ស្កេនទូទាត់ -->
          <div v-else-if="paymentStep === 2" class="p-6 flex flex-col items-center">
            <!-- ABA / KHQR Header -->
            <div class="w-full bg-[#00557b] text-white p-4 rounded-2xl flex items-center justify-between mb-5 shadow-md">
              <div class="flex items-center gap-2">
                <div class="w-7 h-7 bg-red-600 rounded-lg flex items-center justify-center font-bold text-xs text-white">KH</div>
                <span class="font-bold tracking-wider text-sm">KHQR PAY</span>
              </div>
              <span class="font-extrabold text-2xl">${{ Number(newPayment.amount || 0).toFixed(2) }}</span>
            </div>
            
            <h4 class="text-gray-600 mb-3 text-sm text-center font-medium">សូមស្កេន QR កូដខាងក្រោមដើម្បីបង់ប្រាក់</h4>
            
            <!-- Mock QR Code Design -->
            <div class="bg-white p-4 border-4 border-[#00557b] rounded-2xl mb-4 relative shadow-lg">
              <!-- SVG QR Code Icon -->
              <svg xmlns="http://www.w3.org/2000/svg" class="w-44 h-44 text-gray-800" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 3h8v8H3V3zm2 2v4h4V5H5zm8-2h8v8h-8V3zm2 2v4h4V5h-4zM3 13h8v8H3v-8zm2 2v4h4v-4H5zm13-2h3v3h-3v-3zm-3 3h3v3h-3v-3zm3 3h3v3h-3v-3zm-3-6h3v3h-3v-3zm-3 3h3v3h-3v-3zm0 3h3v3h-3v-3zm-3-3h3v3h-3v-3zm3 3h3v3h-3v-3z"/>
              </svg>
              <!-- កណ្តាល QR មានរូបតំណាង ABA/KH -->
              <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div class="bg-white p-1 rounded-xl shadow-md border border-gray-200">
                  <div class="w-9 h-9 bg-[#ea2127] text-white flex items-center justify-center font-extrabold text-xs rounded-lg">KHQR</div>
                </div>
              </div>
            </div>

            <p class="text-sm font-bold text-gray-800 mb-6">Car Park Management Co., Ltd</p>

            <div class="w-full flex gap-3">
              <button @click="paymentStep = 1" :disabled="isProcessing" class="w-1/2 bg-gray-100 text-gray-700 py-3 rounded-xl font-bold hover:bg-gray-200 transition-colors disabled:opacity-50 text-sm">
                ត្រឡប់ក្រោយ
              </button>
              <button @click="confirmBankPayment" :disabled="isProcessing" class="w-1/2 bg-[#00557b] text-white py-3 rounded-xl font-bold hover:bg-[#003d59] transition-colors shadow-lg disabled:opacity-70 flex justify-center items-center gap-2 text-sm">
                <svg v-if="isProcessing" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ isProcessing ? 'កំពុងផ្ទៀងផ្ទាត់...' : 'ទូទាត់រួចរាល់' }}
              </button>
            </div>
          </div>

        </div>
      </div>
      <!-- ចប់ Modal -->

    </div>
  </div>
</template>
