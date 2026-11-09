<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

// Mode: 'roleSelect' (ផ្ទាំងជ្រើសរើស Role ដូចក្នុង Mockup) ឬ 'loginForm' (ផ្ទាំងបញ្ចូល Password)
const mode = ref('roleSelect');
const selectedRole = ref('Administrator');

const username = ref('admin');
const password = ref('admin123');
const errorMsg = ref('');
const isLoading = ref(false);
const router = useRouter();

const selectRole = (role) => {
  selectedRole.value = role;
  if (role === 'Administrator') {
    username.value = 'admin';
    password.value = 'admin123';
  } else if (role === 'Cashier') {
    username.value = 'cashier';
    password.value = 'cashier123';
  } else {
    username.value = 'customer';
    password.value = 'customer123';
  }
  mode.value = 'loginForm';
};

const handleLogin = async () => {
  isLoading.value = true;
  errorMsg.value = '';
  try {
    const params = new URLSearchParams();
    params.append('username', username.value);
    params.append('password', password.value);

    const response = await axios.post('http://127.0.0.1:8000/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    
    const role = (response.data.role || (selectedRole.value === 'Administrator' ? 'admin' : selectedRole.value === 'Cashier' ? 'cashier' : 'customer')).toLowerCase();
    const name = response.data.username || username.value;

    localStorage.setItem('token', response.data.access_token);
    localStorage.setItem('user_role', role);
    localStorage.setItem('user_name', name);
    router.push('/dashboard'); 
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      errorMsg.value = error.response.data.detail;
    } else {
      errorMsg.value = "Email or Username and Password do not match.";
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="min-h-screen flex font-sans">
    
    <!-- ផ្នែកខាងឆ្វេង (Hero Banner & Feature Highlights ដូចក្នុង Design System) -->
    <div class="hidden lg:flex lg:w-1/2 bg-primary relative text-white flex-col justify-between p-16 overflow-hidden">
      <!-- Gradient & Background Effect -->
      <div class="absolute inset-0 bg-gradient-to-br from-[#0D664F] via-[#074b3a] to-[#04281f] z-0"></div>
      
      <!-- Subtle Decorative Circle Glow -->
      <div class="absolute -top-32 -left-32 w-96 h-96 bg-emerald-400/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -bottom-32 -right-32 w-96 h-96 bg-emerald-300/10 rounded-full blur-3xl pointer-events-none"></div>

      <!-- Top Brand Logo -->
      <div class="relative z-10 flex items-center gap-3">
        <div class="w-12 h-12 bg-white text-primary rounded-xl flex items-center justify-center font-bold text-3xl shadow-lg">
          P
        </div>
        <div>
          <h1 class="text-3xl font-extrabold tracking-tight">Car<span class="text-emerald-400">Park</span></h1>
          <p class="text-xs font-medium text-emerald-200/80 uppercase tracking-wider">Monthly Parking Management System</p>
        </div>
      </div>

      <!-- Middle Headline Content -->
      <div class="relative z-10 my-auto py-12">
        <h2 class="text-5xl font-extrabold mb-5 leading-tight tracking-tight">
          Smart Parking <br>
          <span class="text-emerald-400">Better Life</span>
        </h2>
        <p class="text-emerald-100/90 text-lg max-w-md font-light leading-relaxed">
          Manage your monthly parking with ease. Safe, secure and convenient.
        </p>
      </div>

      <!-- Bottom Feature Badges matching mockup -->
      <div class="relative z-10 grid grid-cols-2 gap-6 pt-6 border-t border-white/10">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-emerald-300 shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" /></svg>
          </div>
          <div>
            <p class="text-sm font-semibold">Secure Access</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-emerald-300 shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" /></svg>
          </div>
          <div>
            <p class="text-sm font-semibold">Real-time Availability</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-emerald-300 shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" /></svg>
          </div>
          <div>
            <p class="text-sm font-semibold">Payment Reminders</p>
          </div>
        </div>

        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-emerald-300 shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" /></svg>
          </div>
          <div>
            <p class="text-sm font-semibold">Detailed Reports</p>
          </div>
        </div>
      </div>
    </div>

    <!-- ផ្នែកខាងស្តាំ (Interactive Role Selector ឬ Form Login) -->
    <div class="w-full lg:w-1/2 flex items-center justify-center bg-gray-50/70 p-6 sm:p-12">
      
      <!-- MODE 1: Role Selection Card (ដូចរូបភាព Mockup 100%) -->
      <div v-if="mode === 'roleSelect'" class="w-full max-w-md bg-white p-8 sm:p-10 rounded-3xl shadow-xl shadow-gray-200/60 border border-gray-100 transition-all">
        <div class="text-left mb-8">
          <h2 class="text-2xl sm:text-3xl font-extrabold text-primary">Welcome to CarPark</h2>
          <p class="text-gray-500 text-sm mt-1">Please select your role to continue</p>
        </div>

        <!-- 3 Role Options -->
        <div class="space-y-4">
          
          <!-- Role 1: Administrator -->
          <div @click="selectRole('Administrator')"
               class="group p-4 border border-gray-200 rounded-2xl hover:border-primary hover:shadow-md transition-all cursor-pointer flex items-center justify-between bg-white">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-xl bg-emerald-50 text-primary flex items-center justify-center group-hover:bg-primary group-hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" /></svg>
              </div>
              <div class="text-left">
                <h3 class="font-bold text-gray-800 text-base group-hover:text-primary transition-colors">Administrator</h3>
                <p class="text-xs text-gray-500 max-w-[210px] leading-relaxed">Manage users, customers, contracts, payments and system settings.</p>
              </div>
            </div>
            <div class="text-gray-400 group-hover:text-primary group-hover:translate-x-1 transition-all">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" /></svg>
            </div>
          </div>

          <!-- Role 2: Cashier -->
          <div @click="selectRole('Cashier')"
               class="group p-4 border border-gray-200 rounded-2xl hover:border-info hover:shadow-md transition-all cursor-pointer flex items-center justify-between bg-white">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-xl bg-blue-50 text-info flex items-center justify-center group-hover:bg-info group-hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6H2.25m0 0v10.5m0-10.5h19.5m0 0v10.5m0-10.5a.75.75 0 00-.75-.75h-.75M3.75 19.5h16.5a1.5 1.5 0 001.5-1.5V6.75A1.5 1.5 0 0020.25 5.25H3.75A1.5 1.5 0 002.25 6.75v11.25a1.5 1.5 0 001.5 1.5z" /></svg>
              </div>
              <div class="text-left">
                <h3 class="font-bold text-gray-800 text-base group-hover:text-info transition-colors">Cashier</h3>
                <p class="text-xs text-gray-500 max-w-[210px] leading-relaxed">Register customers, manage payments, issue receipts and daily transactions.</p>
              </div>
            </div>
            <div class="text-gray-400 group-hover:text-info group-hover:translate-x-1 transition-all">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" /></svg>
            </div>
          </div>

          <!-- Role 3: Customer -->
          <div @click="selectRole('Customer')"
               class="group p-4 border border-gray-200 rounded-2xl hover:border-purple-600 hover:shadow-md transition-all cursor-pointer flex items-center justify-between bg-white">
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center group-hover:bg-purple-600 group-hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
              </div>
              <div class="text-left">
                <h3 class="font-bold text-gray-800 text-base group-hover:text-purple-600 transition-colors">Customer</h3>
                <p class="text-xs text-gray-500 max-w-[210px] leading-relaxed">View your information, contracts, payments and notifications.</p>
              </div>
            </div>
            <div class="text-gray-400 group-hover:text-purple-600 group-hover:translate-x-1 transition-all">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" /></svg>
            </div>
          </div>

        </div>

        <!-- Footer Link -->
        <div class="mt-8 pt-6 border-t border-gray-100 text-center">
          <p class="text-xs text-gray-500">
            Already have an account? 
            <button @click="mode = 'loginForm'" class="text-primary font-bold hover:underline ml-1">Login</button>
          </p>
        </div>
      </div>

      <!-- MODE 2: Sign In Form -->
      <div v-else class="w-full max-w-md bg-white p-8 sm:p-10 rounded-3xl shadow-xl shadow-gray-200/60 border border-gray-100 transition-all">
        
        <!-- Back Button & Role Badge -->
        <div class="flex justify-between items-center mb-6">
          <button @click="mode = 'roleSelect'" class="text-xs text-gray-500 hover:text-primary flex items-center gap-1 font-medium">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" /></svg>
            Choose Role
          </button>
          <span class="text-xs font-semibold px-2.5 py-1 bg-emerald-50 text-primary rounded-full border border-emerald-100">
            {{ selectedRole }}
          </span>
        </div>

        <div class="flex flex-col items-center mb-6">
          <div class="w-14 h-14 bg-primary text-white rounded-2xl flex items-center justify-center font-bold text-2xl mb-3 shadow-md shadow-primary/25">
            P
          </div>
          <h2 class="text-2xl font-bold text-gray-900">Sign in to CarPark</h2>
          <p class="text-gray-500 text-xs mt-1">Enter your credentials to continue</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="space-y-4">
          
          <!-- Username Input -->
          <div>
            <label class="block text-gray-700 text-xs font-semibold mb-1.5">Email or Username</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" /></svg>
              </div>
              <input v-model="username" type="text" required 
                     class="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all bg-gray-50/50 text-gray-800 text-sm" 
                     placeholder="admin or user@carpark.com">
            </div>
          </div>
          
          <!-- Password Input -->
          <div>
            <label class="block text-gray-700 text-xs font-semibold mb-1.5">Password</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" /></svg>
              </div>
              <input v-model="password" type="password" required 
                     class="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all bg-gray-50/50 text-gray-800 text-sm" 
                     placeholder="••••••••">
            </div>
          </div>

          <!-- Options -->
          <div class="flex items-center justify-between text-xs">
            <label class="flex items-center text-gray-600 cursor-pointer select-none">
              <input type="checkbox" class="w-3.5 h-3.5 mr-2 rounded border-gray-300 text-primary focus:ring-primary accent-primary">
              Remember me
            </label>
            <a href="#" class="text-primary hover:text-secondary hover:underline font-semibold">Forgot password?</a>
          </div>
          
          <!-- Error Message -->
          <div v-if="errorMsg" class="bg-red-50 text-red-600 p-3 rounded-xl text-xs text-center border border-red-100 flex items-center justify-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4 shrink-0"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" /></svg>
            <span>{{ errorMsg }}</span>
          </div>
          
          <!-- Submit Button -->
          <button type="submit" :disabled="isLoading"
                  class="w-full bg-primary text-white font-semibold py-3 px-4 rounded-xl hover:bg-secondary transition duration-300 flex justify-center items-center gap-2 shadow-lg shadow-primary/20 mt-2 disabled:opacity-70 disabled:cursor-not-allowed text-sm">
            <span v-if="isLoading">Signing in...</span>
            <span v-else>Sign In as {{ selectedRole }}</span>
          </button>
        </form>

        <div class="mt-6 pt-4 border-t border-gray-100 text-center">
          <p class="text-[11px] text-gray-400">
            CarPark Monthly Parking Management System &copy; 2026
          </p>
        </div>

      </div>

    </div>
  </div>
</template>
