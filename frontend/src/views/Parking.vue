<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Sidebar from '../components/Sidebar.vue';
import Navbar from '../components/Navbar.vue';

const router = useRouter();
const parkingRecords = ref([]);

// អថេរសម្រាប់ Modal Check-in
const showModal = ref(false);
const newRecord = ref({
  customer_id: '',
  license_plate: ''
});

const fetchParkingRecords = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://127.0.0.1:8000/parking/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    parkingRecords.value = response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      router.push('/login');
    }
  }
};

// អនុគមន៍កត់ត្រាឡានចូល (Check-in)
const handleCheckIn = async () => {
  try {
    const token = localStorage.getItem('token');
    await axios.post('http://127.0.0.1:8000/parking/check-in', newRecord.value, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    showModal.value = false;
    newRecord.value = { customer_id: '', license_plate: '' };
    await fetchParkingRecords();
    alert("កត់ត្រាឡានចូលបានជោគជ័យ!");
  } catch (error) {
    const msg = error.response?.data?.detail || "មានបញ្ហា! សូមប្រាកដថាលេខអតិថិជននេះពិតជាមានក្នុងប្រព័ន្ធមែន។";
    alert(typeof msg === 'string' ? msg : JSON.stringify(msg));
  }
};

// អនុគមន៍បញ្ជាឲ្យឡានចេញ (Check-out)
const handleCheckOut = async (recordId) => {
  if (!confirm("តើលោកម្ចាស់ពិតជាចង់បញ្ជាឲ្យឡាននេះចេញមែនទេ?")) return;
  
  try {
    const token = localStorage.getItem('token');
    await axios.put(`http://127.0.0.1:8000/parking/check-out/${recordId}`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    await fetchParkingRecords();
  } catch (error) {
    const msg = error.response?.data?.detail || "មានបញ្ហាក្នុងការ Check-out!";
    alert(typeof msg === 'string' ? msg : JSON.stringify(msg));
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'កំពុងចត...';
  const date = new Date(dateString);
  return date.toLocaleString('en-GB'); 
};

onMounted(() => {
  fetchParkingRecords();
});
</script>

<template>
  <div class="flex h-screen bg-[#f8fafc] font-sans text-gray-800">
    <Sidebar />

    <div class="flex-1 flex flex-col overflow-hidden relative">
      <Navbar title="Vehicles (Parking Records)" subtitle="Home / Vehicles" />

      <!-- តារាងចំណតឡាន -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <h2 class="text-2xl font-extrabold text-gray-800">ប្រវត្តិចេញចូលយានយន្ត (Parking Records)</h2>
            <p class="text-sm text-gray-500 mt-1">កត់ត្រា និងគ្រប់គ្រងរថយន្តចេញចូលចំណតប្រចាំថ្ងៃ</p>
          </div>
          <button 
            @click="showModal = true" 
            class="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold text-sm shadow-md transition-all flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
            កត់ត្រាឡានចូល (Check-in)
          </button>
        </div>

        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-gray-600">
              <thead class="text-xs text-gray-400 uppercase bg-gray-50/50 border-b border-gray-100">
                <tr>
                  <th scope="col" class="px-6 py-4 font-semibold">ID</th>
                  <th scope="col" class="px-6 py-4 font-semibold">លេខអតិថិជន</th>
                  <th scope="col" class="px-6 py-4 font-semibold">ស្លាកលេខ</th>
                  <th scope="col" class="px-6 py-4 font-semibold">ម៉ោងចូល</th>
                  <th scope="col" class="px-6 py-4 font-semibold">ម៉ោងចេញ</th>
                  <th scope="col" class="px-6 py-4 text-center font-semibold">សកម្មភាព (Action)</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-if="parkingRecords.length === 0">
                  <td colspan="6" class="px-6 py-10 text-center text-gray-400">មិនមានប្រវត្តិចេញចូលនៅឡើយទេ...</td>
                </tr>
                <tr v-for="record in parkingRecords" :key="record.id" class="hover:bg-gray-50/80 transition-colors">
                  <td class="px-6 py-4 font-mono text-gray-400 font-semibold">#REC-{{ record.id }}</td>
                  <td class="px-6 py-4 font-bold text-gray-800">#CUS-{{ record.customer_id }}</td>
                  <td class="px-6 py-4 font-bold text-primary font-mono tracking-wider">{{ record.license_plate }}</td>
                  <td class="px-6 py-4 text-emerald-600 font-medium text-xs">{{ formatDate(record.check_in_time) }}</td>
                  <td class="px-6 py-4 text-xs" :class="record.check_out_time ? 'text-red-500 font-medium' : 'text-gray-400 italic'">
                    {{ formatDate(record.check_out_time) }}
                  </td>
                  <td class="px-6 py-4 text-center">
                    <!-- បើឡានមិនទាន់ចេញ បង្ហាញប៊ូតុង Check-out -->
                    <button 
                      v-if="!record.check_out_time" 
                      @click="handleCheckOut(record.id)" 
                      class="px-3.5 py-1.5 bg-amber-500 hover:bg-amber-600 text-white rounded-lg text-xs font-bold transition-colors shadow-sm inline-flex items-center gap-1.5"
                    >
                      <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
                      ចុចបញ្ជាឲ្យចេញ
                    </button>
                    <!-- បើឡានចេញហើយ បង្ហាញត្រឹម Badge -->
                    <span v-else class="px-3 py-1 bg-gray-100 text-gray-500 rounded-full text-xs font-semibold">
                      ចេញរួចរាល់
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>

      <!-- ផ្ទាំង Popup (Modal) សម្រាប់កត់ត្រាឡានចូល -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 backdrop-blur-xs z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
            <div>
              <h3 class="font-extrabold text-lg text-gray-800">កត់ត្រាឡានចូលចំណត</h3>
              <p class="text-xs text-gray-500">បញ្ចូលលេខ ID អតិថិជន និងស្លាកលេខ</p>
            </div>
            <button @click="showModal = false" class="text-gray-400 hover:text-gray-600 text-lg">✕</button>
          </div>
          
          <form @submit.prevent="handleCheckIn" class="p-6 space-y-4">
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1.5">លេខសម្គាល់អតិថិជន (Customer ID)</label>
              <input v-model.number="newRecord.customer_id" type="number" required class="w-full p-2.5 border border-gray-300 rounded-xl focus:ring-primary focus:border-primary text-sm" placeholder="ឧទាហរណ៍៖ 1">
            </div>
            
            <div>
              <label class="block text-xs font-bold text-gray-700 mb-1.5">ស្លាកលេខរថយន្ត (License Plate)</label>
              <input v-model="newRecord.license_plate" type="text" required class="w-full p-2.5 border border-gray-300 rounded-xl focus:ring-primary focus:border-primary uppercase text-sm font-mono" placeholder="ឧទាហរណ៍៖ PP-9999">
            </div>
            
            <div class="pt-4 flex gap-3 border-t border-gray-100">
              <button type="button" @click="showModal = false" class="flex-1 bg-gray-100 text-gray-700 py-2.5 rounded-xl font-bold hover:bg-gray-200 transition-colors text-sm">
                បោះបង់
              </button>
              <button type="submit" class="flex-1 bg-blue-600 text-white py-2.5 rounded-xl font-bold hover:bg-blue-700 transition-colors text-sm shadow-md">
                បញ្ជាក់ Check-in
              </button>
            </div>
          </form>
        </div>
      </div>

    </div>
  </div>
</template>
