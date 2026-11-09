<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Sidebar from '../components/Sidebar.vue';
import Navbar from '../components/Navbar.vue';

const router = useRouter();
const customers = ref([]);
const showModal = ref(false);
const newCustomer = ref({
  first_name: '',
  last_name: '',
  phone_number: '',
  email: ''
});

const fetchCustomers = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://127.0.0.1:8000/customers/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    customers.value = response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      router.push('/login');
    }
  }
};

const createCustomer = async () => {
  try {
    const token = localStorage.getItem('token');
    await axios.post('http://127.0.0.1:8000/customers/', newCustomer.value, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    showModal.value = false;
    newCustomer.value = { first_name: '', last_name: '', phone_number: '', email: '' };
    await fetchCustomers();
    alert("បង្កើតអតិថិជនថ្មីបានជោគជ័យ!");
  } catch (error) {
    alert("មានបញ្ហាក្នុងការបង្កើតអតិថិជន! សូមពិនិត្យលេខទូរស័ព្ទម្តងទៀត។");
  }
};

onMounted(() => {
  fetchCustomers();
});
</script>

<template>
  <div class="flex h-screen bg-[#f8fafc] font-sans text-gray-800">
    <Sidebar />

    <div class="flex-1 flex flex-col overflow-hidden relative">
      <Navbar title="Customers Management" subtitle="Home / Customers" />

      <!-- តារាងទិន្នន័យអតិថិជន -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <h2 class="text-2xl font-extrabold text-gray-800">ការគ្រប់គ្រងអតិថិជន (Customers)</h2>
            <p class="text-sm text-gray-500 mt-1">បញ្ជីឈ្មោះអតិថិជនដែលបានចុះឈ្មោះប្រើប្រាស់សេវាចំណត</p>
          </div>
          <button 
            @click="showModal = true" 
            class="px-5 py-2.5 bg-primary hover:bg-emerald-700 text-white rounded-xl font-bold text-sm shadow-md transition-all flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
            + បន្ថែមអតិថិជនថ្មី
          </button>
        </div>

        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-gray-600">
              <thead class="text-xs text-gray-400 uppercase bg-gray-50/50 border-b border-gray-100">
                <tr>
                  <th scope="col" class="px-6 py-4">ID</th>
                  <th scope="col" class="px-6 py-4">ឈ្មោះ (First Name)</th>
                  <th scope="col" class="px-6 py-4">ត្រកូល (Last Name)</th>
                  <th scope="col" class="px-6 py-4">លេខទូរស័ព្ទ</th>
                  <th scope="col" class="px-6 py-4">អ៊ីមែល</th>
                  <th scope="col" class="px-6 py-4">ស្ថានភាព</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-if="customers.length === 0">
                  <td colspan="6" class="px-6 py-8 text-center text-gray-400">មិនមានទិន្នន័យអតិថិជននៅឡើយទេ...</td>
                </tr>
                <tr v-for="cus in customers" :key="cus.id" class="hover:bg-gray-50/60 transition-colors">
                  <td class="px-6 py-4 font-mono text-gray-400 font-semibold">#CUS-{{ cus.id }}</td>
                  <td class="px-6 py-4 font-bold text-gray-800">{{ cus.first_name }}</td>
                  <td class="px-6 py-4 font-bold text-gray-800">{{ cus.last_name }}</td>
                  <td class="px-6 py-4 font-mono text-xs">{{ cus.phone_number }}</td>
                  <td class="px-6 py-4 text-gray-500">{{ cus.email || '-' }}</td>
                  <td class="px-6 py-4">
                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-green-50 text-green-700 rounded-full text-xs font-semibold border border-green-200">
                      <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span>
                      Active
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>

    <!-- Modal បន្ថែមអតិថិជនថ្មី -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 backdrop-blur-xs flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl p-6 w-full max-w-md shadow-2xl animate-in fade-in zoom-in-95 duration-200">
        <div class="flex justify-between items-center mb-6 border-b border-gray-100 pb-4">
          <h3 class="text-lg font-extrabold text-gray-800">បន្ថែមអតិថិជនថ្មី</h3>
          <button @click="showModal = false" class="text-gray-400 hover:text-gray-600 text-lg">✕</button>
        </div>
        
        <form @submit.prevent="createCustomer" class="space-y-4">
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1.5">ឈ្មោះ (First Name)</label>
            <input v-model="newCustomer.first_name" type="text" required class="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl focus:ring-primary focus:border-primary text-sm" placeholder="ឧ. Sok">
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1.5">ត្រកូល (Last Name)</label>
            <input v-model="newCustomer.last_name" type="text" required class="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl focus:ring-primary focus:border-primary text-sm" placeholder="ឧ. Chan">
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1.5">លេខទូរស័ព្ទ</label>
            <input v-model="newCustomer.phone_number" type="text" required class="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl focus:ring-primary focus:border-primary text-sm" placeholder="ឧ. 012345678">
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1.5">អ៊ីមែល (បើមាន)</label>
            <input v-model="newCustomer.email" type="email" class="w-full px-3.5 py-2.5 border border-gray-300 rounded-xl focus:ring-primary focus:border-primary text-sm" placeholder="ឧ. sokchan@gmail.com">
          </div>

          <div class="flex justify-end gap-3 pt-4 border-t border-gray-100">
            <button type="button" @click="showModal = false" class="px-4 py-2.5 border border-gray-200 rounded-xl text-sm font-semibold text-gray-600 hover:bg-gray-50 transition-colors">បោះបង់</button>
            <button type="submit" class="px-5 py-2.5 bg-primary text-white rounded-xl text-sm font-bold hover:bg-emerald-700 shadow-md transition-colors">រក្សាទុក</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>
