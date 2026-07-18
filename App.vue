<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6 font-sans">
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
      <h1 class="text-2xl font-bold text-emerald-800 mb-2">VyaaparDrishti AI</h1>
      <p class="text-sm text-gray-500 mb-6">Upload physical ledger images for instant risk scoring.</p>
      
      <div class="border-2 border-dashed border-emerald-300 rounded-xl p-6 text-center bg-emerald-50/50 mb-6">
        <input type="file" @change="onFileSelected" accept="image/*" class="hidden" id="fileInput"/>
        <label for="fileInput" class="cursor-pointer text-emerald-700 font-semibold block">
          {{ selectedFile ? selectedFile.name : 'Click to select ledger photo' }}
        </label>
      </div>

      <button @click="uploadImage" :disabled="!selectedFile || loading" 
              class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-3 rounded-xl transition duration-200 disabled:opacity-50">
        {{ loading ? 'Processing Asynchronously...' : 'Analyze Ledger' }}
      </button>

      <div v-if="insights" class="mt-8 border-t pt-6">
        <h3 class="font-bold text-gray-800 text-lg mb-4">Risk Evaluation Results</h3>
        <div class="flex items-center justify-between p-3 bg-gray-100 rounded-lg mb-3">
          <span class="text-sm font-medium text-gray-600">Calculated Risk Score:</span>
          <span :class="insights.risk_score > 50 ? 'text-red-600' : 'text-emerald-600'" class="font-bold text-xl">
            {{ insights.risk_score }}/100
          </span>
        </div>
        <div class="bg-red-50 p-4 rounded-xl border border-red-100">
          <span class="text-xs font-bold text-red-700 tracking-wider uppercase block mb-2">System Risk Flags</span>
          <ul class="list-disc list-inside text-sm text-red-900 space-y-1">
            <li v-for="flag in insights.extracted_data.risk_flags" :key="flag">{{ flag }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      taskId: null,
      loading: false,
      insights: null,
      pollInterval: null
    };
  },
  methods: {
    onFileSelected(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadImage() {
      this.loading = true;
      this.insights = null;
      const formData = new FormData();
      formData.append('image', this.selectedFile);

      try {
        const response = await axios.post('http://localhost:5000/api/upload', formData);
        this.taskId = response.data.task_id;
        this.startPolling();
      } catch (error) {
        alert('Upload failed. Check backend configuration.');
        this.loading = false;
      }
    },
    startPolling() {
      this.pollInterval = setInterval(async () => {
        try {
          const response = await axios.get(`http://localhost:5000/api/status/${this.taskId}`);
          if (response.data.status === 'COMPLETED') {
            this.insights = response.data;
            clearInterval(this.pollInterval);
            this.loading = false;
          }
        } catch (error) {
          clearInterval(this.pollInterval);
          this.loading = false;
        }
      }, 2000);
    }
  },
  beforeUnmount() {
    if (this.pollInterval) clearInterval(this.pollInterval);
  }
};
</script>
