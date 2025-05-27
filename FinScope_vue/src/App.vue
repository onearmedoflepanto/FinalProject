<script setup>
import { RouterView, useRoute } from 'vue-router'
import NavigationBar from '@/components/NavigationBar.vue' // Assuming NavigationBar.vue is in src/components
import Footer from '@/components/footer.vue' // Assuming footer.vue is in src/components

const route = useRoute();
</script>

<template>
  <div class="flex flex-col min-h-screen bg-gray-900"> {/* Added bg-gray-900 here */}
    <NavigationBar />
    <RouterView :key="route.fullPath" class="px-4" />
    <Footer />
  </div>
</template>
