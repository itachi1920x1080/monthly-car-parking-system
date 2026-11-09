<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Sidebar from '../components/Sidebar.vue';
import Navbar from '../components/Navbar.vue';

const router = useRouter();
const userRole = ref((localStorage.getItem('user_role') || 'admin').toLowerCase());

const settings = ref({
  business_name: 'CarPark Central Management',
  contact_phone: '+855 12 345 678',
  contact_email: 'support@carpark.com',
  default_hourly_rate: 1.5,
  default_monthly_rate: 50.0,
  currency: 'USD ($)',
  total_capacity: 80,
  auto_email_receipt: true,
  enable_sms_alerts: false
});

const isSaved = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');

const fetchSettings = async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/settings/');
    if (res.data) {
      settings.value = {
        business_name: res.data.business_name ?? settings.value.business_name,
        contact_phone: res.data.contact_phone ?? settings.value.contact_phone,
        contact_email: res.data.contact_email ?? settings.value.contact_email,
        default_hourly_rate: res.data.default_hourly_rate ?? settings.value.default_hourly_rate,
        default_monthly_rate: res.data.default_monthly_rate ?? settings.value.default_monthly_rate,
        currency: res.data.currency ?? settings.value.currency,
        total_capacity: res.data.total_capacity ?? settings.value.total_capacity,
        auto_email_receipt: res.data.auto_email_receipt ?? settings.value.auto_email_receipt,
        enable_sms_alerts: res.data.enable_sms_alerts ?? settings.value.enable_sms_alerts
      };
      localStorage.setItem('default_monthly_rate', String(settings.value.default_monthly_rate));
      localStorage.setItem('business_name', settings.value.business_name);
    }
  } catch (err) {
    console.error('Failed to load settings:', err);
  }
};

const saveSettings = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const token = localStorage.getItem('token');
    const res = await axios.put('http://127.0.0.1:8000/settings/', settings.value, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    if (res.data) {
      settings.value = res.data;
      localStorage.setItem('default_monthly_rate', String(settings.value.default_monthly_rate));
      localStorage.setItem('business_name', settings.value.business_name);
    }
    isSaved.value = true;
    setTimeout(() => {
      isSaved.value = false;
    }, 3500);
  } catch (err) {
    if (err.response?.status === 403) {
      errorMessage.value = 'គ្មានសិទ្ធិ! មានតែ Administrator ប៉ុណ្ណោះដែលអាចកែប្រែថ្លៃសេវា និងការកំណត់បាន។';
    } else {
      errorMessage.value = err.response?.data?.detail || 'មិនអាចរក្សាទុកការកំណត់បានទេ!';
    }
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchSettings();
});
</script>

<template>
  <div class="flex h-screen bg-[#f8fafc] font-sans text-gray-800">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden relative">
      <Navbar title="System Settings" subtitle="Home / Settings" />

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-8">
        <!-- Success Banner -->
        <div v-if="isSaved" class="mb-6 p-4 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-2xl flex items-center gap-2 text-sm font-bold shadow-xs animate-in fade-in">
          <svg class="w-5 h-5 text-emerald-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
          ការកំណត់ និងថ្លៃសេវាចំណតត្រូវបានរក្សាទុកទៅក្នុងប្រព័ន្ធដោយជោគជ័យ!
        </div>

        <!-- Error Banner -->
        <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 text-red-800 rounded-2xl flex items-center gap-2 text-sm font-bold shadow-xs animate-in fade-in">
          <svg class="w-5 h-5 text-red-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
          {{ errorMessage }}
        </div>

        <form @submit.prevent="saveSettings" class="space-y-6 max-w-4xl">
          <!-- Parking Rates -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm space-y-4">
            <div class="flex items-center justify-between border-b border-gray-100 pb-3">
              <div>
                <h3 class="text-base font-bold text-gray-800">ថ្លៃសេវាចំណត (Parking Pricing)</h3>
                <p class="text-xs text-gray-500">កំណត់ថ្លៃជួលចំណតប្រចាំខែ និងថ្លៃចតតាមម៉ោង</p>
              </div>
              <span class="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-700 text-xs font-bold border border-emerald-200">Live Sync</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
              <div>
                <label class="block text-xs font-bold text-gray-700 mb-1.5">ថ្លៃចតប្រចាំខែ ($ / Month)</label>
                <div class="relative">
                  <span class="absolute left-3 top-2.5 text-gray-400 font-bold">$</span>
                  <input v-model.number="settings.default_monthly_rate" required type="number" step="0.5" min="0" class="w-full pl-8 pr-3 py-2.5 border border-gray-300 rounded-xl text-sm font-semibold focus:ring-primary focus:border-primary">
                </div>
                <p class="text-[11px] text-gray-400 mt-1">តម្លៃគោលសម្រាប់ចេញវិក្កយបត្រកិច្ចសន្យាប្រចាំខែ</p>
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-700 mb-1.5">ថ្លៃចតប្រចាំម៉ោង ($ / Hour)</label>
                <div class="relative">
                  <span class="absolute left-3 top-2.5 text-gray-400 font-bold">$</span>
                  <input v-model.number="settings.default_hourly_rate" required type="number" step="0.25" min="0" class="w-full pl-8 pr-3 py-2.5 border border-gray-300 rounded-xl text-sm font-semibold focus:ring-primary focus:border-primary">
                </div>
                <p class="text-[11px] text-gray-400 mt-1">តម្លៃសម្រាប់រថយន្តចតបណ្តោះអាសន្ន</p>
              </div>
            </div>
          </div>

          <!-- Facility Profile -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm space-y-4">
            <h3 class="text-base font-bold text-gray-800 border-b border-gray-100 pb-3">ព័ត៌មានចំណត (Facility Profile)</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-bold text-gray-700 mb-1.5">ឈ្មោះស្ថាប័ន / ចំណត</label>
                <input v-model="settings.business_name" required type="text" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-700 mb-1.5">ចំណុះចំណតសរុប (Capacity)</label>
                <input v-model.number="settings.total_capacity" required type="number" min="1" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-700 mb-1.5">លេខទូរស័ព្ទទំនាក់ទំនង</label>
                <input v-model="settings.contact_phone" required type="text" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
              </div>
              <div>
                <label class="block text-xs font-bold text-gray-700 mb-1.5">អ៊ីមែលទំនាក់ទំនង</label>
                <input v-model="settings.contact_email" required type="email" class="w-full p-2.5 border border-gray-300 rounded-xl text-sm focus:ring-primary focus:border-primary">
              </div>
            </div>
          </div>

          <!-- Notification Toggles -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm space-y-4">
            <h3 class="text-base font-bold text-gray-800 border-b border-gray-100 pb-3">ការជូនដំណឹងស្វ័យប្រវត្ត (Automations)</h3>
            <div class="space-y-3">
              <label class="flex items-center gap-3 cursor-pointer">
                <input v-model="settings.auto_email_receipt" type="checkbox" class="w-4 h-4 text-primary rounded focus:ring-primary">
                <span class="text-sm text-gray-700 font-medium">ផ្ញើវិក្កយបត្រស្វ័យប្រវត្តតាមអ៊ីមែលពេលអតិថិជនបង់ប្រាក់</span>
              </label>
              <label class="flex items-center gap-3 cursor-pointer">
                <input v-model="settings.enable_sms_alerts" type="checkbox" class="w-4 h-4 text-primary rounded focus:ring-primary">
                <span class="text-sm text-gray-700 font-medium">ផ្ញើសារ SMS រំលឹកមុនកិច្ចសន្យាជិតផុតកំណត់ ៥ ថ្ងៃ</span>
              </label>
            </div>
          </div>

          <div class="flex justify-end gap-3">
            <button 
              type="submit" 
              :disabled="isLoading"
              class="px-6 py-2.5 bg-primary text-white rounded-xl text-sm font-bold hover:bg-emerald-700 transition-colors shadow-sm disabled:opacity-50 flex items-center gap-2"
            >
              <svg v-if="isLoading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
              រក្សាទុកការកំណត់
            </button>
          </div>
        </form>
      </main>
    </div>
  </div>
</template>
