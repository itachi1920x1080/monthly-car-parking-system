<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const userName = ref('Admin');

const settings = ref({
  businessName: 'CarPark Central Management',
  contactPhone: '+855 12 345 678',
  contactEmail: 'support@carpark.com',
  defaultHourlyRate: 1.5,
  defaultMonthlyRate: 50.0,
  currency: 'USD ($)',
  totalCapacity: 80,
  autoEmailReceipt: true,
  enableSmsAlerts: false
});

const isSaved = ref(false);

const saveSettings = () => {
  isSaved.value = true;
  setTimeout(() => {
    isSaved.value = false;
  }, 3000);
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};
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
        <h2 class="text-xl font-bold text-gray-800">ការកំណត់ប្រព័ន្ធ (System Settings)</h2>
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-full bg-primary text-white flex items-center justify-center font-bold text-sm shadow-sm">A</div>
          <div>
            <p class="text-sm font-bold text-gray-800 leading-tight">{{ userName }}</p>
            <p class="text-xs text-gray-500">Administrator</p>
          </div>
        </div>
      </header>

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        <div v-if="isSaved" class="mb-6 p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-2xl flex items-center gap-2 text-sm font-semibold">
          <svg class="w-5 h-5 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
          ការកំណត់ត្រូវបានរក្សាទុកដោយជោគជ័យ!
        </div>

        <form @submit.prevent="saveSettings" class="space-y-6 max-w-4xl">
          <!-- Parking Rates -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm space-y-4">
            <h3 class="text-base font-bold text-gray-800 border-b border-gray-100 pb-3">ថ្លៃសេវាចំណត (Parking Pricing)</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-semibold text-gray-600 mb-1">ថ្លៃចតប្រចាំខែ ($ / Month)</label>
                <input v-model.number="settings.defaultMonthlyRate" type="number" step="0.5" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-600 mb-1">ថ្លៃចតប្រចាំម៉ោង ($ / Hour)</label>
                <input v-model.number="settings.defaultHourlyRate" type="number" step="0.25" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
              </div>
            </div>
          </div>

          <!-- Facility Profile -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm space-y-4">
            <h3 class="text-base font-bold text-gray-800 border-b border-gray-100 pb-3">ព័ត៌មានចំណត (Facility Profile)</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-semibold text-gray-600 mb-1">ឈ្មោះស្ថាប័ន / ចំណត</label>
                <input v-model="settings.businessName" type="text" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-600 mb-1">ចំណុះចំណតសរុប (Capacity)</label>
                <input v-model.number="settings.totalCapacity" type="number" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-600 mb-1">លេខទូរស័ព្ទទំនាក់ទំនង</label>
                <input v-model="settings.contactPhone" type="text" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-600 mb-1">អ៊ីមែលទំនាក់ទំនង</label>
                <input v-model="settings.contactEmail" type="email" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
              </div>
            </div>
          </div>

          <!-- Notification Toggles -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm space-y-4">
            <h3 class="text-base font-bold text-gray-800 border-b border-gray-100 pb-3">ការជូនដំណឹងស្វ័យប្រវត្ត (Automations)</h3>
            <div class="space-y-3">
              <label class="flex items-center gap-3 cursor-pointer">
                <input v-model="settings.autoEmailReceipt" type="checkbox" class="w-4 h-4 text-primary rounded focus:ring-primary">
                <span class="text-sm text-gray-700 font-medium">ផ្ញើវិក្កយបត្រស្វ័យប្រវត្តតាមអ៊ីមែលពេលអតិថិជនបង់ប្រាក់</span>
              </label>
              <label class="flex items-center gap-3 cursor-pointer">
                <input v-model="settings.enableSmsAlerts" type="checkbox" class="w-4 h-4 text-primary rounded focus:ring-primary">
                <span class="text-sm text-gray-700 font-medium">ផ្ញើសារ SMS រំលឹកមុនកិច្ចសន្យាជិតផុតកំណត់ ៥ ថ្ងៃ</span>
              </label>
            </div>
          </div>

          <div class="flex justify-end">
            <button type="submit" class="px-6 py-2.5 bg-primary text-white rounded-xl text-sm font-bold hover:bg-emerald-700 transition-colors shadow-sm">
              រក្សាទុកការកំណត់
            </button>
          </div>
        </form>
      </main>
    </div>
  </div>
</template>

