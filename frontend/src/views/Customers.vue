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
      <nav class="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
        <router-link to="/dashboard" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-lg font-medium transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" /></svg>
          Dashboard
        </router-link>
        <router-link to="/customers" class="flex items-center gap-3 px-4 py-3 bg-white/10 text-white rounded-lg font-medium transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 002.625.372 9.337 9.337 0 004.121-.952 4.125 4.125 0 00-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 018.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0111.964-3.07M12 6.375a3.375 3.375 0 11-6.75 0 3.375 3.375 0 016.75 0zm8.25 2.25a2.625 2.625 0 11-5.25 0 2.625 2.625 0 015.25 0z" /></svg>
          Customers
        </router-link>
        <router-link to="/parking" class="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-white/5 hover:text-white rounded-lg font-medium transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" /></svg>
          Parking
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
