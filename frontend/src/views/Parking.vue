<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const parkingRecords = ref([]);
const userName = ref('Admin');

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
      alert("សោររបស់អ្នកផុតកំណត់ហើយ! សូម Login ម្តងទៀត។");
      handleLogout();
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
    // ហៅ API Check-out
    await axios.put(`http://127.0.0.1:8000/parking/check-out/${recordId}`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    // ទាញទិន្នន័យសាជាថ្មី ដើម្បីឲ្យវាលោតម៉ោងចេញ និងបាត់ប៊ូតុង
    await fetchParkingRecords();
  } catch (error) {
    const msg = error.response?.data?.detail || "មានបញ្ហាក្នុងការ Check-out!";
    alert(typeof msg === 'string' ? msg : JSON.stringify(msg));
  }
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
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
  <div class="flex h-screen bg-gray-50 font-sans text-gray-800">
    
    <!-- របារចំហៀង (Sidebar) ដដែល -->
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
        <router-link to="/parking" class="flex items-center gap-3 px-4 py-3 bg-white/10 text-white rounded-lg font-medium transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" /></svg>
          Parking
        </router-link>
        <router-link to="/contracts" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-lg font-medium transition-colors">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
          Contracts
        </router-link>
        <router-link to="/payments" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-lg font-medium transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" /></svg>
          Payments
        </router-link>
      </nav>
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
        <h2 class="text-xl font-bold text-gray-800">Parking Records</h2>
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-bold shadow-sm">A</div>
          <span class="font-bold text-gray-700">{{ userName }}</span>
        </div>
      </header>

      <!-- តារាងចំណតឡាន -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-8">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center">
            <div>
              <h3 class="text-lg font-bold text-gray-800">ប្រវត្តិចេញចូលចំណត (Check-in / Check-out)</h3>
              <p class="text-xs text-gray-400 mt-0.5">កត់ត្រា និងគ្រប់គ្រងរថយន្តចេញចូលចំណតប្រចាំថ្ងៃ</p>
            </div>
            <button @click="showModal = true" class="bg-info text-white px-4 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center gap-2 shadow-sm text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
              កត់ត្រាឡានចូល (Check-in)
            </button>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-gray-500">
              <thead class="text-xs text-gray-700 uppercase bg-gray-50 border-b border-gray-100">
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
                  <td class="px-6 py-4 font-medium text-gray-900">#{{ record.id }}</td>
                  <td class="px-6 py-4 font-medium text-gray-700">#{{ record.customer_id }}</td>
                  <td class="px-6 py-4 font-bold text-gray-800 font-mono tracking-wider">{{ record.license_plate }}</td>
                  <td class="px-6 py-4 text-emerald-600 font-medium text-xs">{{ formatDate(record.check_in_time) }}</td>
                  <td class="px-6 py-4 text-xs" :class="record.check_out_time ? 'text-red-500 font-medium' : 'text-gray-400 italic'">
                    {{ formatDate(record.check_out_time) }}
                  </td>
                  <td class="px-6 py-4 text-center">
                    <!-- បើឡានមិនទាន់ចេញ បង្ហាញប៊ូតុង Check-out -->
                    <button v-if="!record.check_out_time" @click="handleCheckOut(record.id)" class="px-3.5 py-1.5 bg-warning hover:bg-amber-600 text-white rounded-lg text-xs font-bold transition-colors shadow-sm inline-flex items-center gap-1.5">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-3.5 h-3.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" /></svg>
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
      <div v-if="showModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
            <h3 class="text-lg font-bold text-gray-800">កត់ត្រាឡានចូលចំណត</h3>
            <button @click="showModal = false" class="text-gray-400 hover:text-red-500 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
          
          <form @submit.prevent="handleCheckIn" class="p-6 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">លេខសម្គាល់អតិថិជន (Customer ID)</label>
              <input v-model.number="newRecord.customer_id" type="number" required class="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary text-sm" placeholder="ឧទាហរណ៍៖ 1">
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">ស្លាកលេខរថយន្ត (License Plate)</label>
              <input v-model="newRecord.license_plate" type="text" required class="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary uppercase text-sm font-mono" placeholder="ឧទាហរណ៍៖ PP-9999">
            </div>
            
            <div class="pt-4 flex gap-3">
              <button type="button" @click="showModal = false" class="flex-1 bg-gray-100 text-gray-700 py-2.5 rounded-lg font-medium hover:bg-gray-200 transition-colors text-sm">
                បោះបង់ (Cancel)
              </button>
              <button type="submit" class="flex-1 bg-info text-white py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors text-sm shadow-sm">
                បញ្ជាក់ការចូល (Check-in)
              </button>
            </div>
          </form>
        </div>
      </div>
      <!-- ចប់ Modal -->

    </div>
  </div>
</template>
