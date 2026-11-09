<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Sidebar from '../components/Sidebar.vue';
import Navbar from '../components/Navbar.vue';

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
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden relative">
      <Navbar title="System Settings" subtitle="Home / Settings" />

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

