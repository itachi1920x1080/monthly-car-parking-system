<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Sidebar from '../components/Sidebar.vue';
import Navbar from '../components/Navbar.vue';

const router = useRouter();
const users = ref([]);
const showModal = ref(false);
const newUser = ref({
  username: '',
  email: '',
  password: '',
  role: 'cashier'
});

const userRole = ref((localStorage.getItem('user_role') || 'admin').toLowerCase());

const fetchUsers = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://127.0.0.1:8000/users/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    users.value = response.data;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      router.push('/login');
    }
  }
};

const createUser = async () => {
  try {
    const token = localStorage.getItem('token');
    const payload = {
      username: newUser.value.username.trim(),
      email: newUser.value.email.trim(),
      password: newUser.value.password,
      role: newUser.value.role || 'cashier'
    };
    await axios.post('http://127.0.0.1:8000/users/register', payload, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    showModal.value = false;
    newUser.value = { username: '', email: '', password: '', role: 'cashier' };
    await fetchUsers();
    alert('✅ បង្កើតគណនីអ្នកប្រើប្រាស់បានជោគជ័យ!');
  } catch (error) {
    let msg = 'មិនអាចបង្កើតគណនីបានទេ!';
    if (error.response?.data?.detail) {
      const detail = error.response.data.detail;
      if (Array.isArray(detail)) {
        msg = detail.map(d => d.msg || JSON.stringify(d)).join('\n');
      } else if (typeof detail === 'string') {
        msg = detail;
      } else {
        msg = JSON.stringify(detail);
      }
    }
    alert(msg);
  }
};

onMounted(() => {
  if (userRole.value !== 'admin') {
    alert('ទំព័រនេះសម្រាប់តែ Administrator ប៉ុណ្ណោះ!');
    router.push('/dashboard');
    return;
  }
  fetchUsers();
});
</script>

<template>
  <div class="flex h-screen bg-[#f8fafc] font-sans text-gray-800">
    <Sidebar />

    <div class="flex-1 flex flex-col overflow-hidden relative">
      <Navbar title="Users Management" subtitle="Home / Users" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        <!-- Title & Action Bar -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <div class="flex items-center gap-3">
              <h2 class="text-2xl font-extrabold text-gray-800">ការគ្រប់គ្រងអ្នកប្រើប្រាស់ (Users)</h2>
              <span class="px-2.5 py-0.5 rounded-full bg-purple-100 text-purple-700 text-xs font-bold border border-purple-200">Admin Only</span>
            </div>
            <p class="text-sm text-gray-500 mt-1">គ្រប់គ្រងគណនី Administrator, Cashier (បេឡា) និង Customer (អតិថិជន)</p>
          </div>
          <button 
            @click="showModal = true"
            class="px-5 py-2.5 bg-primary hover:bg-emerald-700 text-white rounded-xl font-bold text-sm shadow-md transition-all flex items-center gap-2"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
            + បង្កើត User ថ្មី
          </button>
        </div>

        <!-- Users Table Card -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-gray-100 bg-gray-50/50 text-[11px] font-bold text-gray-400 uppercase tracking-wider">
                <th class="px-6 py-4">ID</th>
                <th class="px-6 py-4">USERNAME</th>
                <th class="px-6 py-4">EMAIL</th>
                <th class="px-6 py-4">ROLE (តួនាទី)</th>
                <th class="px-6 py-4">STATUS</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 text-sm">
              <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50/60 transition-colors">
                <td class="px-6 py-4 font-mono text-gray-400 font-semibold">#USR-{{ user.id }}</td>
                <td class="px-6 py-4 font-bold text-gray-800 flex items-center gap-2.5">
                  <span 
                    class="w-7 h-7 rounded-full flex items-center justify-center font-bold text-xs"
                    :class="{
                      'bg-purple-100 text-purple-700': user.role?.toLowerCase() === 'admin',
                      'bg-blue-100 text-blue-700': user.role?.toLowerCase() === 'cashier',
                      'bg-emerald-100 text-emerald-700': user.role?.toLowerCase() === 'customer'
                    }"
                  >
                    {{ user.username?.charAt(0).toUpperCase() }}
                  </span>
                  <span>{{ user.username }}</span>
                </td>
                <td class="px-6 py-4 text-gray-600">{{ user.email }}</td>
                <td class="px-6 py-4">
                  <span 
                    class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold"
                    :class="{
                      'bg-purple-50 text-purple-700 border border-purple-200': user.role?.toLowerCase() === 'admin',
                      'bg-blue-50 text-blue-700 border border-blue-200': user.role?.toLowerCase() === 'cashier',
                      'bg-emerald-50 text-emerald-700 border border-emerald-200': user.role?.toLowerCase() === 'customer'
                    }"
                  >
                    <span 
                      class="w-1.5 h-1.5 rounded-full"
                      :class="{
                        'bg-purple-500': user.role?.toLowerCase() === 'admin',
                        'bg-blue-500': user.role?.toLowerCase() === 'cashier',
                        'bg-emerald-500': user.role?.toLowerCase() === 'customer'
                      }"
                    ></span>
                    {{ user.role?.toLowerCase() === 'admin' ? 'Administrator' : (user.role?.toLowerCase() === 'customer' ? 'Customer' : 'Cashier / Staff') }}
                  </span>
                </td>
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
      </main>
    </div>

    <!-- Modal Create User -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-xs p-4">
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
          <div>
            <h3 class="font-extrabold text-lg text-gray-800">បង្កើតគណនីអ្នកប្រើប្រាស់ថ្មី</h3>
            <p class="text-xs text-gray-500">ជ្រើសរើសតួនាទី Admin, Cashier ឬ Customer</p>
          </div>
          <button @click="showModal = false" class="text-gray-400 hover:text-gray-600 text-lg p-1">✕</button>
        </div>
        <form @submit.prevent="createUser" class="p-6 space-y-4">
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1.5">Username (ឈ្មោះគណនី)</label>
            <input v-model="newUser.username" required type="text" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary" placeholder="ឧ. cashier02">
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1.5">Email (អ៊ីមែល)</label>
            <input v-model="newUser.email" required type="email" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary" placeholder="ឧ. cashier02@carpark.com">
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1.5">Password (ពាក្យសម្ងាត់)</label>
            <input v-model="newUser.password" required type="password" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary" placeholder="••••••••">
          </div>
          <div>
            <label class="block text-xs font-bold text-gray-700 mb-1.5">Role (តួនាទី និងសិទ្ធិ)</label>
            <select v-model="newUser.role" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm bg-white focus:ring-primary focus:border-primary">
              <option value="cashier">Cashier / Staff (បេឡា/បុគ្គលិកច្រកចេញចូល)</option>
              <option value="admin">Administrator (អ្នកគ្រប់គ្រងប្រព័ន្ធ)</option>
              <option value="customer">Customer / User (អតិថិជនជួលចំណត)</option>
            </select>
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
