<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  title: {
    type: String,
    default: 'Dashboard'
  },
  subtitle: {
    type: String,
    default: 'Home / Dashboard'
  }
});

const router = useRouter();
const userRole = ref(localStorage.getItem('user_role') || 'admin');
const userName = ref(localStorage.getItem('user_name') || 'Admin');

const isAdmin = computed(() => userRole.value.toLowerCase() === 'admin');
const isCashier = computed(() => userRole.value.toLowerCase() === 'cashier');
const isCustomer = computed(() => userRole.value.toLowerCase() === 'customer');

const roleDisplayName = computed(() => {
  if (isAdmin.value) return 'Administrator';
  if (isCashier.value) return 'Cashier / Staff';
  return 'Customer';
});

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user_role');
  localStorage.removeItem('user_name');
  router.push('/login');
};
</script>

<template>
  <header class="h-20 bg-white border-b border-gray-100 flex items-center justify-between px-8 z-10 shrink-0 select-none">
    <!-- Left: Breadcrumb / Search -->
    <div class="relative w-72 md:w-96">
      <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
      </div>
      <input 
        type="text" 
        class="w-full bg-gray-50/70 border border-gray-200 text-gray-900 text-sm rounded-full focus:ring-primary focus:border-primary block pl-10 pr-4 py-2 transition-shadow placeholder:text-gray-400" 
        placeholder="ស្វែងរកទិន្នន័យ (Search)..."
      >
    </div>
    
    <!-- Right Actions -->
    <div class="flex items-center gap-5">
      <!-- Notification Icon -->
      <router-link to="/notifications" class="text-gray-400 hover:text-primary transition-colors relative p-2 rounded-full hover:bg-gray-100">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
        <span class="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full"></span>
      </router-link>
      
      <!-- Profile Header -->
      <div class="flex items-center gap-3 pl-3 border-l border-gray-200">
        <div 
          class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm shadow-sm border-2 border-white"
          :class="{
            'bg-purple-600 text-white shadow-purple-100': isAdmin,
            'bg-blue-600 text-white shadow-blue-100': isCashier,
            'bg-emerald-600 text-white shadow-emerald-100': isCustomer
          }"
        >
          {{ userName.charAt(0).toUpperCase() }}
        </div>
        <div class="text-left hidden sm:block">
          <p class="text-sm font-bold text-gray-800 leading-tight">{{ userName }}</p>
          <span 
            class="inline-block text-[10px] font-semibold px-2 py-0.5 rounded-full mt-0.5"
            :class="{
              'bg-purple-100 text-purple-700': isAdmin,
              'bg-blue-100 text-blue-700': isCashier,
              'bg-emerald-100 text-emerald-700': isCustomer
            }"
          >
            {{ roleDisplayName }}
          </span>
        </div>
      </div>
    </div>
  </header>
</template>
