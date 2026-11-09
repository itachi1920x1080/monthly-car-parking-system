<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
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
        
        <router-link to="/notifications" active-class="bg-white/10 text-white font-semibold" class="flex items-center justify-between px-4 py-2.5 text-gray-300 hover:bg-white/5 hover:text-white rounded-xl transition-colors">
          <div class="flex items-center gap-3">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
            Notifications
          </div>
          <span v-if="unreadCount > 0" class="px-2 py-0.5 text-[10px] font-bold bg-red-500 text-white rounded-full">{{ unreadCount }}</span>
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
      <!-- Top Header -->
      <header class="h-20 bg-white border-b border-gray-100 flex items-center justify-between px-8 z-10">
        <div class="flex items-center gap-3">
          <h2 class="text-xl font-bold text-gray-800">ការជូនដំណឹង (Notifications)</h2>
          <span v-if="unreadCount > 0" class="px-2.5 py-1 text-xs font-bold bg-red-100 text-red-600 rounded-full">
            {{ unreadCount }} មិនទាន់អាន
          </span>
        </div>
        
        <div class="flex items-center gap-4">
          <button @click="markAllAsRead" class="text-xs font-semibold text-primary hover:underline flex items-center gap-1.5 bg-green-50 px-3 py-2 rounded-xl border border-green-100 transition-colors">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
            សម្គាល់ថាបានអានទាំងអស់
          </button>
          
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-full bg-primary text-white flex items-center justify-center font-bold text-sm shadow-sm">A</div>
            <div>
              <p class="text-sm font-bold text-gray-800 leading-tight">{{ userName }}</p>
              <p class="text-xs text-gray-500">Administrator</p>
            </div>
          </div>
        </div>
      </header>

      <!-- Content -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        
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
