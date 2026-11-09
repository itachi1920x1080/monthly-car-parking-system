<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const customers = ref([]);
const userName = ref('Admin');

// អថេរសម្រាប់គ្រប់គ្រងផ្ទាំង Popup និងទិន្នន័យអតិថិជនថ្មី
const showModal = ref(false);
const newCustomer = ref({
  first_name: '',
  last_name: '',
  phone_number: '',
  email: ''
});

// អនុគមន៍ទាញយកទិន្នន័យ
const fetchCustomers = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://127.0.0.1:8000/customers/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    customers.value = response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      alert("សោររបស់អ្នកផុតកំណត់ហើយ! សូម Login ម្តងទៀត។");
      handleLogout();
    }
  }
};

// អនុគមន៍បង្កើតអតិថិជនថ្មី
const createCustomer = async () => {
  try {
    const token = localStorage.getItem('token');
    const payload = {
      ...newCustomer.value,
      email: newCustomer.value.email?.trim() || null
    };
    await axios.post('http://127.0.0.1:8000/customers/', payload, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    // បិទ Popup វិញ និងសម្អាតទិន្នន័យក្នុងប្រអប់
    showModal.value = false;
    newCustomer.value = { first_name: '', last_name: '', phone_number: '', email: '' };
    
    // ទាញយកទិន្នន័យសារជាថ្មីដើម្បីបង្ហាញក្នុងតារាងភ្លាមៗ
    await fetchCustomers();
    alert("បង្កើតអតិថិជនថ្មីបានជោគជ័យ!");
  } catch (error) {
    const msg = error.response?.data?.detail || "មានបញ្ហាក្នុងការបង្កើតអតិថិជន! សូមពិនិត្យមើលទិន្នន័យឡើងវិញ។";
    alert(typeof msg === 'string' ? msg : JSON.stringify(msg));
  }
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

onMounted(() => {
  fetchCustomers();
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
        <h2 class="text-xl font-bold text-gray-800">Customers Management</h2>
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-full bg-primary text-white flex items-center justify-center font-bold">A</div>
          <span class="font-bold text-gray-700">{{ userName }}</span>
        </div>
      </header>

      <!-- តារាងទិន្នន័យអតិថិជន -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 p-8">
        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center">
            <h3 class="text-lg font-bold text-gray-800">បញ្ជីអតិថិជន (Customer List)</h3>
            <!-- ប៊ូតុងបើក Modal -->
            <button @click="showModal = true" class="bg-primary text-white px-4 py-2 rounded-lg font-medium hover:bg-secondary transition-colors flex items-center gap-2 shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
              + បន្ថែមអតិថិជនថ្មី
            </button>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-gray-500">
              <thead class="text-xs text-gray-700 uppercase bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-4">ID</th>
                  <th scope="col" class="px-6 py-4">ឈ្មោះ (First Name)</th>
                  <th scope="col" class="px-6 py-4">ត្រកូល (Last Name)</th>
                  <th scope="col" class="px-6 py-4">លេខទូរស័ព្ទ</th>
                  <th scope="col" class="px-6 py-4">អ៊ីមែល</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="customers.length === 0">
                  <td colspan="5" class="px-6 py-8 text-center text-gray-400">មិនមានទិន្នន័យអតិថិជននៅឡើយទេ...</td>
                </tr>
                <tr v-for="cus in customers" :key="cus.id" class="border-b hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-4 font-medium text-gray-900">#{{ cus.id }}</td>
                  <td class="px-6 py-4">{{ cus.first_name }}</td>
                  <td class="px-6 py-4">{{ cus.last_name }}</td>
                  <td class="px-6 py-4 font-mono text-xs">{{ cus.phone_number }}</td>
                  <td class="px-6 py-4">{{ cus.email || '-' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>

      <!-- ផ្ទាំង Popup (Modal) សម្រាប់បញ្ចូលអតិថិជនថ្មី -->
      <div v-if="showModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
            <h3 class="text-lg font-bold text-gray-800">ចុះឈ្មោះអតិថិជនថ្មី</h3>
            <button @click="showModal = false" class="text-gray-400 hover:text-red-500 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
          
          <form @submit.prevent="createCustomer" class="p-6 space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">នាមត្រកូល (Last Name)</label>
                <input v-model="newCustomer.last_name" type="text" required class="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary text-sm" placeholder="ឧ. សុខ">
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">នាមខ្លួន (First Name)</label>
                <input v-model="newCustomer.first_name" type="text" required class="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary text-sm" placeholder="ឧ. ចាន់">
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">លេខទូរស័ព្ទ (Phone Number)</label>
              <input v-model="newCustomer.phone_number" type="text" required class="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary text-sm" placeholder="012345678">
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">អ៊ីមែល (Email) - មិនចាំបាច់ក៏បាន</label>
              <input v-model="newCustomer.email" type="email" class="w-full p-2.5 border border-gray-300 rounded-lg focus:ring-primary focus:border-primary text-sm" placeholder="name@example.com">
            </div>
            
            <div class="pt-4 flex gap-3">
              <button type="button" @click="showModal = false" class="flex-1 bg-gray-100 text-gray-700 py-2.5 rounded-lg font-medium hover:bg-gray-200 transition-colors text-sm">
                បោះបង់ (Cancel)
              </button>
              <button type="submit" class="flex-1 bg-primary text-white py-2.5 rounded-lg font-medium hover:bg-secondary transition-colors text-sm shadow-sm">
                រក្សាទុក (Save)
              </button>
            </div>
          </form>
        </div>
      </div>
      <!-- ចប់ Modal -->

    </div>
  </div>
</template>
