<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

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
  <aside class="w-[260px] bg-primary text-white flex flex-col transition-all duration-300 z-20 shrink-0 shadow-xl select-none">
    <!-- Brand Logo -->
    <div class="h-20 flex items-center px-6 border-b border-white/5">
      <div class="w-10 h-10 bg-white text-primary rounded-xl flex items-center justify-center font-bold text-2xl mr-3 shadow-md shrink-0">
        P
      </div>
      <div class="overflow-hidden">
        <h1 class="font-bold text-xl tracking-wide">Car<span class="text-green-400">Park</span></h1>
        <p class="text-[9px] text-gray-300 uppercase tracking-wider font-medium">Management System</p>
      </div>
    </div>

    <!-- Role Indicator Badge -->
    <div class="px-5 pt-4 pb-2">
      <div 
        class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-semibold border"
        :class="{
          'bg-purple-500/20 text-purple-200 border-purple-400/30': isAdmin,
          'bg-blue-500/20 text-blue-200 border-blue-400/30': isCashier,
          'bg-emerald-500/20 text-emerald-200 border-emerald-400/30': isCustomer
        }"
      >
        <span class="w-2 h-2 rounded-full" :class="{ 'bg-purple-400': isAdmin, 'bg-blue-400': isCashier, 'bg-emerald-400': isCustomer }"></span>
        <span class="truncate">{{ roleDisplayName }} Mode</span>
      </div>
    </div>
    
    <!-- Navigation Links -->
    <nav class="flex-1 px-4 py-2 space-y-1 overflow-y-auto text-sm font-medium">
      <!-- 1. Dashboard (All) -->
      <router-link to="/dashboard" active-class="bg-white/10 text-white font-semibold shadow-inner" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
        <svg class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
        <span>Dashboard</span>
      </router-link>

      <!-- 2. Users (Admin Only) -->
      <router-link v-if="isAdmin" to="/users" active-class="bg-white/10 text-white font-semibold shadow-inner" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
        <svg class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
        <span>Users</span>
        <span class="ml-auto text-[10px] bg-purple-500/30 text-purple-200 px-1.5 py-0.5 rounded font-bold">Admin</span>
      </router-link>

      <!-- 3. Customers (Admin & Cashier) -->
      <router-link v-if="isAdmin || isCashier" to="/customers" active-class="bg-white/10 text-white font-semibold shadow-inner" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
        <svg class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
        <span>Customers</span>
      </router-link>

      <!-- 4. Vehicles / Parking Records (Admin & Cashier) -->
      <router-link v-if="isAdmin || isCashier" to="/parking" active-class="bg-white/10 text-white font-semibold shadow-inner" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
        <svg class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7h12.5M8 7v8.5A2.5 2.5 0 0010.5 18h3.8M8 7l-4.5 4.5M20.5 7v11M16 11h4.5M16 14.5h4.5" /></svg>
        <span>Vehicles</span>
      </router-link>

      <!-- 5. Parking Spaces (All) -->
      <router-link to="/spaces" active-class="bg-white/10 text-white font-semibold shadow-inner" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
        <svg class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" /></svg>
        <span>Parking Spaces</span>
      </router-link>

      <!-- 6. Contracts (All) -->
      <router-link to="/contracts" active-class="bg-white/10 text-white font-semibold shadow-inner" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
        <svg class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
        <span>{{ isCustomer ? 'My Contracts' : 'Contracts' }}</span>
      </router-link>

      <!-- 7. Payments (All) -->
      <router-link to="/payments" active-class="bg-white/10 text-white font-semibold shadow-inner" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
        <svg class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>
        <span>{{ isCustomer ? 'My Payments / KHQR' : 'Payments' }}</span>
      </router-link>

      <!-- 8. Notifications (All) -->
      <router-link to="/notifications" active-class="bg-white/10 text-white font-semibold shadow-inner" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
        <svg class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
        <span>Notifications</span>
      </router-link>

      <!-- 9. Reports (Admin & Cashier) -->
      <router-link v-if="isAdmin || isCashier" to="/reports" active-class="bg-white/10 text-white font-semibold shadow-inner" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
        <svg class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>
        <span>Reports</span>
      </router-link>

      <!-- 10. Settings (Admin Only) -->
      <router-link v-if="isAdmin" to="/settings" active-class="bg-white/10 text-white font-semibold shadow-inner" class="flex items-center gap-3 px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
        <svg class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
        <span>Settings</span>
        <span class="ml-auto text-[10px] bg-purple-500/30 text-purple-200 px-1.5 py-0.5 rounded font-bold">Admin</span>
      </router-link>
    </nav>
    
    <!-- User Profile & Logout -->
    <div class="p-4 border-t border-white/10 bg-black/10">
      <div class="flex items-center gap-3 mb-3">
        <div 
          class="w-9 h-9 rounded-full flex items-center justify-center font-bold text-sm shadow-sm shrink-0"
          :class="{
            'bg-purple-500 text-white': isAdmin,
            'bg-blue-500 text-white': isCashier,
            'bg-emerald-500 text-white': isCustomer
          }"
        >
          {{ userName.charAt(0).toUpperCase() }}
        </div>
        <div class="overflow-hidden">
          <p class="text-sm font-semibold truncate">{{ userName }}</p>
          <p class="text-[11px] text-gray-300 truncate">{{ roleDisplayName }}</p>
        </div>
      </div>
      <button 
        @click="handleLogout" 
        class="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-lg bg-white/5 hover:bg-red-500/20 text-gray-300 hover:text-red-300 transition-colors font-medium text-xs border border-white/5"
      >
        <svg class="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
        <span>Logout (ចាកចេញ)</span>
      </button>
    </div>
  </aside>
</template>
