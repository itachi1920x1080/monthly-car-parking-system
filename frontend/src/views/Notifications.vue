<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Sidebar from '../components/Sidebar.vue';
import Navbar from '../components/Navbar.vue';
import axios from 'axios';

const router = useRouter();
const userName = ref('Admin');
const activeTab = ref('all'); // all, unread, payment, contract, parking

// បញ្ជីការជូនដំណឹង (Notifications List)
const notifications = ref([
  {
    id: 1,
    title: 'ការទូទាត់ប្រាក់ជោគជ័យ',
    message: 'អតិថិជន Chan Sok បានបង់ប្រាក់ចំនួន $50.00 តាមរយៈ KHQR/ABA ជោគជ័យ។',
    type: 'payment',
    time: '10 នាទីមុន',
    date: '2026-11-09 13:40',
    isRead: false,
    severity: 'success'
  },
  {
    id: 2,
    title: 'កិច្ចសន្យាជិតផុតកំណត់',
    message: 'កិច្ចសន្យា #CT-001 របស់លោក Sokha Keo (ចំណត B-12) នឹងផុតកំណត់ក្នុងរយៈពេល ៥ ថ្ងៃទៀត។',
    type: 'contract',
    time: '1 ម៉ោងមុន',
    date: '2026-11-09 12:30',
    isRead: false,
    severity: 'warning'
  },
  {
    id: 3,
    title: 'ចំណតឡានជិតពេញ (High Occupancy)',
    message: 'តំបន់ចំណត Zone A មានរថយន្តចតពេញ ៨៥% ហើយ (នៅសល់តែ ៣ កន្លែងទៀតប៉ុណ្ណោះ)។',
    type: 'parking',
    time: '3 ម៉ោងមុន',
    date: '2026-11-09 10:15',
    isRead: true,
    severity: 'info'
  },
  {
    id: 4,
    title: 'វិក្កយបត្រហួសកាលកំណត់បង់ប្រាក់',
    message: 'វិក្កយបត្របង់ប្រាក់ប្រចាំខែ #INV-0089 របស់អតិថិជន Vanna Pich ហួសកាលកំណត់ ៣ ថ្ងៃ។',
    type: 'payment',
    time: 'ម្សិលមិញ',
    date: '2026-11-08 16:20',
    isRead: true,
    severity: 'danger'
  },
  {
    id: 5,
    title: 'ចុះឈ្មោះអតិថិជនថ្មី',
    message: 'អតិថិជនថ្មី David Kim ត្រូវបានចុះឈ្មោះចូលក្នុងប្រព័ន្ធដោយជោគជ័យ។',
    type: 'system',
    time: '២ ថ្ងៃមុន',
    date: '2026-11-07 09:00',
    isRead: true,
    severity: 'info'
  }
]);

// គណនាចំនួន Unread
const unreadCount = computed(() => notifications.value.filter(n => !n.isRead).length);

// ត្រងតាមប្រភេទ Tab
const filteredNotifications = computed(() => {
  if (activeTab.value === 'unread') {
    return notifications.value.filter(n => !n.isRead);
  }
  if (activeTab.value === 'payment') {
    return notifications.value.filter(n => n.type === 'payment');
  }
  if (activeTab.value === 'contract') {
    return notifications.value.filter(n => n.type === 'contract');
  }
  if (activeTab.value === 'parking') {
    return notifications.value.filter(n => n.type === 'parking');
  }
  return notifications.value;
});

// សម្គាល់ថាបានអានទាំងអស់
const markAllAsRead = () => {
  notifications.value.forEach(n => n.isRead = true);
};

// សម្គាល់មួយៗ
const toggleReadStatus = (id) => {
  const item = notifications.value.find(n => n.id === id);
  if (item) item.isRead = !item.isRead;
};

// លុបការជូនដំណឹង
const deleteNotification = (id) => {
  notifications.value = notifications.value.filter(n => n.id !== id);
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

onMounted(() => {
  const token = localStorage.getItem('token');
  if (!token) router.push('/login');
});
</script>

<template>
  <div class="flex h-screen bg-[#f8fafc] font-sans text-gray-800">
    
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden relative">
      <Navbar title="Notifications" subtitle="Home / Notifications" />

      <!-- Content -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        <!-- Title & Action Bar -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div class="flex items-center gap-3">
            <h2 class="text-2xl font-extrabold text-gray-800">មជ្ឈមណ្ឌលជូនដំណឹង (Notifications)</h2>
            <span v-if="unreadCount > 0" class="px-2.5 py-1 text-xs font-bold bg-red-100 text-red-600 rounded-full">
              {{ unreadCount }} មិនទាន់អាន
            </span>
          </div>
          <button @click="markAllAsRead" class="text-xs font-semibold text-primary hover:underline flex items-center gap-1.5 bg-green-50 px-3.5 py-2 rounded-xl border border-green-200 shadow-2xs transition-all">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
            សម្គាល់ថាបានអានទាំងអស់
          </button>
        </div>
        
        <!-- Filter Tabs -->
        <div class="flex items-center justify-between mb-6 pb-2 border-b border-gray-200">
          <div class="flex items-center gap-2">
            <button 
              @click="activeTab = 'all'" 
              :class="activeTab === 'all' ? 'bg-primary text-white font-bold' : 'bg-white text-gray-600 hover:bg-gray-100'"
              class="px-4 py-2 rounded-xl text-xs transition-all shadow-sm border border-gray-200"
            >
              ទាំងអស់ ({{ notifications.length }})
            </button>
            <button 
              @click="activeTab = 'unread'" 
              :class="activeTab === 'unread' ? 'bg-primary text-white font-bold' : 'bg-white text-gray-600 hover:bg-gray-100'"
              class="px-4 py-2 rounded-xl text-xs transition-all shadow-sm border border-gray-200 flex items-center gap-1.5"
            >
              <span class="w-2 h-2 rounded-full bg-red-500"></span>
              មិនទាន់អាន ({{ unreadCount }})
            </button>
            <button 
              @click="activeTab = 'payment'" 
              :class="activeTab === 'payment' ? 'bg-primary text-white font-bold' : 'bg-white text-gray-600 hover:bg-gray-100'"
              class="px-4 py-2 rounded-xl text-xs transition-all shadow-sm border border-gray-200"
            >
              💵 ការទូទាត់ប្រាក់
            </button>
            <button 
              @click="activeTab = 'contract'" 
              :class="activeTab === 'contract' ? 'bg-primary text-white font-bold' : 'bg-white text-gray-600 hover:bg-gray-100'"
              class="px-4 py-2 rounded-xl text-xs transition-all shadow-sm border border-gray-200"
            >
              📄 កិច្ចសន្យា
            </button>
            <button 
              @click="activeTab = 'parking'" 
              :class="activeTab === 'parking' ? 'bg-primary text-white font-bold' : 'bg-white text-gray-600 hover:bg-gray-100'"
              class="px-4 py-2 rounded-xl text-xs transition-all shadow-sm border border-gray-200"
            >
              🚗 ចំណតយានយន្ត
            </button>
          </div>
          
          <p class="text-xs text-gray-400">បង្ហាញ {{ filteredNotifications.length }} ការជូនដំណឹង</p>
        </div>

        <!-- Notifications List -->
        <div class="space-y-3">
          <div 
            v-for="item in filteredNotifications" 
            :key="item.id"
            :class="[
              'p-5 rounded-2xl border transition-all flex items-start justify-between gap-4',
              item.isRead ? 'bg-white border-gray-100 opacity-80' : 'bg-emerald-50/40 border-emerald-200 shadow-sm'
            ]"
          >
            <div class="flex items-start gap-4">
              <!-- Severity Icon -->
              <div 
                :class="[
                  'w-11 h-11 rounded-2xl flex items-center justify-center shrink-0 text-lg shadow-xs',
                  item.severity === 'success' ? 'bg-green-100 text-green-700' :
                  item.severity === 'warning' ? 'bg-amber-100 text-amber-700' :
                  item.severity === 'danger' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
                ]"
              >
                <span v-if="item.type === 'payment'">💵</span>
                <span v-else-if="item.type === 'contract'">📄</span>
                <span v-else-if="item.type === 'parking'">🅿️</span>
                <span v-else>🔔</span>
              </div>

              <!-- Content Text -->
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <h3 :class="['text-sm', item.isRead ? 'font-semibold text-gray-700' : 'font-bold text-gray-900']">
                    {{ item.title }}
                  </h3>
                  <span v-if="!item.isRead" class="w-2 h-2 rounded-full bg-primary inline-block"></span>
                </div>
                <p class="text-xs text-gray-600 leading-relaxed mb-2">{{ item.message }}</p>
                <div class="flex items-center gap-3 text-[11px] text-gray-400 font-mono">
                  <span>{{ item.time }}</span>
                  <span>•</span>
                  <span>{{ item.date }}</span>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center gap-2 shrink-0">
              <button 
                @click="toggleReadStatus(item.id)" 
                class="px-3 py-1.5 text-xs font-semibold rounded-xl border transition-colors"
                :class="item.isRead ? 'border-gray-200 text-gray-500 hover:bg-gray-100' : 'border-primary text-primary hover:bg-green-50'"
              >
                {{ item.isRead ? 'សម្គាល់មិនទាន់អាន' : 'អានរួច' }}
              </button>
              
              <button 
                @click="deleteNotification(item.id)" 
                class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-xl transition-colors"
                title="លុបចោល"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
            </div>
          </div>

          <div v-if="filteredNotifications.length === 0" class="text-center py-16 bg-white rounded-2xl border border-gray-100">
            <div class="w-16 h-16 bg-gray-50 text-gray-400 rounded-full flex items-center justify-center mx-auto mb-3 text-2xl">
              📭
            </div>
            <p class="text-sm font-semibold text-gray-600">មិនមានការជូនដំណឹងនៅក្នុងប្រអប់នេះទេ</p>
            <p class="text-xs text-gray-400 mt-1">រាល់ព្រឹត្តិការណ៍ថ្មីៗនឹងលេចឡើងនៅទីនេះ</p>
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

