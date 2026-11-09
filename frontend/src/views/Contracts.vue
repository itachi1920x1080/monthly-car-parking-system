<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Sidebar from '../components/Sidebar.vue';
import Navbar from '../components/Navbar.vue';

const router = useRouter();
const contracts = ref([]);
const customers = ref([]);

const showModal = ref(false);
const newContract = ref({
  customer_id: '',
  space_id: '',
  start_date: '',
  end_date: '',
  status: 'Active'
});

// ទាញយកបញ្ជីអតិថិជនដើម្បីបង្ហាញឈ្មោះ
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

// ទាញយកទិន្នន័យពិតពី Database
const fetchContracts = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://127.0.0.1:8000/contracts/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    contracts.value = response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      router.push('/login');
    }
  }
};

// បញ្ជូនទិន្នន័យទៅរក្សាទុកក្នុង MySQL
const createContract = async () => {
  try {
    const token = localStorage.getItem('token');
    await axios.post('http://127.0.0.1:8000/contracts/', {
      customer_id: parseInt(newContract.value.customer_id),
      space_id: newContract.value.space_id,
      start_date: newContract.value.start_date,
      end_date: newContract.value.end_date,
      status: newContract.value.status
    }, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    showModal.value = false;
    newContract.value = { customer_id: '', space_id: '', start_date: '', end_date: '', status: 'Active' };
    
    // Refresh តារាង
    await fetchContracts();
    alert("បង្កើតកិច្ចសន្យាថ្មីបានជោគជ័យ និងរក្សាទុកក្នុង Database រួចរាល់!");
  } catch (error) {
    const msg = error.response?.data?.detail || "មានបញ្ហា! សូមប្រាកដថាលេខអតិថិជននេះពិតជាមានក្នុងប្រព័ន្ធមែន។";
    alert(typeof msg === 'string' ? msg : JSON.stringify(msg));
  }
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
    <Sidebar />

    <div class="flex-1 flex flex-col overflow-hidden relative">
      <Navbar title="Contracts Management" subtitle="Home / Contracts" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <h2 class="text-2xl font-extrabold text-gray-800">ការគ្រប់គ្រងកិច្ចសន្យា (Contracts)</h2>
            <p class="text-sm text-gray-500 mt-1">សរុបមាន {{ contracts.length }} កិច្ចសន្យាជួលចំណតក្នុងប្រព័ន្ធ</p>
          </div>
          <button 
            @click="showModal = true" 
            class="px-5 py-2.5 bg-primary hover:bg-emerald-700 text-white rounded-xl font-bold text-sm shadow-md transition-all flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
            + បង្កើតកិច្ចសន្យាថ្មី
          </button>
        </div>

        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-gray-600">
              <thead class="text-xs text-gray-400 uppercase bg-gray-50/50 border-b border-gray-100">
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
                <tr v-if="contracts.length === 0">
                  <td colspan="6" class="px-6 py-8 text-center text-gray-400">មិនទាន់មានកិច្ចសន្យានៅឡើយទេ...</td>
                </tr>
                <tr v-for="contract in contracts" :key="contract.id" class="hover:bg-gray-50/80 transition-colors">
                  <td class="px-6 py-4 font-bold font-mono text-gray-900">#CT-{{ contract.id.toString().padStart(3, '0') }}</td>
                  <td class="px-6 py-4 font-medium text-gray-700">
                    <div class="font-bold text-gray-800">{{ getCustomerName(contract.customer_id) }}</div>
                    <div class="text-xs text-gray-400 font-mono">ID: #CUS-{{ contract.customer_id }}</div>
                  </td>
                  <td class="px-6 py-4 font-bold text-primary font-mono">{{ contract.space_id }}</td>
                  <td class="px-6 py-4 font-mono text-gray-600 text-xs">{{ formatDate(contract.start_date) }}</td>
                  <td class="px-6 py-4 font-mono text-gray-600 text-xs">{{ formatDate(contract.end_date) }}</td>
                  <td class="px-6 py-4">
                    <span v-if="contract.status === 'Active'" class="inline-flex items-center gap-1.5 px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-bold border border-green-200">
                      <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span>
                      Active
                    </span>
                    <span v-else class="inline-flex items-center gap-1.5 px-3 py-1 bg-red-50 text-red-700 rounded-full text-xs font-bold border border-red-200">
                      <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                      {{ contract.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>

      <!-- Modal បង្កើតកិច្ចសន្យាថ្មី -->
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
        <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
            <div>
              <h3 class="font-extrabold text-lg text-gray-800">បង្កើតកិច្ចសន្យាថ្មី</h3>
              <p class="text-xs text-gray-500">ភ្ជាប់អតិថិជនទៅនឹងទីតាំងចំណតជាក់លាក់</p>
            </div>
            <button @click="showModal = false" class="text-gray-400 hover:text-gray-600 text-lg">✕</button>
          </div>
          
          <form @submit.prevent="createContract" class="p-6 space-y-4">
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1.5">លេខកូដអតិថិជន (Customer ID)</label>
              <input v-model="newContract.customer_id" type="number" required placeholder="ឧទាហរណ៍៖ 1" class="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
            </div>

            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1.5">ទីតាំងចំណត (Space Code)</label>
              <input v-model="newContract.space_id" type="text" required placeholder="ឧទាហរណ៍៖ A-01" class="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl text-sm font-mono uppercase focus:ring-primary focus:border-primary">
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-gray-700 mb-1.5">ថ្ងៃចាប់ផ្តើម</label>
                <input v-model="newContract.start_date" type="date" required class="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-700 mb-1.5">ថ្ងៃផុតកំណត់</label>
                <input v-model="newContract.end_date" type="date" required class="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
              </div>
            </div>

            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1.5">ស្ថានភាព (Status)</label>
              <select v-model="newContract.status" class="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl text-sm bg-white focus:ring-primary focus:border-primary">
                <option value="Active">Active (សកម្ម)</option>
                <option value="Terminated">Terminated (បានបញ្ចប់)</option>
              </select>
            </div>

            <div class="pt-4 flex gap-3 border-t border-gray-100">
              <button type="button" @click="showModal = false" class="flex-1 bg-gray-100 text-gray-700 py-2.5 rounded-xl font-bold hover:bg-gray-200 transition-colors text-sm">
                បោះបង់
              </button>
              <button type="submit" class="flex-1 bg-primary text-white py-2.5 rounded-xl font-bold hover:bg-emerald-700 transition-colors text-sm shadow-md">
                រក្សាទុកកិច្ចសន្យា
              </button>
            </div>
          </form>
        </div>
      </div>

    </div>
  </div>
</template>
