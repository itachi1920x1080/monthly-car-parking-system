<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const contracts = ref([]);
const customers = ref([]);
const userName = ref('Admin');

const showModal = ref(false);
const newContract = ref({
  customer_id: '',
  space_id: '',
  start_date: '',
  end_date: '',
  status: 'Active'
});

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

const getCustomerName = (customerId) => {
  const found = customers.value.find(c => c.id === customerId);
  return found ? `${found.last_name} ${found.first_name}` : `CUS-${customerId}`;
};

const fetchContracts = async () => {
  try {
    const token = localStorage.getItem('token');
    // សាកល្បងហៅ API (បើថ្ងៃមុខយើងមាន Backend សម្រាប់វា)
    const response = await axios.get('http://127.0.0.1:8000/contracts/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    contracts.value = response.data;
  } catch (error) {
    // ដោយសារពេលនេះយើងអត់ទាន់មាន Backend API, យើងក្លែងធ្វើទិន្នន័យបង្ហាញសិន
    contracts.value = [
      { id: 1, customer_id: 1, space_id: 'A-01', start_date: '2026-11-01', end_date: '2027-11-01', status: 'Active' },
      { id: 2, customer_id: 2, space_id: 'B-12', start_date: '2026-05-15', end_date: '2026-11-15', status: 'Expired' },
      { id: 3, customer_id: 3, space_id: 'A-05', start_date: '2026-11-08', end_date: '2027-11-08', status: 'Active' }
    ];
  }
};

const createContract = () => {
  // ក្លែងធ្វើការរក្សាទុកទិន្នន័យ (Mock Save)
  const fakeId = contracts.value.length + 1;
  contracts.value.unshift({
    id: fakeId,
    customer_id: newContract.value.customer_id,
    space_id: newContract.value.space_id,
    start_date: newContract.value.start_date,
    end_date: newContract.value.end_date,
    status: newContract.value.status
  });
  
  showModal.value = false;
  newContract.value = { customer_id: '', space_id: '', start_date: '', end_date: '', status: 'Active' };
  alert("បង្កើតកិច្ចសន្យាថ្មីបានជោគជ័យ! (បណ្តោះអាសន្ននៅលើ UI)");
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
  fetchContracts();
  fetchCustomers();
});
</script>

<template>
  <div class="flex h-screen bg-[#f8fafc] font-sans text-gray-800">
    
    <!-- Sidebar -->
    <aside class="w-[260px] bg-primary text-white flex flex-col transition-all duration-300 z-20 shadow-xl">
      <div class="h-20 flex items-center px-6">
        <div class="w-10 h-10 bg-white text-primary rounded-xl flex items-center justify-center font-bold text-2xl mr-3 shadow-md">P</div>
        <div>
          <h1 class="font-bold text-xl tracking-wide">Car<span class="text-green-400">Park</span></h1>
          <p class="text-[9px] text-gray-300 uppercase tracking-wider font-medium">Management System</p>
        </div>
      </div>
      
      <!-- ប្រើប្រាស់ active-class ដើម្បីឲ្យវាភ្លឺស្វ័យប្រវត្តិ ពេលចុចម៉ឺនុយណាមួយ -->
      <nav class="flex-1 px-4 py-4 space-y-1.5 overflow-y-auto mt-4 text-sm font-medium">
        <router-link to="/dashboard" active-class="bg-white/10 text-white" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
          Dashboard
        </router-link>
        <router-link to="/customers" active-class="bg-white/10 text-white" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
          Customers
        </router-link>
        <router-link to="/parking" active-class="bg-white/10 text-white" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7h12.5M8 7v8.5A2.5 2.5 0 0010.5 18h3.8M8 7l-4.5 4.5M20.5 7v11M16 11h4.5M16 14.5h4.5" /></svg>
          Vehicles
        </router-link>
        <!-- មឺនុយ Contracts ថ្មី -->
        <router-link to="/contracts" active-class="bg-white/10 text-white" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
          Contracts
        </router-link>
        <router-link to="/payments" active-class="bg-white/10 text-white" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>
          Payments
        </router-link>
      </nav>
      
      <div class="p-6 border-t border-white/10">
        <p class="text-[10px] text-emerald-200/60 mb-3">Version 1.0.0</p>
        <button @click="handleLogout" class="w-full flex items-center gap-2 text-red-400 hover:text-red-300 transition-colors font-medium text-sm">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          Logout
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden relative">
      <header class="h-20 bg-white border-b border-gray-100 flex items-center justify-between px-8 z-10">
        <div class="flex items-center gap-4">
          <h2 class="text-xl font-bold text-gray-800">Contracts Management</h2>
          <span class="text-xs text-gray-500 bg-gray-100 px-2.5 py-1 rounded-full font-medium">Monthly Leases</span>
        </div>
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-bold shadow-sm">A</div>
          <div>
            <p class="text-sm font-bold text-gray-700 leading-tight">{{ userName }}</p>
            <p class="text-xs text-gray-500">Administrator</p>
          </div>
        </div>
      </header>

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
            <div>
              <h3 class="text-lg font-bold text-gray-800">បញ្ជីកិច្ចសន្យា (Contracts List)</h3>
              <p class="text-xs text-gray-400 mt-0.5">សរុបមាន {{ contracts.length }} កិច្ចសន្យាក្នុងប្រព័ន្ធ</p>
            </div>
            <button @click="showModal = true" class="bg-primary text-white px-4 py-2.5 rounded-xl font-semibold hover:bg-secondary transition-colors shadow-md shadow-primary/20 flex items-center gap-2 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
              + បង្កើតកិច្ចសន្យាថ្មី
            </button>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-gray-500">
              <thead class="text-xs text-gray-400 uppercase bg-gray-50 tracking-wider border-b border-gray-100">
                <tr>
                  <th scope="col" class="px-6 py-4">កិច្ចសន្យា (ID)</th>
                  <th scope="col" class="px-6 py-4">អតិថិជន</th>
                  <th scope="col" class="px-6 py-4">កន្លែងចត (Space)</th>
                  <th scope="col" class="px-6 py-4">ថ្ងៃចាប់ផ្តើម</th>
                  <th scope="col" class="px-6 py-4">ថ្ងៃផុតកំណត់</th>
                  <th scope="col" class="px-6 py-4">ស្ថានភាព</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="contract in contracts" :key="contract.id" class="hover:bg-gray-50/80 transition-colors">
                  <td class="px-6 py-4 font-bold font-mono text-gray-900">#CT-{{ contract.id.toString().padStart(3, '0') }}</td>
                  <td class="px-6 py-4 font-medium text-gray-700">
                    <div class="font-semibold text-gray-800">{{ getCustomerName(contract.customer_id) }}</div>
                    <div class="text-xs text-gray-400 font-mono">ID: #{{ contract.customer_id }}</div>
                  </td>
                  <td class="px-6 py-4 font-bold text-primary font-mono">{{ contract.space_id }}</td>
                  <td class="px-6 py-4 font-mono text-gray-600">{{ formatDate(contract.start_date) }}</td>
                  <td class="px-6 py-4 font-mono text-gray-600">{{ formatDate(contract.end_date) }}</td>
                  <td class="px-6 py-4">
                    <span v-if="contract.status === 'Active'" class="inline-flex items-center gap-1.5 px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-bold border border-green-200">
                      <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span>
                      Active
                    </span>
                    <span v-else class="inline-flex items-center gap-1.5 px-3 py-1 bg-red-50 text-red-700 rounded-full text-xs font-bold border border-red-200">
                      <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                      Expired
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>

      <!-- Modal បង្កើតកិច្ចសន្យា -->
      <div v-if="showModal" class="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4 backdrop-blur-sm transition-all">
        <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden transform transition-all border border-gray-100">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/70">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
              </div>
              <div>
                <h3 class="text-lg font-bold text-gray-900">បង្កើតកិច្ចសន្យាថ្មី</h3>
                <p class="text-xs text-gray-500">Create New Parking Lease</p>
              </div>
            </div>
            <button @click="showModal = false" class="text-gray-400 hover:text-red-500 p-1 rounded-lg">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
          
          <form @submit.prevent="createContract" class="p-6 space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">អតិថិជន</label>
                <select v-if="customers.length > 0" v-model="newContract.customer_id" required class="w-full p-2.5 border border-gray-300 rounded-xl focus:ring-primary focus:border-primary text-sm bg-white">
                  <option value="" disabled>-- ជ្រើសរើស --</option>
                  <option v-for="c in customers" :key="c.id" :value="c.id">
                    #{{ c.id }} {{ c.last_name }}
                  </option>
                </select>
                <input v-else v-model.number="newContract.customer_id" type="number" required class="w-full p-2.5 border border-gray-300 rounded-xl focus:ring-primary focus:border-primary text-sm" placeholder="លេខ ID">
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">កន្លែងចត (Space)</label>
                <input v-model="newContract.space_id" type="text" required class="w-full p-2.5 border border-gray-300 rounded-xl focus:ring-primary focus:border-primary uppercase text-sm font-semibold" placeholder="ឧ. A-01">
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">ថ្ងៃចាប់ផ្តើម</label>
                <input v-model="newContract.start_date" type="date" required class="w-full p-2.5 border border-gray-300 rounded-xl focus:ring-primary focus:border-primary text-sm">
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">ថ្ងៃផុតកំណត់</label>
                <input v-model="newContract.end_date" type="date" required class="w-full p-2.5 border border-gray-300 rounded-xl focus:ring-primary focus:border-primary text-sm">
              </div>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">ស្ថានភាព (Status)</label>
              <select v-model="newContract.status" class="w-full p-2.5 border border-gray-300 rounded-xl focus:ring-primary focus:border-primary text-sm bg-white">
                <option value="Active">Active (កំពុងដំណើរការ)</option>
                <option value="Expired">Expired (ផុតកំណត់)</option>
              </select>
            </div>
            
            <div class="pt-4 flex gap-3">
              <button type="button" @click="showModal = false" class="flex-1 bg-gray-100 text-gray-700 py-3 rounded-xl font-bold hover:bg-gray-200 transition-colors text-sm">បោះបង់</button>
              <button type="submit" class="flex-1 bg-primary text-white py-3 rounded-xl font-bold hover:bg-secondary transition-colors shadow-lg shadow-primary/25 text-sm">រក្សាទុក</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

