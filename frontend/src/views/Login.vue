<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const errorMsg = ref('');
const isLoading = ref(false);
const router = useRouter();

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
    
    localStorage.setItem('token', response.data.access_token);
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
  <div class="min-h-screen flex">
    <!-- ផ្នែកខាងឆ្វេង (រូបភាព និង អត្ថបទ) -->
    <div class="hidden lg:flex lg:w-1/2 bg-primary relative text-white flex-col justify-center px-16 overflow-hidden">
      <!-- Background Overlay (ដើម្បីឲ្យមើលទៅដូចមានស្រមោលឡាន) -->
      <div class="absolute inset-0 bg-gradient-to-br from-primary via-[#0a4d3b] to-black opacity-90 z-0"></div>
      
      <div class="relative z-10 -mt-10">
        <div class="flex items-center gap-3 mb-12">
          <div class="w-12 h-12 bg-white text-primary rounded-xl flex items-center justify-center font-bold text-3xl shadow-md">
            P
          </div>
          <div>
            <h1 class="text-3xl font-bold tracking-tight">Car<span class="text-emerald-400">Park</span></h1>
            <span class="text-xs font-normal text-emerald-200/80 uppercase tracking-wider">Monthly Parking Management System</span>
          </div>
        </div>

        <h2 class="text-5xl font-extrabold mb-4 leading-tight tracking-tight">
          Smart Parking <br>
          <span class="text-emerald-400">Better Life</span>
        </h2>
        <p class="text-gray-200 text-lg mb-10 max-w-md font-light leading-relaxed">
          Manage your monthly parking with ease. Safe, secure and convenient.
        </p>

        <!-- Feature Pills from the image -->
        <div class="grid grid-cols-2 gap-4 max-w-md pt-4 border-t border-white/10">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-white/10 flex items-center justify-center text-emerald-300 shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z" /></svg>
            </div>
            <div>
              <p class="text-sm font-semibold">Secure Access</p>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-white/10 flex items-center justify-center text-emerald-300 shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 01-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 00-3.213-9.193 2.056 2.056 0 00-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 00-10.026 0 1.106 1.106 0 00-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" /></svg>
            </div>
            <div>
              <p class="text-sm font-semibold">Real-time Availability</p>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-white/10 flex items-center justify-center text-emerald-300 shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" /></svg>
            </div>
            <div>
              <p class="text-sm font-semibold">Payment Reminders</p>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-lg bg-white/10 flex items-center justify-center text-emerald-300 shrink-0">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" /></svg>
            </div>
            <div>
              <p class="text-sm font-semibold">Detailed Reports</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ផ្នែកខាងស្តាំ (Form Login) -->
    <div class="w-full lg:w-1/2 flex items-center justify-center bg-gray-50/50 p-6 sm:p-12">
      <div class="w-full max-w-md bg-white p-8 sm:p-10 rounded-2xl shadow-xl shadow-gray-200/60 border border-gray-100">
        
        <div class="flex flex-col items-center mb-8">
          <div class="w-16 h-16 bg-primary text-white rounded-2xl flex items-center justify-center font-bold text-3xl mb-4 shadow-lg shadow-primary/30">
            P
          </div>
          <h2 class="text-2xl font-bold text-gray-900">Welcome to CarPark</h2>
          <p class="text-gray-500 text-sm mt-1">Sign in to your account to continue</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="space-y-5">
          
          <!-- Username Input -->
          <div>
            <label class="block text-gray-700 text-sm font-semibold mb-2">Email or Username</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" /></svg>
              </div>
              <input v-model="username" type="text" required 
                     class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all bg-gray-50/50 text-gray-800 placeholder-gray-400 text-sm" 
                     placeholder="Enter your email or username">
            </div>
          </div>
          
          <!-- Password Input -->
          <div>
            <label class="block text-gray-700 text-sm font-semibold mb-2">Password</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" /></svg>
              </div>
              <input v-model="password" type="password" required 
                     class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all bg-gray-50/50 text-gray-800 placeholder-gray-400 text-sm" 
                     placeholder="Enter your password">
            </div>
          </div>

          <!-- Options -->
          <div class="flex items-center justify-between text-sm">
            <label class="flex items-center text-gray-600 cursor-pointer select-none">
              <input type="checkbox" class="w-4 h-4 mr-2 rounded border-gray-300 text-primary focus:ring-primary accent-primary">
              Remember me
            </label>
            <a href="#" class="text-primary hover:text-secondary hover:underline font-semibold text-xs">Forgot password?</a>
          </div>
          
          <!-- Error Message -->
          <div v-if="errorMsg" class="bg-red-50 text-red-600 p-3.5 rounded-xl text-sm text-center border border-red-100 flex items-center justify-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4 shrink-0"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-5a.75.75 0 01.75.75v4.5a.75.75 0 01-1.5 0v-4.5A.75.75 0 0110 5zm0 10a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" /></svg>
            <span>{{ errorMsg }}</span>
          </div>
          
          <!-- Submit Button -->
          <button type="submit" :disabled="isLoading"
                  class="w-full bg-primary text-white font-semibold py-3.5 px-4 rounded-xl hover:bg-secondary transition duration-300 flex justify-center items-center gap-2 shadow-lg shadow-primary/25 mt-2 disabled:opacity-70 disabled:cursor-not-allowed">
            <svg v-if="!isLoading" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" /></svg>
            <span v-if="isLoading">Signing in...</span>
            <span v-else>Sign In</span>
          </button>
        </form>

        <div class="mt-8 pt-6 border-t border-gray-100 text-center">
          <p class="text-xs text-gray-400">
            CarPark Monthly Parking Management System &copy; 2026
          </p>
        </div>

      </div>
    </div>
  </div>
</template>
