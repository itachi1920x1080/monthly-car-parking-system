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
