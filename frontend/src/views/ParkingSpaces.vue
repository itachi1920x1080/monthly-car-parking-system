<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const userName = ref('Admin');
const selectedZone = ref('All'); // All, A, B, C, D
const selectedFilter = ref('All'); // All, Available, Occupied

const parkingRecords = ref([]);
const totalSpaces = 80;

// បង្កើតបញ្ជីចំណតសរុប ៨០ កន្លែង (A-01 -> D-20)
const zones = ['A', 'B', 'C', 'D'];
const spaces = ref([]);

const generateSpaces = () => {
  const list = [];
  zones.forEach(z => {
    for (let i = 1; i <= 20; i++) {
      const spaceId = `${z}-${i.toString().padStart(2, '0')}`;
      list.push({
        id: spaceId,
        zone: z,
        number: i,
        status: 'Available',
        plate_number: null,
        vehicle_type: null
      });
    }
  });
  return list;
};

const fetchParkingData = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get('http://127.0.0.1:8000/parking/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    parkingRecords.value = response.data;
    
    // បញ្ចូលស្ថានភាពរថយន្តកំពុងចតចូលទៅក្នុង Slot ចំណត
    const baseSpaces = generateSpaces();
    const activeParkings = parkingRecords.value.filter(p => !p.check_out_time);
    
    // សម្គាល់ឡានកំពុងចត
    activeParkings.forEach((p, idx) => {
      // ប្រសិនបើរថយន្តមាន space_id ឬយើងផ្គូផ្គងតាមលំដាប់
      const slotIndex = idx % 80;
      baseSpaces[slotIndex].status = 'Occupied';
      baseSpaces[slotIndex].plate_number = p.plate_number;
      baseSpaces[slotIndex].vehicle_type = p.vehicle_type;
    });

    spaces.value = baseSpaces;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      handleLogout();
    }
  }
};

const filteredSpaces = computed(() => {
  return spaces.value.filter(s => {
    const matchZone = selectedZone.value === 'All' || s.zone === selectedZone.value;
    const matchFilter = selectedFilter.value === 'All' || s.status === selectedFilter.value;
    return matchZone && matchFilter;
  });
});

const occupiedCount = computed(() => spaces.value.filter(s => s.status === 'Occupied').length);
const availableCount = computed(() => totalSpaces - occupiedCount.value);

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

onMounted(() => {
  spaces.value = generateSpaces();
  fetchParkingData();
});
</script>

<template>
  <div class="flex h-screen bg-[#f8fafc] font-sans text-gray-800">
    <!-- Sidebar -->
    <aside class="w-[260px] bg-primary text-white flex flex-col transition-all duration-300 z-20 shrink-0 shadow-xl">
      <div class="h-20 flex items-center px-6 border-b border-white/5">
        <div class="w-10 h-10 bg-white text-primary rounded-xl flex items-center justify-center font-bold text-2xl mr-3 shadow-md">P</div>
        <div>
          <h1 class="font-bold text-xl tracking-wide">Car<span class="text-green-400">Park</span></h1>
          <p class="text-[9px] text-gray-300 uppercase tracking-wider font-medium">Management System</p>
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
      
      <div class="p-5 border-t border-white/10">
        <p class="text-[10px] text-gray-300 mb-3 opacity-60">Version 1.0.0</p>
        <button @click="handleLogout" class="w-full flex items-center gap-2 text-red-400 hover:text-red-300 hover:bg-white/5 px-3 py-2 rounded-xl transition-colors font-medium text-sm">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          Logout
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden relative">
      <header class="h-20 bg-white border-b border-gray-100 flex items-center justify-between px-8 z-10">
        <div class="flex items-center gap-3">
          <h2 class="text-xl font-bold text-gray-800">ប្លង់កន្លែងចតរថយន្ត (Parking Spaces)</h2>
          <span class="px-2.5 py-1 text-xs font-bold bg-green-50 text-green-700 rounded-full">
            ទំនេរ {{ availableCount }} / {{ totalSpaces }}
          </span>
        </div>
        
        <div class="flex items-center gap-6">
          <div class="flex items-center gap-4 text-xs font-semibold">
            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-md bg-emerald-500"></span> ទំនេរ (Available)</span>
            <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-md bg-rose-500"></span> មានឡានចត (Occupied)</span>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-full bg-primary text-white flex items-center justify-center font-bold text-sm shadow-sm">A</div>
            <div>
              <p class="text-sm font-bold text-gray-800 leading-tight">{{ userName }}</p>
              <p class="text-xs text-gray-500">Administrator</p>
            </div>
          </div>
        </div>
      </header>

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        <!-- Filter Controls -->
        <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-gray-400 uppercase tracking-wider mr-2">Zone:</span>
            <button 
              v-for="z in ['All', 'A', 'B', 'C', 'D']" 
              :key="z"
              @click="selectedZone = z"
              :class="selectedZone === z ? 'bg-primary text-white font-bold' : 'bg-white text-gray-600 hover:bg-gray-100'"
              class="px-3.5 py-1.5 rounded-xl text-xs transition-colors border border-gray-200 shadow-2xs"
            >
              Zone {{ z }}
            </button>
          </div>

          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-gray-400 uppercase tracking-wider mr-2">Status:</span>
            <button 
              v-for="f in ['All', 'Available', 'Occupied']" 
              :key="f"
              @click="selectedFilter = f"
              :class="selectedFilter === f ? 'bg-primary text-white font-bold' : 'bg-white text-gray-600 hover:bg-gray-100'"
              class="px-3.5 py-1.5 rounded-xl text-xs transition-colors border border-gray-200 shadow-2xs"
            >
              {{ f }}
            </button>
          </div>
        </div>

        <!-- 80 Slots Parking Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-8 xl:grid-cols-10 gap-3">
          <div 
            v-for="space in filteredSpaces" 
            :key="space.id"
            :class="[
              'p-3 rounded-2xl border flex flex-col justify-between h-28 transition-all hover:scale-105 select-none shadow-2xs',
              space.status === 'Occupied' 
                ? 'bg-rose-50/70 border-rose-200 text-rose-900' 
                : 'bg-emerald-50/70 border-emerald-200 text-emerald-900'
            ]"
          >
            <div class="flex items-center justify-between">
              <span class="font-mono font-extrabold text-sm">{{ space.id }}</span>
              <span 
                class="w-2.5 h-2.5 rounded-full"
                :class="space.status === 'Occupied' ? 'bg-rose-500' : 'bg-emerald-500'"
              ></span>
            </div>

            <div class="text-center my-auto">
              <span v-if="space.status === 'Occupied'" class="text-xl">🚗</span>
              <span v-else class="text-xs font-bold text-emerald-700/80">Available</span>
            </div>

            <div class="text-[10px] truncate font-mono text-center font-bold" :class="space.status === 'Occupied' ? 'text-rose-700' : 'text-emerald-600'">
              {{ space.plate_number || 'Slot ទំនេរ' }}
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
