<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Sidebar from '../components/Sidebar.vue';
import Navbar from '../components/Navbar.vue';

const router = useRouter();
const selectedZone = ref('All'); // All, A, B, C, D
const selectedFilter = ref('All'); // All, Available, Occupied

const parkingRecords = ref([]);
const dbSpaces = ref([]);
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
        vehicle_type: null,
        description: null
      });
    }
  });
  return list;
};

const fetchParkingData = async () => {
  try {
    const token = localStorage.getItem('token');
    const headers = { Authorization: `Bearer ${token}` };

    const [parkRes, spaceRes] = await Promise.allSettled([
      axios.get('http://127.0.0.1:8000/parking/', { headers }),
      axios.get('http://127.0.0.1:8000/parking-spaces/', { headers })
    ]);

    if (parkRes.status === 'fulfilled') {
      parkingRecords.value = parkRes.value.data;
    }

    if (spaceRes.status === 'fulfilled') {
      dbSpaces.value = spaceRes.value.data;
    }
    
    // បញ្ចូលស្ថានភាពរថយន្តកំពុងចតចូលទៅក្នុង Slot ចំណត
    const baseSpaces = generateSpaces();
    const activeParkings = parkingRecords.value.filter(p => !p.check_out_time);
    
    // សម្គាល់ឡានកំពុងចត
    activeParkings.forEach((p, idx) => {
      const slotIndex = idx % 80;
      baseSpaces[slotIndex].status = 'Occupied';
      baseSpaces[slotIndex].plate_number = p.plate_number;
      baseSpaces[slotIndex].vehicle_type = p.vehicle_type;
    });

    // ពិនិត្យក្រែងលោមានកំណត់ត្រាក្នុង DB parking_spaces ដែលមិនទំនេរ (is_available == False)
    dbSpaces.value.forEach(ds => {
      const found = baseSpaces.find(bs => bs.id === ds.name);
      if (found) {
        found.description = ds.description;
        if (!ds.is_available) {
          found.status = 'Occupied';
        }
      }
    });

    spaces.value = baseSpaces;
  } catch (error) {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      router.push('/login');
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

onMounted(() => {
  spaces.value = generateSpaces();
  fetchParkingData();
});
</script>

<template>
  <div class="flex h-screen bg-[#f8fafc] font-sans text-gray-800">
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden relative">
      <Navbar title="Parking Spaces" subtitle="Home / Parking Spaces" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        <!-- Title & Counter -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-8">
          <div>
            <h2 class="text-2xl font-extrabold text-gray-800">ប្លង់កន្លែងចតរថយន្ត (Parking Spaces)</h2>
            <p class="text-sm text-gray-500 mt-1">ទិដ្ឋភាពរួមនៃទីតាំងចំណតសរុប ៨០ កន្លែង ចែកជា ៤ តំបន់ (Zone A, B, C, D)</p>
          </div>
          <div class="flex items-center gap-4">
            <span class="px-3.5 py-1.5 text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-full flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
              ទំនេរ {{ availableCount }} កន្លែង
            </span>
            <span class="px-3.5 py-1.5 text-xs font-bold bg-rose-50 text-rose-700 border border-rose-200 rounded-full flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-rose-500"></span>
              មានឡានចត {{ occupiedCount }} កន្លែង
            </span>
          </div>
        </div>

        <!-- Filter Controls -->
        <div class="flex flex-wrap items-center justify-between gap-4 mb-6 bg-white p-4 rounded-2xl border border-gray-100 shadow-2xs">
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-gray-400 uppercase tracking-wider mr-2">Zone:</span>
            <button 
              v-for="z in ['All', 'A', 'B', 'C', 'D']" 
              :key="z"
              @click="selectedZone = z"
              :class="selectedZone === z ? 'bg-primary text-white font-bold shadow' : 'bg-gray-50 text-gray-600 hover:bg-gray-100'"
              class="px-3.5 py-1.5 rounded-xl text-xs transition-all border border-gray-200"
            >
              {{ z === 'All' ? 'គ្រប់ Zone' : `Zone ${z}` }}
            </button>
          </div>

          <div class="flex items-center gap-2">
            <span class="text-xs font-bold text-gray-400 uppercase tracking-wider mr-2">Status:</span>
            <button 
              v-for="f in ['All', 'Available', 'Occupied']" 
              :key="f"
              @click="selectedFilter = f"
              :class="selectedFilter === f ? 'bg-primary text-white font-bold shadow' : 'bg-gray-50 text-gray-600 hover:bg-gray-100'"
              class="px-3.5 py-1.5 rounded-xl text-xs transition-all border border-gray-200"
            >
              {{ f === 'All' ? 'ទាំងអស់' : (f === 'Available' ? 'កន្លែងទំនេរ' : 'មានឡានចត') }}
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
